# Multi-tenant signal product

Miguel uses the scanner first. The same service later sells signal access. Tenancy, plans, and publication are part of the model now so a public launch is a flag and a legal gate, not a rewrite.

This is a product plan. It is not legal advice. Competitor prices are not filled in. That note is [competitive-analysis.md](competitive-analysis.md).

File-level routes, models, and indexes for the new domains are under "Multi-tenant domains" in [repositories.md](repositories.md).

## Tenancy

One deployment, many accounts.

| Role | Who | Access |
| --- | --- | --- |
| `owner` | Miguel, seeded | Everything, including unpublished signals and billing admin |
| `admin` | Staff he adds | Users, audit, support. Not a paid plan |
| `subscriber` | Paying or trialing account | Entitlements of their plan |
| `free` | Signed-up account with no paid plan | The free tier only |

`PUBLIC_SIGNUP` defaults to false (`app_settings` key `tenancy` once Mongo is seeded; the env var is the switch until then). While it is false, signup is closed and the deployment key (`API_KEY`) acts as the owner. That is single-tenant mode. Opening signup does not change collections.

The deployment `API_KEY` is not a customer secret. Customer access is a JWT or a user API key. The worker keeps using the deployment key.

## Auth

Two credentials, one middleware.

- **JWT.** `POST /api/v1/auth/login` checks the password hash and returns a short-lived access token (15 minutes) and a refresh token. Refresh tokens are stored as a hash, rotated on use, and revoked on logout. Access tokens carry `user_id` and `role`.
- **User API key.** Header `X-API-Key` with a `cs_live_` prefix. Only the hash and the last four characters are stored. Keys have scopes (`signals:read`, `account:read`) and an expiry. Creating one requires `entitlements.api_access`.
- **Deployment key.** The existing `API_KEY` env var. Accepted only as the owner, and only from the worker and from Miguel while signup is closed.

`Core.auth.require_user` is the dependency every protected route will use. Order: rate limit, then auth, then entitlement. The skeleton still uses `require_api_key` on the current routes so local development with an empty key keeps working. `require_user` is present and, until JWT verification is implemented, delegates to that same check.

Passwords are hashed with Argon2id when signup is built. The field exists now. Nothing hashes a password in this pass.

`GET /api/v1/auth/config` is public enough for the client to know whether the form is shown. The skeleton returns `public_signup: false` and `mode: single_tenant`.

## Plans and entitlements

A plan is a sellable bundle. A subscription ties a user to a plan and a payment state. An entitlement check reads the subscription, not a hardcoded role, except `owner` and `admin`, who bypass quotas.

Seed plans have no prices. Prices wait on the competitive note and on Miguel. Currency placeholder is CAD because he is in Alberta. That is not a decision that CAD is the only currency Stripe will charge.

| Code | Who | Signal delay | Symbols | API | Channels in the seed |
| --- | --- | --- | --- | --- | --- |
| `free` | Default signup | 3600 seconds | 3 | no | `grok_chat` |
| `starter` | Paid | 900 seconds | 10 | no | `grok_chat`, `email` |
| `pro` | Paid | 0 | 50 | yes | `grok_chat`, `email`, `webhook` |

All three include the time@mode strategy and the full ladder. `arbitrage` is false on every public plan until he sells it. `paper_trading` is true on all three so a free account can see simulated results, not a private tape. `trial_days` is 7 and `grace_days` is 3 on the paid plans. Both are fields.

Entitlement object:

| Key | Meaning |
| --- | --- |
| `symbol_limit` | Max enabled symbols on the user's watchlist. Null would mean unlimited. The seed does not use null |
| `timeframes` | Ladder names they may receive |
| `strategies` | `time_mode` for now |
| `signal_delay_seconds` | Added to `visible_at` at publication |
| `channels` | Which alert kinds may be enabled |
| `api_access` | User API keys |
| `paper_trading` | A personal paper account besides the house account |
| `arbitrage` | Arbitrage feed |

`require_entitlement` lives in `Core/entitlements.py` and is not wired yet. When it is, a miss returns 403 `entitlement_required` and writes an audit row. It does not silently downgrade a payload except for the publication delay, which is data, not an error.

Subscription states: `trialing`, `active`, `past_due`, `grace`, `canceled`, `incomplete`.

`past_due` starts at a failed invoice. After `grace_days` the state becomes `canceled` for entitlements and the role returns to `free`. Access during grace keeps the paid entitlements. The clock is on the subscription document.

## Payments

`Billing/modules/providers.py` is a protocol. `StripeProvider` is first. `CryptoProvider` is the second implementation, same subscription rows.

Stripe, when built:

- Checkout and the customer portal. Card numbers are never stored here.
- Webhook `POST /api/v1/billing/webhooks/stripe`. Verify the signature. Idempotency key is the Stripe event id, unique on `payment_events`.
- Events that matter: `checkout.session.completed`, `invoice.paid`, `invoice.payment_failed`, `customer.subscription.updated`, `customer.subscription.deleted`.

Crypto, later, same table:

- An invoice with asset, address, amount, and confirmations required.
- A watcher marks the payment event `confirmed`. It does not move coins. The provider is still an adapter.

The skeleton lists plans and an empty subscription list. It does not mount the webhook.

## Generation versus publication

The worker writes the truth once, then fans it out.

1. Detection inserts `signals` and, in the same step, appends `signal_logs` before any outcome exists.
2. `Publications` reads the log row and each entitled user. It does not call the detector.
3. For each user it inserts `publications` with `visible_at = logged_at + plan.signal_delay_seconds`. Owner delay is 0.
4. Alerts for that user are created at `visible_at`, not at detection time. The feed query is `visible_at <= now` and `user_id` is the caller. The deployment key sees delay 0.

A lower tier never receives an early webhook and a late UI. The delay is on the publication row, and every channel reads that row.

Channels stay pluggable: `grok_chat` now, `webhook` and `email` on paid plans, Telegram and Discord as later `kind` values and notifier classes. A plan that does not list a kind cannot enable that channel.

## Performance and the rule against repainting

`signal_logs` is append-only.

| Field | Rule |
| --- | --- |
| `seq` | Integer, unique, assigned by the writer |
| `payload` | Canonical JSON of the signal at detection |
| `payload_hash` | SHA-256 of that JSON |
| `prev_hash` | Hash of the previous row. The first row uses 64 zero hex digits |
| `logged_at` | Server time, set by the database clock path, not by the candle time |

Candle time stays inside `payload`. `logged_at` is when the system committed. Updates to a log row are not part of the API. A correction is a new row with `corrects_seq`. Outcomes live in `outcomes` and reference `signal_log_id`. They never rewrite the log.

The detector already uses only closed candles. Publication and the outcome job must use candles that closed after `logged_at`. That is the look-ahead ban. A backtest that fills on the signal bar's close is labeled `backtest` and is not shown as forward performance.

Outcomes the worker records when later candles exist: `open`, `stopped`, `target_hit`, `exited`, `expired`. `r_multiple` is the close versus the planned stop distance. Win rate, average R, and max drawdown are aggregates over a declared sample. The public page shows the **house paper account** forward window only, with the backtest window beside it and labeled. They are not averaged together.

`GET /api/v1/public/performance` is unauthenticated when the public page exists. The skeleton returns the disclaimer and an empty sample so the route is real. It does not claim a track record.

## Paper trading

The house paper account is created in the personal-use phase and simulates every entry plan: fill at the planned entry, fees and slippage from `app_settings` key `paper` (seed `fee_bps` 10, `slippage_bps` 5, same shape as the arbitrage cost seed, separate document). Stops and targets use the risk profile attached to the plan.

`forward_started_at` on that account is the split. Fills before it are backtest imports. Fills at or after it are the forward test. The public page refuses to render a forward stat until that timestamp exists and at least one closed forward outcome exists. Until then the page says the record has not started.

Personal paper accounts are the same collection with `owner_user_id` set and `kind: personal`. They do not affect the public number.

## Exchange accounts (later)

Optional auto-execution is a later phase and stays off. The collection exists so the shape is not an afterthought.

- Store ciphertext, nonce, and `key_id` of the server key. The server key is `SECRETS_KEY` in the environment, not in Mongo.
- The user key must be trade-only. The connect flow asks for a key that cannot withdraw. The app cannot prove that for every venue, so the UI states the requirement and stores a `withdrawal_enabled` flag the user attests, default unknown, and execution refuses unless the flag is false.
- No route accepts a key in this pass. `GET /api/v1/exchange-accounts` is an empty page.

## Operations

| Topic | Plan |
| --- | --- |
| Rate limit | Per IP on auth routes, per API key on `/api/v1`. `Core/rate_limit.py` is the seam. Not enforced yet. A miss is 429 `rate_limited` |
| Audit | `audit_logs` for login, logout, key create and revoke, role change, subscription change, entitlement denial, account delete. Append-only |
| Observability | Request id on every response, structured logs, no secrets in logs. OpenTelemetry is the later export. No collector in this pass |
| Environments | Same as [environments.md](environments.md). Staging uses Stripe test mode and `PUBLIC_SIGNUP=false`. Production signup stays false until the legal gate is signed off |
| Retention | Signals and `signal_logs` are kept (they are the product record). Refresh tokens 30 days after expiry. Audit logs 24 months. Payment events 7 years as a bookkeeping default, not a tax opinion. Scan runs 90 days. Venue quotes 1 day. Paper fills are kept with the account |
| Privacy | Email, name, password hash. Export and delete under PIPEDA. Delete removes the account and keys, anonymizes publications to a deleted-user id, and keeps `signal_logs` and payment rows. If EU users appear, the same export and delete cover a GDPR request. The policy text is a later page, not this file |
| Disclaimer | On signup, on the performance page, and in the feed payload metadata. Text in `Core/planning_seeds.py` as `DISCLAIMER`. It says the output is not investment advice and that past or simulated results are not future results |

## Legal gate

Miguel is in Alberta, Canada. Selling trading signals to the public can raise securities, derivatives, and registration questions, including whether the activity is advising. This plan does not answer that.

Public signup and paid checkout stay off until a lawyer licensed for that question says otherwise and the decision is written down outside this repo. The roadmap calls that the launch gate. Nothing in the skeleton enables taking payment from the public.

## Product stages

These stages sit on top of the build phases in [roadmap.md](roadmap.md).

1. **Personal use.** Signup closed. Miguel is the owner. Detection, confluence, risk, the house paper account, and the Grok Bot feed.
2. **Paper track record.** The immutable log and the house account run forward from `forward_started_at`. The public page stays unpublished. Backtests are not mixed into the forward number.
3. **Private beta.** Invite-only accounts, Stripe test mode, delays and entitlements enforced, signup still closed to the internet.
4. **Public paid launch.** Blocked on the legal gate. Then `PUBLIC_SIGNUP=true`, live Stripe, the public performance page, and the disclaimer on every surface.
