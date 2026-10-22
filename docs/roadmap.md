# Roadmap

Phases are ordered so each one leaves a runnable system. Dates are not estimated. A phase is done when its checks pass, not when a branch is opened.

The behavior oracle through phase 4 is `prototype/`: `timemode.py`, `data.py`, `scan.py`, `validate.py`, and the recorded score in `validation_results.txt` (18 of 23 chart checks). Do not retune rules to chase the five misses unless Miguel answers the matching open question in [strategy-spec.md](strategy-spec.md).

## Phase 0 — Planning foundation (this branch)

- Docs, cursor rule, folder skeleton, FastAPI health route, stub domain routes.
- `development`, `staging`, and `production` branches exist from `main`.
- Prototype copied under `prototype/` and not imported by the app.

Done when `/health` returns `status: ok` and the docs describe the domains, collections, and endpoints.

## Phase 1 — Port the scanner

Move detection and fetching behind the domains without changing results.

- `Repositories/Strategies/TimeMode` gets the pure functions from `prototype/timemode.py` (`atr_rma`, `sma`, `detect_modes`, `detect_blocks`, `params_for`).
- `Repositories/Exchanges` and `Repositories/MarketData` get the fallback fetch from `prototype/data.py`. Fix the OKX symbol mapping so non-USDT pairs (ETHBTC, ARBBTC) are not rewritten to `*-USDT`. Binance and Bybit already use the symbol as given.
- Worker loop: read the default watchlist and active strategy config (seed them from `prototype/config.json` on empty collections), fetch closed candles, detect, upsert `signals` by `signal_id`, write a `scan_runs` document.
- Delete the `state.json` path. Uniqueness is the index.
- Connect Mongo on API and worker startup. `/health` pings it.
- Replay `prototype/validate.py` cases through the ported functions. Score must stay at least 18/23 on the same checks. Check in a test that does not depend on a live exchange if fixtures are captured; until then the network replay can be marked manual.
- APScheduler in the worker at `SCAN_INTERVAL_SECONDS`. `--once` runs a single pass.

Exit rule: a `--once` scan against live or fixture data inserts signals, a second `--once` inserts zero new rows, and the replay score does not drop.

## Phase 2 — Read and manage API

Replace the empty list stubs with `build_query`.

- Implement `Core.mongo_orm.build_query` for the operators in the architecture doc, with tests against a Mongo instance or a disposable container.
- Signals list, get, and status patch.
- Watchlist CRUD.
- `PUT /strategies/time-mode` versions the config.
- `POST /scanner/runs` records a scan run the worker picks up (a `queued` scan run is enough; no second queue).
- Remove `Core.prototype_config` once seeding and the PUT path cover it.
- API key required in the staging environment.

## Phase 3 — Alerts

- `alert_channels` CRUD, URL masked on list.
- `WebhookNotifier` posts the signal JSON. Timeouts and non-2xx become `failed` with `last_error`.
- Unique `(signal_id, channel_id)` so a re-scan does not double-send.
- Test-send and retry endpoints.
- The notifier registry stays the only place that knows `kind`.

## Phase 4 — Backtests

- `POST /backtests` runs the same pure functions over a closed-candle range and writes `backtest_events`.
- The 23 chart checks become the first fixture backtest, with the five known misses asserted as misses so a "fix" shows up in review.
- Summary is signal counts, not PnL. No stops and no size are invented here.
- Candle cache fills as a side effect when it saves requests. Correctness does not depend on the cache.

## Phase 5 — Futures

Blocked on Miguel for stop placement, size, and which contract type (USDT-M, coin-M, hedge mode). The domain folder already exists.

- Futures klines on the same fallback idea, behind `market: "futures"`.
- Run the same time@mode functions. Do not fork the rules.
- `positions` registered and exposed. A position opens on `block_breakout_entry` and closes on `exit` only if he wants the bot to track positions. Until then, signals stay signals.

## Phase 6 — Arbitrage

Blocked on a written rule set. The folder stays empty of logic. No spread math, no exchange transfer assumptions, and no default strategy "to have something". When rules exist they get a strategy spec of the same kind as time@mode, then a module, then routes.

## Phase 7 — A simple UI

A separate client that talks to this API. It is not a domain under `Repositories/`.

- Show the signal list, the TradingView link, watchlist edit, and strategy params.
- No new detection rules in the UI.
- CORS and auth for a browser are decided here, not before.

## Explicitly out of scope until a later decision

- Order routing or placing trades.
- Stop-loss and position size (no chart shows a stop).
- R.E.Signal V3.3 and the blue/grey markers.
- Multi-user accounts and verifik-style client scoping.
- A message bus.

## Suggested PR slicing

One PR per phase is too big for phase 1. A workable split:

1. Pure port of `timemode.py` plus unit tests with captured candles, no I/O.
2. Exchange fetch behind MarketData, including the OKX symbol fix, with recorded HTTP fixtures.
3. Mongo signal upsert and the worker `--once` path.
4. Replay test wired into CI once fixtures exist.

Phases 2 and 3 can follow the same "read path, then write path" split.
