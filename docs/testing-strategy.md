# Testing strategy

The default test run is `pytest` with no Mongo, no exchange network, and no API key. CI (`.github/workflows/test.yml`) runs that plus Ruff. A test that needs a service is opt-in and is not part of phase 0.

## What phase 0 covers

- `GET /health` returns `status: ok` and the skeleton fields.
- Each mounted list route returns the page envelope.
- `GET /strategies/time-mode` matches `prototype/config.json`.
- `GET /exchanges` follows `data_sources` order, Binance first.
- Protected routes return 401 when `APP_ENV=production` and the key is wrong, and 500 `server_misconfigured` when that environment has an empty key.
- Development with an empty key leaves the routes open.
- `build_query` raises `NotImplementedError` so a module cannot pretend reads work.
- `python -m app.worker --once` exits 0.
- Domain modules import, and the Signals module returns an empty page.

These tests lock the layout. They do not lock detection. Detection is not in the app yet.

## Layers once the port starts

### Pure rules

`detect_modes` and `detect_blocks` are functions of arrays and a params dict. Test them with candle fixtures, no clock and no network. Fixture files should be small JSON arrays of closed candles cut from the chart windows (ETHBTC daily Sep–Oct 2021, ETHBTC weekly spring 2021, ARBBTC Dec 2023, ETHUSDT Feb 2024).

Assert the 18 passing checks and assert the 5 misses still miss. A change that "fixes" a miss fails the test until the open question is resolved and the expected value is edited on purpose.

Also cover:

- The forming candle is not in the input the detector sees (that filter is in MarketData, tested there).
- ATR(14) RMA on ETHBTC daily around 4 Nov 2021 matches the chart legend value 0.002534 when the same series, including that partial candle, is used. The scanner itself drops the partial candle; the ATR identity check can include it the way the chart legend did.
- SMA 70 is a simple average. One hand-computed series is enough.
- `signal_id` is stable for a fixed payload, including the `.10g` level format.

### Market data

Record HTTP responses as fixtures. Tests replay them through the fetch parser. Assert closed-candle filtering, dedup, and sort. One test per source for the interval map (Bybit `1h` → `60`, OKX `6h` → `6Hutc`, and the ETHBTC inst id once the OKX map is fixed).

Do not call live Binance from CI. A manual `prototype/validate.py` remains available for a human with network.

### Mongo

Phase 2. Use a disposable Mongo (CI service container or testcontainers) for `build_query`: equality, comparison, `in_`, pagination envelope, sort, and a rejected populate. Keep the parser tests that do not need a server in the default run if the parser is split from execution.

Signal upsert: insert twice, count stays 1, `signals_new` on the second scan run is 0.

### API

`TestClient` over `app.main:app`. Override settings in a fixture (`get_settings.cache_clear()`). Do not boot uvicorn in the test.

Cover auth, the page envelope, 404 `not_found`, and 422 on a bad watchlist body. Domain errors use `{message, code}`.

### Worker

A `--once` test with fixture candles and a fake notifier. Assert the order of composition (fetch result passed into detect, detect result passed into upsert, only new ids passed into alerts) without importing modules from each other inside the test's production code. The worker test is allowed to call several modules; that is the composition root.

### Alerts

Webhook notifier against `httpx.MockTransport` or a local stub. Assert the payload is the signal, non-2xx marks `failed`, and a second scan does not create a second alert row.

### Backtests

The chart fixture suite is the first backtest. Summary counts must equal the pure-rule tests. Hypothetical R from the planned stop is labeled `hypothetical`. No filled-order PnL.

## What not to test

- Arbitrage net-spread math gets fixture tests in its phase: two quotes in, one net bps out. No test sends an order.
- Resampling tests lock Binance's 8h, 3d, weekly, and monthly open times.
- Confluence tests lock the seed weights: a conflicting weekly and daily score is penalized, a failed 6h SMA zeros the score, and no plan uses a 1h entry.
- Risk tests lock the size formula, including a null equity leaving `size_base` null.
- Alert tests lock `pending → delivered → acked` on the feed.
- Signup stays closed in tests. Plan prices stay null. The public performance route returns zero trades and does not require a key. The private track record does.
- Do not snapshot the entire FastAPI OpenAPI schema in phase 0. It will churn as routes are filled in.
- Do not require the prototype's live `validate.py` in CI. Historical exchange responses can move by a bar revision; fixtures will not.

## Where tests live

| Kind | Path |
| --- | --- |
| HTTP and settings | `tests/` |
| Core helpers | `Core/tests/` |
| A domain's module | `Repositories/<Domain>/tests/` |

The time@mode replay tests will live in `Repositories/Strategies/TimeMode/tests/` next to the ported functions.

## Failure policy

A red replay test blocks the PR. A new miss against the 18 is a bug. A newly passing miss is also a review item: it means a default changed, and the strategy spec has to change in the same PR with Miguel's answer cited.
