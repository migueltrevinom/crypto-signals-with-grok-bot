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

`price_cents` is null. The research's dollar ranges are hypotheses in [competitive-analysis.md](competitive-analysis.md), not a price list. Currency placeholder is CAD because he is in Alberta. Stripe can charge another currency later without a schema change.

Plans and the effective entitlement copy are Mongo documents. Stripe Products and Features use the same lookup keys (`signals.delay_seconds`, and the rest). The webhook `entitlements.active_entitlement_summary.updated` rebuilds the user's `entitlements` row. If the payload sets `has_more`, the worker fetches the rest of the list. The catalog on `plans` is what we intend to sell. The `entitlements` row is what that user has right now. Reads use the row, not a hardcoded tier.

| Code | Kind | Delay | What they receive | Channels |
| --- | --- | --- | --- | --- |
| `free` | base | 14400 seconds (4 hours; the seed for "N hours") | BTCUSDT and ETHUSDT spot, `1d` and `1w` only | `grok_chat` |
| `starter` | base | 0, meaning the candle-close signal | Up to 20 USDT pairs, `1d`, `3d`, `1w`, spot | chat, email, Telegram |
| `pro` | base | 0 | All monitored pairs, `4h` through `1M`, spot and futures | those, plus Discord, signed webhooks, and the read API |
| `arbitrage` | add-on on starter or pro | 0 | CEX and DEX spread records | chat, Telegram, webhook |

`signals.max_pairs: null` on Pro means every enabled symbol, not a missing field. Futures on Pro are still withheld when Compliance says the viewer's country is Canada. That gate is not the plan document. Pro's trial seed is 14 days. Starter's is 7. Grace on paid plans and the add-on is 3 days. `paper_trading` is true on the three base plans. `arbitrage.enabled` is false on them and true only on the add-on.

Entitlement keys, also the Stripe feature lookup keys:

| Key | Meaning |
| --- | --- |
| `signals.delay_seconds` | Added to the log's `created_at` to get `release_at` |
| `signals.max_pairs` | Cap. Null means all enabled symbols |
| `signals.symbols` | Allow-list. Set on Free. Null means "up to the cap" |
| `signals.timeframes` | Ladder names they may receive |
| `signals.markets` | `spot` and, on Pro, `futures` |
| `channels` | Alert and webhook kinds they may turn on |
| `api.rate_limit_per_min` | 0 means no customer API |
| `webhooks.max_endpoints` | Signed outbound endpoints. 0 means none |
| `arbitrage.enabled` | The add-on |
| `history.days` | How far back a read may go. Null means the retained log |
| `backtests.per_month` | Quota |
| `paper_trading` | A personal paper account besides the house account |

`require_entitlement` lives in `Core/entitlements.py` and is not wired yet. When it is, a miss returns 403 `entitlement_required` and writes an audit row. It does not silently downgrade a payload except for the publication delay, which is data, not an error.

Subscription states: `trialing`, `active`, `past_due`, `grace`, `canceled`, `incomplete`.

`past_due` starts at a failed invoice. After `grace_days` the state becomes `canceled` for entitlements and the role returns to `free`. Access during grace keeps the paid entitlements. The clock is on the subscription document.

## Payments

`Billing/modules/providers.py` is a protocol with three adapters and the same subscription rows: `StripeProvider`, `BtcPayProvider`, and `NowPaymentsProvider`. Coinbase Commerce is not a planned adapter. The research could not confirm it is usable for a Canadian merchant.

Stripe, when built:

- Checkout and the customer portal. Card numbers are never stored here.
- Webhook `POST /api/v1/billing/webhooks/stripe`. Verify the signature. Idempotency key is the Stripe event id, unique on `payment_events`.
- Events that matter: `checkout.session.completed`, `invoice.paid`, `invoice.payment_failed`, `customer.subscription.updated`, `customer.subscription.deleted`, and `entitlements.active_entitlement_summary.updated`.
- `renewal_mode` on the subscription is `auto`.

Crypto is BTCPay Server (self-hosted, subscriptions, trials, grace) or NOWPayments (custodial, their subscription product). Both set `renewal_mode` to `manual`, because competitor crypto checkouts do not auto-renew. A reminder goes out before `current_period_end`. The same webhook idempotency rule applies. Stripe's restricted-business policy for signal products was not checked in the research. That check sits with the lawyer and with Stripe, before live cards.

The skeleton lists plans and an empty subscription list. It does not mount the webhook.

## Generation versus publication

The worker writes the truth once, then fans it out.

1. Detection inserts `signals` and, in the same step, appends `signal_logs` before any outcome exists. The log time is the triggering candle's close. A swing is dated to the bar that confirmed it, not the pivot bar.
2. `Publications` reads the log row and each entitled user. It does not call the detector.
3. For each user it inserts `publications` with `release_at = created_at + signals.delay_seconds`. Owner and admin delay is 0. A symbol, timeframe, or market the plan does not include is not fanned out (`suppressed`), not delayed.
4. Every read, including the feed, the API, and outbound webhooks, filters `release_at <= now`. A free client cannot fetch a real-time row by calling the API.

A lower tier never receives an early webhook and a late chat message. The delay is on the publication row, and every channel reads that row.

Channels stay pluggable. v1 delivery to a subscriber's own bot is a signed webhook (`Repositories/Webhooks`), not an exchange key. Telegram and Discord are later kinds. A plan that does not list a kind cannot enable that channel. The in-chat feed remains the first channel for Miguel.

## Performance and the rule against repainting

`signal_logs` is append-only.

| Field | Rule |
| --- | --- |
| `seq` | Integer, unique, assigned by the writer |
| `candle_close_time` | Close of the bar that triggered the signal. Swings are not stamped on the pivot bar. They are stamped on the confirming bar, which is 5 bars after the extreme |
| `payload` | Canonical JSON: sorted keys, UTF-8, no insignificant whitespace. Includes mode level, ATR, the 6h SMA value, the timeframe stack, entry, stop, targets, and `ohlcv_hash` of the candles used |
| `strategy_version` | Git SHA of the rules that fired, plus the `strategy_configs` version |
| `prev_hash` | Previous row's `chain_hash`. The first row uses 64 zero hex digits |
| `chain_hash` | SHA-256 of `prev_hash` concatenated with the canonical payload |
| `logged_at` | Server UTC when the row was inserted. `created_at` on the publication delay is this timestamp |

The Mongo user that writes `signal_logs` is granted insert and find, not update or delete. Corrections are a new row with `corrects_seq`. Outcomes live in `outcomes` and reference `signal_log_id`. They never rewrite the log. The working `signals` collection may still be marked acknowledged. It is not the audit chain.

Only closed candles are inputs. A higher timeframe is the last candle that had already closed at `candle_close_time`. The forming weekly bar is not an input in a backtest or in live detection. Publication and the outcome job use candles that closed after `logged_at`. A backtest that fills on the signal bar's close is labeled `backtest` and is not shown as forward performance. Changing the 0.7 ATR threshold versions the strategy. It does not re-score rows already in the log.

Outcomes the worker records when later candles exist: `open`, `stopped`, `target_hit`, `exited`, `expired`. `r_multiple` is the close versus the planned stop distance. Win rate, average R, and max drawdown are aggregates over a declared sample. The public page shows the **house paper account** forward window only, with the backtest window beside it and labeled. They are not averaged together.

`GET /api/v1/public/performance` is unauthenticated when the public page exists. The skeleton returns the disclaimer and an empty sample so the route is real. It does not claim a track record.

## Paper trading

The house paper account is created in the personal-use phase and simulates every entry plan: fill at the planned entry, fees and slippage from `app_settings` key `paper` (seed `fee_bps` 10, `slippage_bps` 5, same shape as the arbitrage cost seed, separate document). Stops and targets use the risk profile attached to the plan.

`forward_started_at` on that account is the split. Fills before it are backtest imports. Fills at or after it are the forward test. The public page refuses to render a forward stat until that timestamp exists and at least one closed forward outcome exists. Until then the page says the record has not started.

Personal paper accounts are the same collection with `owner_user_id` set and `kind: personal`. They do not affect the public number.

## Outbound webhooks, not exchange keys

v1 does not hold user exchange keys. A Pro subscriber registers an HTTPS endpoint. The worker POSTs the publication when `release_at` has passed, with an HMAC-SHA256 signature, a timestamp, and an idempotency key. Retries use exponential backoff. A dead letter is a `webhook_deliveries` row in `failed`, not a dropped signal. Presets for 3Commas, WunderTrading, Cornix, and Altrady are templates on that payload, not a reason to connect their exchange accounts.

`GET /api/v1/webhooks/endpoints` is an empty page. Creating an endpoint is specified and not mounted. The secret is shown once and stored as a hash.

## Exchange accounts (later)

Optional auto-execution stays off through the public launch unless counsel says otherwise. The collection exists so the shape is not an afterthought. The 3Commas API-key leak is why this is not v1.

- Store ciphertext, nonce, and `key_id`. The server key is `SECRETS_KEY` in the environment, or a KMS CMK if that phase chooses CSFLE. The key does not live in the document.
- Trade-only, withdrawals off, IP-allowlisted. Where the venue exposes it (Binance `apiRestrictions`), the connect flow reads `enableWithdrawals` and rejects the key when withdrawals are on.
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

## Compliance gate

This is not legal advice. `Repositories/Compliance` holds the product rules counsel has to review. `GET /api/v1/compliance/gate` returns that list and `legal_advice: false`.

Public material the research summarized, for the lawyer and not as a conclusion:

- CSA/CIRO Staff Notice 31-369 (11 Dec 2025). Paid buy and sell signals on a schedule are described there as advising. A disclaimer does not remove the registration requirement.
- The general-advice exemption in NI 31-103 section 8.25 can cover advice that is not tailored to the recipient, if conflicts are disclosed specifically and up front. Ontario has its own section 34 equivalent. Internet delivery may mean every province and territory.
- Copy-trading or auto-trading a subscriber's account for payment is discussed as trading activity, and the notice says there is no matching exemption for trading. v1 does not do it.
- Futures and perpetual signals are signals on derivatives. Spot is less clear. Futures content is geo-gated when `users.country` is `CA`, until counsel says otherwise.
- Whether a calculator that applies the fixed stop rule to a user's own equity is "tailoring" is an open question for that lawyer. Until they answer, the published signal carries the strategy's fixed stop and size rule, and the per-user calculator stays off the public API.

Consents store the ToS, risk disclosure, and conflict-disclosure version the user accepted, with a timestamp. Each public signal can carry the current conflict disclosure id. Marketing does not promise returns.

Public signup and live checkout stay off until that review is written down outside this repo.

## Product stages

These stages sit on top of the build phases in [roadmap.md](roadmap.md).

1. **Personal use.** Signup closed. Miguel is the owner. Detection, confluence, risk, the house paper account, and the Grok Bot feed.
2. **Paper track record.** The immutable log and the house account run forward from `forward_started_at`. The public page stays unpublished. Backtests are not mixed into the forward number.
3. **Private beta.** Invite-only accounts, Stripe test mode, delays and entitlements enforced, signup still closed to the internet.
4. **Public paid launch.** Blocked on the legal gate. Then `PUBLIC_SIGNUP=true`, live Stripe, the public performance page, and the disclaimer on every surface.
