# Roadmap

Phases are ordered so each one leaves a runnable system. Dates are not estimated. A phase is done when its checks pass.

The detector oracle is still `prototype/`: `timemode.py` and `validate.py`, score 18 of 23. Do not retune ATR or wick selection to chase the five misses. Do apply Miguel's resolved decisions on top of that oracle: 6h SMA, the new ladder, resampling, confluence, risk profiles, the symbols collection, the Grok Bot feed, and arbitrage records. Those are specified in [strategy-spec.md](strategy-spec.md) and [repositories.md](repositories.md).

## Phase 0 — Planning foundation

Docs, cursor rule, folder skeleton, health route, placeholder domain routes. This phase includes the update for Miguel's answers. Detection, sizing, and delivery are not implemented.

## Phase 1 — Port detection and candles

- Move `prototype/timemode.py` into `Strategies/TimeMode` without changing mode or block math, except the SMA filter reads the 6h series.
- Move fetching into Exchanges. Symbol mapping uses `concat`, `dash`, and `alias`. The OKX `*-USDT` slice is not ported.
- MarketData resamples missing ladder bars onto the Binance grid. A fixture test compares one week of native opens before a venue's native 3d, 6h, or 1M is trusted.
- `timeframe_in_control` is implemented as specified.
- Worker `--once` writes signals. Dedup is the `signal_id` index.
- Replay stays at least 18/23 on the mode checks. The three block/entry checks are re-run with the 6h SMA and the difference is recorded. 1h and 30m checks stay as detector tests, not as live entry timeframes.

## Phase 2 — Mongo settings and the read API

- Implement `build_query`.
- Seed `app_settings`, `strategy_configs`, `confluence_configs`, and the default `risk_profiles` row from `Core/planning_seeds.py`.
- Symbols API. A sync job can fill listings from public instrument endpoints. USDT is preferred, not exclusive.
- Users: one seeded account, still behind the shared API key.
- Watchlists point at symbol ids.
- Remove the runtime read of `prototype/config.json` once the seed exists. Keep the file as the replay oracle.

## Phase 3 — Confluence and entry plans

- `confluence_module.score` uses the seeded weights.
- Entry plans are stored. A second scan expires a plan whose trigger is gone and does not duplicate it.
- Unit fixtures cover: weekly and daily agree and 4h triggers; decision timeframes conflict and the penalty applies; SMA fails and the score is zero; no 1h entry is produced.

## Phase 4 — Risk and planned positions

- Resolve the most specific profile.
- Size with the formula in the repositories doc. Null equity yields a position with `size_base: null` and a clear alert payload.
- Worker writes `planned` positions and `position_events`.
- PATCH to `active` or `cancelled` works. Later candles move `stopped`, `target_hit`, and `exited` without sending an order.

## Phase 5 — Grok Bot alert feed

- Pending rows for entry plans, positions that need equity, and later arbitrage.
- `GET /alerts/feed` and `POST /alerts/{id}/ack`.
- Uniqueness stops a second row for the same subject and channel.
- Webhooks and email stay unimplemented.

## Phase 6 — Backtests

- Same functions as the live path, over a historical range.
- Summary includes signal counts, entry plans, and hypothetical R from the planned stop and targets.
- The 23 chart checks are a fixture. The five known misses stay misses.

## Phase 7 — Arbitrage detection

- CEX quotes from the enabled exchanges. DEX quotes from the enabled dex venues. Both start disabled where the connector does not exist yet.
- Net spread after fees, the flat slippage bps, and transfer or gas.
- Opportunities stored. Orders are not sent. `place_orders` stays false.
- An opportunity becomes a feed row.

## Phase 8 — Futures candles

Same detector, confluence, and risk path with `market: futures` and `max_leverage` from the profile. Blocked on the contract-type question (USDT-M, coin-M, hedge mode). No separate domain.

## Phase 9 — Webhooks and email

Implement the two notifier classes. Mask secrets. This is after the Grok Bot feed is in use.

## Phase 10 — A simple UI

A separate client. It reads the feed, the position list, and the settings. It is not a repository domain. CORS is decided here.

## Out of scope

- Submitting orders or swaps.
- R.E.Signal V3.3.
- Verifik-style multi-tenant client ids.
- A message bus. The bot polls.

## Suggested PR slicing

1. Pure port of detection, 6h SMA injected as a series, replay tests.
2. Symbol styles and resampling, with recorded HTTP fixtures.
3. `build_query` and the settings seed.
4. Confluence score tests, no I/O.
5. Risk formula tests, then position writes.
6. Alert feed.
7. Arbitrage net-spread tests with fixture quotes.
