# Crypto Signals SaaS: Competitive & Best-Practice Research

**Prepared for:** Miguel Trevino, crypto-signals-with-grok-bot (time@mode strategy: spot, futures, arbitrage)
**Stack context:** Python, FastAPI, MongoDB, verifik-style `Repositories/` + `Core/` architecture
**Research date:** Oct 22, 2026 (prices checked that day; they change often, so re-check before pricing decisions)
**Method:** web search plus direct fetches of vendor pricing pages, docs, and regulator publications. Every price below comes from a cited page. Where I could only see a figure in a search-engine summary and not on the page itself, it's marked **(unverified)**.

> **Not legal advice.** Section 3 summarizes public regulator material so you can brief a securities lawyer. It is not a legal opinion.

---

## 0. TL;DR

1. **The market splits three ways:** (a) **bot/execution platforms** that monetize tooling, priced at roughly $20–$140/mo (3Commas, Cryptohopper, WunderTrading, Altrady, Coinrule, Cornix); (b) **signal marketplaces** that take a 30–50% revenue share from signal sellers (3Commas 30%, Cryptohopper 30% or 15% exclusive, Collective2 50% or 40%); (c) **specialist data/arbitrage tools** at $29–$795/mo (CoinGlass API, ArbitrageScanner).
2. **Trust is the moat.** Collective2's whole pitch is a forward-only, timestamped, losses-included record with no edits or backfills. Telegram VIP groups are the opposite (screenshots, cherry-picked take-profit targets), and regulators explicitly flag "AI trading signals" as a fraud red flag. An **immutable, publicly auditable signal log** is the #1 feature to build from day one.
3. **Delivery norm:** web app + Telegram + webhook (for 3Commas/Cornix/WunderTrading/Altrady signal bots) + email. Most bot platforms accept TradingView-style webhooks, so a **signed outbound webhook** gives you auto-execution without holding user exchange keys.
4. **Compliance headline (Alberta/Canada):** selling buy/sell signals for money, regularly, is "advising" under securities law *if* the instruments are securities or derivatives. Crypto perps/futures are derivatives, and spot crypto can be caught depending on how it's traded. The **general-advice exemption (NI 31-103 s. 8.25)** can cover **non-tailored** signals sent identically to all subscribers, with conflict disclosure. **Tailored advice, copy-trading links, or auto-trading on users' behalf likely require registration**, and **a disclaimer alone does not avoid registration** (CSA/CIRO SN 31-369). Get a securities lawyer before the public launch.
5. **Recommended model:** Free (delayed, limited pairs, public track record) → Starter → Pro (all pairs/timeframes, webhooks/API) → Arbitrage add-on/tier. No auto-execution with custody of user keys in v1. Integrate via webhooks to the user's own bot platform instead.

---

## 1. Competitor landscape

### 1.1 Summary table

| Product | What they sell | Pricing seen (USD unless noted) | Delivery | Performance display | Trial / freemium |
|---|---|---|---|---|---|
| **3Commas** | Bot platform (DCA/Grid/Signal bots), Pine Script execution, plus a **Signal Marketplace** | Starter $20/mo ($15/mo annual); Pro $50 ($38 annual); Expert $140 ($105 annual). Price rise in May 2026 from $15/$40/$110 | Web/mobile app, webhooks ("Webhook execution" on all plans), exchange auto-execution on 9 exchanges, Developer API (Expert) | Bot stats; marketplace signal pages | No free plan (removed Jun 2026 per comparedge); "Try for free" + demo account |
| **3Commas Signal Marketplace** | Third-party signal subscriptions that drive 3Commas bots | Seller-set price; **3Commas keeps 30%, provider gets 70%**, paid in USDC | Signals trigger subscribers' bots | Marketplace ranking favors new, discounted, or exclusive signals | Seller may offer discounts or free |
| **Cryptohopper** | Bot platform plus **Marketplace** (signals, strategies, templates, copy bots) | Explorer $29/mo ($24.16 annual); Adventurer $69 ($57.50); Hero $129 ($107.50); ex-VAT | Web/app, exchange auto-execution (16+ exchanges), signals from "Signalers" | Backtesting, paper trading; seller profile must include trading history | 3-day free Explorer trial; free "Pioneer" tier retired Jun 18, 2026 |
| **Cryptohopper Marketplace (sellers)** | Signal/strategy subscriptions | **30% commission**, **15% if exclusive**; seller must not take direct payments | In-platform | Seller "Profile Information" incl. past performance | — |
| **Cornix** | Telegram/Discord **signal-group auto-trading**, plus DCA/Grid/TradingView bots | Advanced $32.99/mo; Premium $52.99/mo; ~33% off annual; Asset Manager "from $99.90/mo"; white-label Community Admin "from $146.90/mo" | Telegram bot, web, mobile apps; auto-executes posted signals on users' own exchange accounts | Channel marketplace with reviews, scores and stats; "results when targets are hit in real time" | 14-day Premium trial, no card; **free for channel admins**; free plan closed to new users Feb 18, 2026 |
| **WunderTrading** | Signal/DCA/Grid bots, TradingView automation, spread & arbitrage tools, copy trading | Free $0; Basic $19.95; Pro $39.95; Premium $89.95 (up to 25% off annual). Prices from the vendor's own journal articles, since the pricing page renders them dynamically | Webhooks, API & MCP, Telegram notifications (Pump Screener), exchange execution on 18+ exchanges | Backtesting, optimiser | Lifetime Free plan; 7-day Pro trial, no card; crypto payments (no auto-renew) |
| **Altrady** | Multi-exchange terminal, signal/grid bots, scanners, alerts | Basic €28/mo (€20/mo annual). Essential €50/Premium €90 per search summary **(unverified)**. TA Scanner Pro add-on €21/mo | Web app, price/trend-line alerts, signal bots accepting Altrady signals, TradingView alerts or custom webhooks; MCP server | Trading journal: win rate, avg profit, drawdown | 5-day trial, no card; 30-day money-back |
| **Coinrule** | Rule/AI-agent automated trading | Free (paper only); Investor $29.99/mo ($265.99/yr); Trader $59.99 ($532.99/yr); Pro $675 ($5,994/yr); Enterprise custom. Credit overage $0.02/credit; billed via **Stripe** | Exchange auto-execution | Backtests (Investor: 5 lifetime runs) | Free tier, paper only |
| **LuxAlgo** | Indicators/toolkits (incl. on TradingView), AI "Quant" coding agent, Orderflow, strategy alerts | Free $0; Essential $39.99/mo ($24.99 annual); Premium $67.99 ($39.99); Ultimate $119.99 ($59.99); AI Ultra $229.99 ($119.99). Promo prices shown lower on site | Platform + TradingView; **webhook automation from Premium**; strategy alerts 5/50/100/200/500 by tier | Strategy Screener, backtests | Free forever; 30-day money-back on first payment |
| **TradingView invite-only scripts** | Paid access to closed-source indicators/strategies + alerts/webhooks | Vendor-set. **From Nov 1, 2026, selling invite-only access outside the TradingView Marketplace is banned**; vendors must move to the Marketplace. TradingView plan prices are geo/promo dependent (CA page showed "special price" C$19.95 / 41.95 / 82.95 / 279.92 per month for Essential/Plus/Premium/Ultimate) | TradingView alerts → webhook/email/app | Moderated per House Rules; TV recommends users ask for a real-account track record | Vendor-defined |
| **Collective2** | Marketplace of **tracked strategies**, auto-trade in subscriber's own brokerage account (stocks/futures/forex, not crypto-native) | Manager sets price; FAQ: practical "sweet spot" ~$49–$199/mo, cap $1,000 (per search summary); fees typically $20–$200+/mo; **C2 takes 50% (40% if "Trades Own Strategy")**; AutoTrade $49/mo | Web, API, email, broker auto-trade | **Forward-only, timestamped, losses included, no edits or backfill**; equity incl. fees; max drawdown; follower fills feed the record | — |
| **Telegram VIP signal groups** | Paid private channels | Anecdotal: 0.02 BTC/mo average subscription (2018 TakeProfit press release, self-interested source); other quoted prices from review/scam-report sites are **unverified** | Telegram | Typically screenshots, multiple TP targets reported as max gain; no verified history (per same release) | Free "teaser" channel → paid VIP |
| **ArbitrageScanner.io** | CEX/DEX spread scanner, perps/funding arbitrage, wallet analytics, education | $99/mo (Test), Business $195/mo, Platinum $397/mo, Enterprise $795/mo (range from FAQ); temporary GURU $1,199/6 mo, VIP $2,999/12 mo, Whale $9,990/15 mo | Web + **Telegram** screener, notifications | "Video cases"; wallet ROI/win-rate filters | 24-hour trial; crypto-only payments (USDT TRC-20/BEP-20, Crypto Cloud); 50% recurring referral |
| **CoinGlass API** | Derivatives data (funding, OI, liquidations, order book) | Hobbyist $29/mo ($348/yr); Startup $79/mo ($948/yr); Standard $299 and Professional $699 per search summary **(Standard/Pro unverified on page)**. Hobbyist/Startup = personal use only | REST API (30 req/min on Hobbyist) | n/a (data vendor) | — |

### 1.2 Sources per competitor
- 3Commas pricing: https://3commas.io/pricing ; help center plan table: https://help.3commas.io/tr/articles/8420093-mevcut-abonelik-planlari ; price history: https://comparedge.com/tools/3commas/changelog ; plan change post: https://3commas.io/blog/were-improving-our-subscription-plans
- 3Commas Signal Provider terms (70/30, USDC payouts, ranking, scam/leak bans): https://3commas.io/terms-and-conditions-for-marketplace-signallers ; marketplace page: https://3commas.io/crypto-signals
- Cryptohopper pricing: https://www.cryptohopper.com/pricing ; Pioneer retirement: https://www.cryptohopper.com/blog/the-pioneer-plan-is-moving-to-explorer-what-you-need-to-know-13114 ; seller T&Cs (30%/15%): https://docs.cryptohopper.com/docs/sellers/terms-and-conditions
- Cornix pricing: https://cornix.io/pricing/ ; plans: https://help.cornix.io/en/articles/5814828-cornix-subscription-plans ; admin onboarding (free for admins): https://help.cornix.io/en/articles/11657514-admin-onboarding ; signal integration: https://cornix.io/features/signal-integration/
- WunderTrading pricing: https://wundertrading.com/en/pricing ; prices cross-checked: https://roistreet.com/reviews/wundertrading and https://rewardio.com/wundertrading-pricing/
- Altrady pricing: https://www.altrady.com/pricing
- Coinrule plans: https://cloud.coinrule.com/docs/billing/plans-overview
- LuxAlgo plans: https://docs.luxalgo.com/llms-full.txt (Plans section), https://www.luxalgo.com/pricing/ , FAQ https://docs.luxalgo.com/platform/getting-started/faq
- TradingView Marketplace change: https://www.tradingview.com/blog/en/commercial-scripts-move-to-marketplace-61291/ ; vendor requirements: https://www.tradingview.com/support/solutions/43000549951-vendor-requirements/ ; invite-only guidance: https://www.tradingview.com/support/solutions/43000614617-publishing-invite-only-scripts/ ; pricing: https://www.tradingview.com/pricing/
- Collective2: https://trade.collective2.com/strategy-managers.html ; payout: https://support.collective2.com/hc/en-us/articles/203081490-How-much-do-I-get-paid ; pricing guidance: https://support.collective2.com/hc/en-us/articles/226592327-How-much-should-I-charge-my-subscribers
- Telegram VIP (anecdotal): https://www.einpresswire.com/article/433098241/research-paid-telegram-channels-with-tracking-signals-yield-a-negative-profitability ; pump-and-dump research: https://arxiv.org/html/2105.00733v2
- ArbitrageScanner: https://arbitragescanner.io/plans
- CoinGlass: https://www.coinglass.com/pricing

### 1.3 Patterns worth copying
- **Tier levers competitors actually use:** number of coins/pairs (Cryptohopper 15/50/75), scan interval or latency (Cryptohopper 10/5/2-min), number of alerts (LuxAlgo 5→500), active bots, number of exchange accounts (3Commas 1/5/25), history depth (LuxAlgo, CoinGlass), **webhook access gated to mid tier** (LuxAlgo Premium), API at top tier (3Commas Expert), commercial-use rights (CoinGlass).
- **Annual discounts of 17–50%** are universal (Cryptohopper 17%, WunderTrading up to 25%, Coinrule ~26%, Altrady 30%, Cornix ~33%, LuxAlgo 40–50%).
- **Trials:** 3–14 days, often no card (Cornix 14d, WunderTrading 7d, Altrady 5d, Cryptohopper 3d, ArbitrageScanner 24h). Several vendors **killed their free tiers in 2026** (3Commas, Cryptohopper Pioneer, Cornix for new users), while others keep a permanent free tier (WunderTrading, LuxAlgo, Coinrule paper-only).
- **Crypto payments are offered but don't auto-renew** (Cornix, WunderTrading, 3Commas). Plan for manual crypto renewals.
- **Signal distribution via other people's execution engines:** Cornix is free for channel admins and subscribers pay Cornix for execution. 3Commas, WunderTrading and Altrady signal bots accept webhooks/TradingView alerts. You can piggy-back on these instead of building execution.
- **Delayed free signals** are a common freemium lever among smaller signal products (examples from search: 5 min, 15 min, 30 s, 1 h delays). These are small vendors, so I'm citing them only as illustrations: https://www.smartflowsignals.com/ , https://app.alphaalert.app/pricing , https://leadedge.dev/ , https://prescience.markets/pro

---

## 2. Best practices for a signal SaaS

### 2.1 Verifiable, auditable performance (the core differentiator)
- **Forward-only, timestamped, losses included, no edits or backfill.** This is Collective2's stated model ("Every buy and sell is timestamped as it happens... Nothing is backfilled, nothing is edited, and nothing is quietly deleted"), and even when a strategy goes private the record keeps running. Source: https://trade.collective2.com/strategy-managers.html
- **Publish methodology for stats:** Collective2 documents its assumptions (reinvestment, starting capital, fees included, peak-to-valley max drawdown). Source: https://support.collective2.com/hc/en-us/articles/203081490-How-much-do-I-get-paid
- **Avoid "max TP" reporting:** a common Telegram trick is quoting the furthest take-profit as the result (TakeProfit 2018 release above). Report realized R-multiple per signal using a pre-declared exit rule.
- **Implementation for this project:**
  - `signals` collection is **append-only**. Give the app's MongoDB user a custom role with `insert`/`find` only on `signals` (no `update`/`remove`). Outcomes go into a separate `signal_outcomes` collection that references the signal.
  - Each signal stores: `created_at` (server UTC), `candle_close_time` that triggered it, the full rule inputs (mode level, ATR, SMA70-6h value, timeframe stack), entry/stop/targets, `strategy_version` (git SHA), and **`hash = sha256(prev_hash + canonical_json(payload))`** forming a hash chain. Publish the chain head periodically (e.g., in the public Telegram channel or a public page) so anyone can detect edits. An external timestamping service (e.g., OpenTimestamps) is an option, but I didn't research it here.
  - Publish **every** signal to the public record (free tier sees it delayed). Never let a signal be "unpublished."
  - Stats: win rate, avg R, expectancy, profit factor, max drawdown, longest losing streak, exposure. Show them per timeframe and per pair, with fees/slippage assumptions stated.

### 2.2 No repainting, no look-ahead bias
- TradingView's own definition: repainting is when historical and realtime calculations behave differently. "Unacceptable" forms include **leaking future info into the past** and **using realtime intrabars to generate alerts/orders**. Fix: act only on **confirmed (closed) bars**, and for higher-timeframe data use only the **last confirmed HTF value** (`close[1]` with `lookahead_on` in Pine). Pivots detected N bars later must not be plotted or credited at the pivot bar. Sources: https://www.tradingview.com/pine-script-docs/concepts/repainting/ , https://www.tradingview.com/pine-script-docs/concepts/other-timeframes-and-data/
- **Direct implications for time@mode:**
  - Swing highs/lows ("no new high for 5 bars") are only known **5 bars later**. The signal timestamp must be the detection bar, not the pivot bar.
  - Multi-timeframe confirmations (1W/3D/1D/6h SMA70) must use **only closed HTF candles** as of the entry-bar close. Don't use the forming weekly candle in backtests.
  - Mode expiry and "mode in control" re-evaluation must be computed with data available at the time. Store the snapshot of inputs on the signal so audits can replay it.
  - Exchange data revisions happen. Store the OHLCV used per signal (or its hash) so results are reproducible.
- **Backtest hygiene:** walk-forward / out-of-sample split, parameter changes (e.g., the 0.7 ATR threshold) versioned as `strategy_version`. Never re-score past live signals with new parameters; publish the backtest separately and label it hypothetical. Collective2 makes the same point: "Anyone can show off a backtest... A Collective2 record is different."

### 2.3 Multi-tenancy, plans and entitlements
- Shared-database, `tenant_id`/`user_id`-scoped multi-tenancy is enough for this product. Signals are global, and entitlements decide *who sees what and when*.
- **Entitlements as data, not code:** Stripe Billing Entitlements attaches "Features" to Products. Active subscriptions create active entitlements, and you sync them via the `entitlements.active_entitlement_summary.updated` webhook (payload lists at most 10; fetch the full list if `has_more`). Source: https://docs.stripe.com/billing/entitlements , https://docs.stripe.com/api/entitlements/active-entitlement
- Recommended entitlement keys (mirrored into Mongo `entitlements`): `signals.delay_seconds`, `signals.max_pairs`, `signals.timeframes[]`, `signals.markets[] (spot|futures)`, `channels[] (app|email|telegram|discord|webhook|api)`, `api.rate_limit_per_min`, `webhooks.max_endpoints`, `arbitrage.enabled`, `history.days`, `backtests.per_month`.
- **Gate at publish time, not only at read time.** The SignalPublishing service fans out per tier with `release_at = created_at + delay_seconds`, and API reads filter `release_at <= now` for the caller's tier. That way a free user can't fetch a real-time signal by hitting the API directly.

### 2.4 API keys, rate limiting, outbound webhooks
- Customer API keys: random 32+ byte tokens, **store only a hash** (show once), prefix for identification (e.g., `tm_live_…`), scopes, last-used, revoke/rotate. Rate-limit per key per entitlement (Redis token bucket, or `slowapi` for FastAPI). I didn't research specific library docs, so treat this as a design suggestion.
- Outbound webhooks to bots (3Commas/WunderTrading/Altrady/Cornix accept webhook or TradingView-style signals): HMAC-SHA256 signature header + timestamp + idempotency key, retries with exponential backoff, dead-letter queue, per-endpoint delivery log. Stripe's own model (signed webhooks, event IDs) is the reference pattern: https://docs.stripe.com/billing/subscriptions/webhooks
- Inbound billing webhooks (Stripe/BTCPay/NOWPayments): verify signatures, process idempotently by event ID, and treat them as the source of truth for subscription state.

### 2.5 Payments
| Provider | Facts found | Notes |
|---|---|---|
| **Stripe** (Canada) | Domestic cards **2.9% + C$0.30**; **Billing 0.7%** of billing volume (pay-as-you-go). https://stripe.com/en-ca/pricing , https://stripe.com/en-ca/billing/pricing | Subscriptions, trials, proration, Customer Portal, Entitlements, tax. Coinrule bills through Stripe. Check Stripe's restricted-businesses policy for "investment advice/signals" with Stripe before relying on it (not verified here). |
| **Coinbase Commerce** | Coinbase docs now describe **migrating from the Commerce Charge API to the Coinbase Business Checkouts API** (requires a Coinbase Business account). https://docs.cdp.coinbase.com/coinbase-business/checkout-apis/migrate-from-commerce/overview . A search summary says Commerce shut down Mar 31, 2026 and Coinbase Business is limited to US/Singapore merchants. **I couldn't load the help page to confirm (Cloudflare), so treat as unverified.** | Likely **not usable for a Canadian merchant**. Verify before planning on it. |
| **NOWPayments** | Recurring/subscription payments supported; standard fee **1% single-currency / 1.5% multi-currency** (per help center/search). https://nowpayments.io/crypto-subscriptions , https://nowpayments.zendesk.com/hc/en-us/articles/18143125295261-Fees | Custodial processor; email-invoice style renewals. |
| **BTCPay Server** | v2.3+ has **Subscriptions** (offerings, plans, trials, grace periods, prepaid credit for auto-renew) and an API. https://docs.btcpayserver.org/Subscriptions/ , https://blog.btcpayserver.org/btcpay-server-2-3-0/ | Self-hosted, non-custodial, no processor fee; you run the infra. |
- Competitor norm: crypto payments are **one-time/manual renewal** (Cornix, WunderTrading, 3Commas). Model `Subscription.renewal_mode = auto|manual` and send reminder notifications before expiry.

### 2.6 Security for user exchange API keys (only if/when you add execution)
- **Real-world failure:** in Dec 2022, 3Commas confirmed leaked files held valid API keys/secrets for ~100,000 users, linked to unauthorized trades. https://3commas.io/blog/notice-on-api-data-disclosure-incident , https://www.coindesk.com/tech/2022/12/28/anonymous-twitter-user-leaks-alleged-3commas-api-database , https://www.bleepingcomputer.com/news/security/crypto-platform-3commas-admits-hackers-stole-api-keys/
- **Exchange-side controls:** require **trade-only keys with withdrawals disabled**, **IP-whitelisted** to your static egress IPs. Binance requires an IP whitelist before withdrawals can be enabled, and `GET /sapi/v1/account/apiRestrictions` returns `enableWithdrawals` and `ipRestrict` so you can **verify on connect and reject keys with withdrawal rights**. https://www.binance.com/en/support/faq/how-to-create-api-keys-on-binance-360002502072 , https://www.binance.com/en/blog/security/how-to-secure-your-api-keys-on-binance-5-tips-for-protecting-your-crypto-8638066848800196896
- **Storage:** envelope encryption with a KMS-held master key. MongoDB **CSFLE / Queryable Encryption** supports AWS KMS (and others). The CMK never reaches the app, wrapped data keys live in a key-vault collection, and the app IAM role is limited to `kms:Encrypt`/`kms:Decrypt` on that key. https://www.mongodb.com/docs/manual/core/queryable-encryption/fundamentals/kms-providers/ , https://www.mongodb.com/docs/manual/core/queryable-encryption/fundamentals/keys-key-vaults
- Isolate the execution worker (separate service/network, only component allowed to decrypt), never log secrets, rotate, audit every decrypt.
- **Better v1 alternative:** don't hold user keys at all. Send signed webhooks to the user's own 3Commas/WunderTrading/Altrady/Cornix bot. That also reduces regulatory exposure (Section 3).

---

## 3. Legal & compliance (Alberta / Canada). **Not legal advice.**

### 3.1 What the regulators say
- **Alberta Securities Act:** an "adviser" is in the business of advising in **securities or derivatives**. Section 75 requires registration to advise unless exempt (search summary of https://www.canlii.org/en/ab/laws/stat/rsa-2000-c-s-4/latest/rsa-2000-c-s-4.html , consistent with ASC guidance https://www.asc.ca/en/registrant-and-market-regulation/registrant-toolkit/getting-registered).
- **When crypto is in scope (ASC):** securities law applies where a security or **derivative** exists or is created. That includes crypto that meets the derivative definition, and platforms holding custody where the client only has a contractual claim (CSA SN 21-327). "In Canada, if securities or derivatives are being traded, registration as a dealer or advisor will typically be required." https://www.asc.ca/financial-innovation-in-the-capital-markets/crypto-assets-digital-assets
  - Practical read: **futures/perpetual signals are signals on derivatives.** Whether **spot** BTC/ETH signals are "advising in securities" is less clear-cut. The ASC says it **can't determine whether a given crypto is a security** and points you to a lawyer (https://www.asc.ca/en/registrant-and-market-regulation/registrant-toolkit/faqs).
- **CSA/CIRO Staff Notice 31-369 (Dec 11, 2025), finfluencer guidance,** directly relevant to paid signals: https://www.osc.ca/en/securities-law/instruments-rules-policies/3/31-369/joint-canadian-securities-administrators-and-canadian-investment-regulatory-organization-staff
  - Paid "buy and sell signals" delivered regularly = **advising** (Flora scenario).
  - **General-advice exemption (NI 31-103 s. 8.25):** no adviser registration if the advice is **not tailored** to the recipient's needs, but you **must disclose any financial or other interest** in what you recommend, clearly and up front. Generic "I may hold positions" disclaimers are "not sufficient."
  - Once Flora answers DMs with personalized advice, the exemption is lost and registration is needed.
  - **"There is no equivalent exemption for trading activity."** Facilitating **copy trading** (linking paying subscribers to replicate trades in their accounts), or sharing trading links while being paid by followers or the platform, can be "acts in furtherance of a trade" → **dealer registration**.
  - **"The registration requirement cannot be avoided by simply making a disclaimer."**
  - Register in every province where advice can be seen. For internet services that "likely means all of the provinces and territories." Ontario uses its own s. 34 OSA equivalent of 8.25.
  - AI/automated advice: the person behind the AI is responsible "as if they themselves had done it directly."
  - Misrepresentation and market-manipulation (pump-and-dump) prohibitions apply regardless of exemption. Note **Re Floreani, 2025 ABASC 41** (Alberta finfluencer sanctioned).
  - Nova Scotia's plain-language summary of the same exemption: https://nssc.novascotia.ca/before-you-invest/finfluencers-and-securities-laws-part-2-%E2%80%9Cgeneral-advice-exemption%E2%80%9D
- **Auto-trading / discretionary management:** managing client accounts under discretionary authority is generally portfolio-manager activity (CIRO registration categories: https://www.ciro.ca/office-investor/how-ciro-protects-investors/where-we-fit-canadian-securities-regulatory-framework/understanding-registration-categories). The IIAC (an industry association, **not a regulator**) states "Copy trading meets the definition of non-tailored advice. Firms offering copy trading services must register." https://cffim-fcmfi.ca/iiac-defining-non-tailored-advice-for-order-execution-only-channels/
- **Futures access for Canadians:** CSA terms for crypto trading platforms prohibit offering **margin or leverage** to Canadian clients (ASC page above; CSA SN 21-332 https://www.osc.ca/en/securities-law/instruments-rules-policies/2/21-332/csa-staff-notice-21-332-crypto-asset-trading-platforms-pre-registration-undertakings-changes). Binance, Bybit and OKX restricted/exited Canada in 2023 (e.g., https://decrypt.co/142945/bybit-announces-exit-from-canada , https://crypto.news/okx-to-stop-serving-and-accepting-users-from-canada/). **Futures signals marketed to Canadians point them at products they mostly can't legally access onshore.** Raise this with counsel. Consider geo-gating futures content.
- **Fraud context:** the ASC has warned about schemes using "AI-generated trading signals" and guaranteed returns (https://www.asc.ca/en/news-and-publications/news-releases/2026/02/17--investor-alert-asc-warns-public-about-suspected-investment-scheme-called-bg-wealth-sharing). Marketing must never promise returns.
- **Other jurisdictions (US, EU, etc.)** were **not researched**. A public launch accepting foreign subscribers needs separate review.

### 3.2 Product design choices that keep you nearer the general-advice exemption (discuss with counsel)
1. **Same signal to every subscriber in a tier.** No per-user advice, no DMs answering "should I buy X?"
2. **Stops and position sizing:** publish them as part of the **strategy's fixed rule** (e.g., stop at rule-defined level, "risk 1% of equity" as a stated rule). A per-user calculator driven by *the user's own inputs* resembles tools like Altrady's position-size calculator. Whether that counts as "tailoring" is a question for counsel.
3. **Conflict disclosure** shown with each signal when Miguel or the company holds or trades the same position (31-369 requires specific, prominent disclosure).
4. **No custody, no discretionary trading, no copy-trading links for payment** in v1. Webhooks to the user's own bot are user-configured automation; counsel should confirm this.
5. Track-record claims must be true, complete and not misleading. The immutable log supports this.
6. Typical disclaimers (seen on 3Commas, Collective2): not financial advice, no guarantee, past performance not indicative, risk of total loss, hypothetical results labeled. **They support, but don't replace, the exemption analysis.**
7. Record ToS/risk-disclosure acceptance per user with version and timestamp (`consents` collection).

---

## 4. Synthesis & recommendations

### 4.1 Positioning
"**Rule-based, multi-timeframe crypto signals with a tamper-evident public track record**," delivered wherever the trader already executes (Telegram, webhooks to 3Commas/WunderTrading/Altrady/Cornix, API). Compete on **trust and transparency**, not on bot tooling. Bot platforms are crowded and cheap ($20–$90/mo).

### 4.2 Recommended tier model (**prices are hypotheses**, anchored to competitor data above)
| Tier | Price hypothesis | Signals | Channels | Other |
|---|---|---|---|---|
| **Personal / Admin** | — | Everything, real time | All | Miguel only, during the personal phase |
| **Free** | $0 | **Delayed** (e.g., released after the next candle close or N hours; never real time), BTC/ETH spot only, 1D/1W | Web app + public Telegram channel | Full public track record (all signals, delayed) |
| **Starter** | ~$19–29/mo (bot platforms' entry tier is $20–33) | Real time on candle close, top ~20 USDT pairs, 1D/3D/1W, spot | App, Telegram, email | Stats per pair/timeframe |
| **Pro** | ~$49–79/mo (marketplace sweet spot $49–199) | All monitored pairs, 4h–1M, spot **+ futures** (geo-gated per counsel), rule-defined stops/targets | + **Signed webhooks** (bot integrations), Discord, **REST API** (rate-limited) | Backtest reports, CSV export |
| **Arbitrage (tier or add-on)** | ~$99+/mo (ArbitrageScanner starts $99, Business $195) | CEX↔CEX, CEX↔DEX spreads, funding-rate opportunities | App, Telegram, webhook | Higher API limits |
- 7–14-day trial of Pro, no card. Annual billing ~20–30% off. Stripe for cards plus BTCPay or NOWPayments for crypto (manual renewal).
- Later option: list on Cornix (free for admins) or 3Commas/Cryptohopper marketplaces as **distribution channels**. Note their 30% cut and Cryptohopper's exclusivity/non-compete clauses.

### 4.3 v1 public launch vs later
**v1 (public launch)**
- Auth (email + password/OAuth, 2FA), user profile, consents/ToS versions
- Plans + entitlements (Mongo, synced from Stripe), Stripe subscriptions + Customer Portal, trial
- time@mode engine on closed candles; append-only hash-chained `signals`; `signal_outcomes`
- SignalPublishing with per-tier delay and pair/timeframe gating
- Public track-record page + stats methodology page
- Notifications: in-app, Telegram bot, email
- Pairs/watchlist collection (USDT preferred), admin console
- Audit log, rate limiting, basic API keys (read-only signals API for Pro)
- Legal pages (ToS, risk disclosure, privacy, conflict disclosure) **after a lawyer's review**

**Later**
- Signed outbound webhooks presets for 3Commas/WunderTrading/Altrady/Cornix formats (could be v1.1)
- Discord, SMS
- Crypto payments (BTCPay/NOWPayments)
- Arbitrage scanner (CEX + DEX), funding-rate monitor
- Backtest reports per pair; walk-forward results page
- Affiliate/referral program (watch the 31-369 disclosure and referral rules)
- Exchange account connection + auto-execution (**only after legal sign-off**; KMS/CSFLE, trade-only keys, IP-whitelist verification)
- Marketplace listings, white-label

### 4.4 Architecture implications (verifik-style `Repositories/<Domain>/{routes,middlewares,controllers,modules,models,tests}` + `Core/`)
| Domain (Repository) | Responsibility | Key Mongo collections | Notes |
|---|---|---|---|
| **Users** | Profiles, preferences, locale/timezone, country (for geo-gating) | `users` | |
| **Auth** | Sessions/JWT, 2FA, OAuth, password reset | `auth_sessions`, `auth_tokens` | Middleware `require_auth`, `require_entitlement(key)` |
| **Plans** | Plan catalog, feature/limit definitions | `plans`, `features` | Mirrors Stripe Products/Features |
| **Entitlements** | Effective rights per user (delay, pairs, timeframes, channels, limits) | `entitlements` | Rebuilt from billing webhooks; cached |
| **Subscriptions / Billing** | Stripe customers/subscriptions, trials, crypto invoices, renewal mode | `subscriptions`, `invoices`, `payment_events` | Idempotent webhook handlers; event store |
| **Pairs / Markets** | Monitored symbols, exchanges, spot/futures, USDT preference | `pairs`, `exchanges` | Already decided in t9u |
| **MarketData** | OHLCV ingestion, closed-candle snapshots | `candles` (time-series) | Store the inputs used per signal |
| **Strategies (time@mode)** | Modes, trading blocks, SMA70-6h filter, ATR, TF-in-control | `strategy_versions`, `modes`, `trading_blocks` | Pure functions; versioned by git SHA |
| **RiskSettings** | Stop/position-sizing rule parameters (Mongo, per t9u) | `risk_settings` | Public rule-level defaults; per-user overrides = legal question |
| **Signals** | Append-only signal records, hash chain | `signals` (insert-only role), `signal_chain_heads` | Never update; corrections are new events |
| **SignalPublishing** | Fan-out per tier, `release_at = created_at + delay`, gating | `signal_deliveries` | Workers/queue; API reads filter by `release_at` |
| **PerformanceTracking** | Outcomes, R-multiples, stats, drawdown, public record | `signal_outcomes`, `performance_snapshots` | Methodology versioned; recompute from raw |
| **Notifications** | Channels: app, email, Telegram, Discord, webhook | `notification_channels`, `notification_logs` | Channel availability via entitlements |
| **Webhooks (outbound)** | Endpoints, HMAC secrets, retries, DLQ, delivery logs | `webhook_endpoints`, `webhook_deliveries` | Bot-format templates |
| **ApiKeys** | Customer API keys (hashed), scopes, rate limits | `api_keys`, `api_usage` | Rate-limit middleware |
| **Arbitrage** (later) | CEX/DEX spread & funding scanners | `arb_opportunities` | Separate worker |
| **ExchangeAccounts** (later) | Encrypted trade-only keys, permission verification | `exchange_accounts` (CSFLE fields) | Isolated execution service |
| **Compliance** | Consents, ToS/risk-disclosure versions, conflict disclosures, geo rules | `consents`, `disclosures`, `geo_rules` | Disclosure attached to each signal |
| **AuditLog** | Who did what (admin edits, plan changes, key decrypts) | `audit_logs` (append-only) | Core middleware writes it |
| **Admin** | Back office | — | Role-based |
| **Core/** | `mongo_orm.build_query`, settings, logging, rate limiter, crypto/KMS client, event bus, timezones | — | Shared |

---

## 5. Open items / couldn't verify
- Altrady Essential/Premium prices (only Basic €28/€20 was visible on the fetched page).
- CoinGlass Standard/Professional prices (only Hobbyist/Startup visible on the fetched page).
- TradingView USD plan list prices (page geo-served CAD "special prices").
- Coinbase Commerce shutdown date and Coinbase Business eligibility for Canadian merchants.
- Stripe's policy on signal/advice businesses (restricted-business list not checked).
- Telegram VIP group prices beyond one self-interested 2018 source.
- Non-Canadian regulation (US CFTC/SEC, EU MiCA, etc.) not researched.

---

## 6. How this maps onto the planned Repositories

This section is the project's reconciliation, not part of the vendor research. Prices in section 4.2 stay hypotheses. `price_cents` stays null.

The research lists more repository names than this codebase uses. The extra names are folded into domains that already exist, except Compliance and Webhooks, which are their own folders because the research's rules and the signed-webhook delivery path need a home. Nothing here is legal advice.

| Research name | This repo | Why |
| --- | --- | --- |
| Users | `Repositories/Users` | Same. `country` is on the user for the futures geo-gate. |
| Auth | `Repositories/Auth` | JWT and hashed API keys. Refresh tokens are the session store. 2FA and OAuth are later modules in Auth, not new domains. Key prefix stays `cs_live_`. |
| Plans | `Repositories/Billing` collection `plans` | The catalog lives with billing so Stripe products and Mongo plans are one module. |
| Entitlements | `Repositories/Billing` collection `entitlements` | Effective rights per user, rebuilt from Stripe's entitlements webhook. Not a separate folder. |
| Subscriptions / Billing | `Repositories/Billing` | Stripe, BTCPay Server, and NOWPayments. `renewal_mode` is `auto` for cards and `manual` for crypto. |
| Pairs / Markets | `Repositories/Symbols` and `Repositories/Exchanges` | Already named. Symbols are not renamed to `pairs`. |
| MarketData | `Repositories/MarketData` | The log stores a hash of the OHLCV used for that signal. |
| Strategies (time@mode) | `Repositories/Strategies/TimeMode` and `Strategies/Confluence` | `strategy_configs.version` plus a git SHA. Modes and blocks stay inside the signal payload. They are not their own collections. |
| RiskSettings | `Repositories/Risk` | The published stop and size are the strategy's fixed rule. A calculator that takes a user's own equity is the open tailoring question in Compliance. |
| Signals | `Repositories/Signals` plus `signal_logs` | `signals` is the working set and may be marked acknowledged. `signal_logs` is the insert-only hash chain. Outcomes are not written back onto either row. |
| SignalPublishing | `Repositories/Publications` | `release_at = created_at + delay`. Enforced when the row is written and again on every read. |
| PerformanceTracking | `Repositories/Performance` | `outcomes` is the research `signal_outcomes`. Snapshots are recomputed, not a second source of truth. |
| Notifications | `Repositories/Alerts` | In-chat feed, email, Telegram, Discord. Channel kinds, not a second domain. |
| Webhooks (outbound) | `Repositories/Webhooks` | Signed deliveries to the user's own bot. v1 does not hold exchange keys. |
| ApiKeys | `Repositories/Auth` | Hashed keys stay next to login. |
| Arbitrage | `Repositories/Arbitrage` | Already planned. The sellable switch is the Arbitrage add-on plan, not a rewrite. |
| ExchangeAccounts | `Repositories/ExchangeAccounts` | Later, and only after counsel. v1 has the schema and no key intake. |
| Compliance | `Repositories/Compliance` | Consents, conflict disclosures, Canada futures geo-rule. Not a legal opinion. |
| AuditLog | `Repositories/Audit` | Same. |
| Admin | No repository | `owner` and `admin` roles on the existing routes. |
| Core | `Core/` | Query helper, config, rate-limit seam. No event bus and no KMS client in v1. |
