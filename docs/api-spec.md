# API specification

Base URL: `/api/v1`. Interactive schema: `/docs` (FastAPI). Health is outside the prefix so load balancers can call it without a version.

This pass serves the skeleton endpoints listed at the bottom. Every other endpoint is the contract for the phase that implements it. Skeleton list routes return an empty page and do not read Mongo.

## Conventions

- Auth: header `X-API-Key`. Required when `API_KEY` is set, and required whenever `APP_ENV` is not `development`. `/health` is public. `/docs` is public in development and should be disabled in production when the host is not private (deployment choice, still open).
- Times in JSON are ISO-8601 UTC, except `close_time_edmonton`, which is an ISO string with the Edmonton offset.
- Ids in JSON are strings.
- List envelope:

```json
{"data": [], "total": 0, "limit": 20, "page": 1, "pages": 0}
```

- Single resource: `{"data": {}}`.
- Update and delete: `{"data": {}, "status": "completed"}`.
- Domain errors: `{"message": "Signal not found", "code": "not_found"}` with HTTP 404, 409, 401, 403, or 503.
- Validation errors (bad query or body): HTTP 422 with FastAPI's `detail` array. Not rewritten into `{message, code}` in v1.
- Pagination: `page` starts at 1, `limit` defaults to 20, maximum 100.
- Sort: `sort=-close_time`. A leading `-` is descending. Default for signals is `-close_time`.
- Filters below are the public names. Modules translate them into `Core.mongo_orm.build_query` params (`where_symbol`, and so on). Clients do not send `where_`.

## Health and scanner

### `GET /health`

Public. Always implemented.

```json
{
  "status": "ok",
  "service": "crypto-signals-with-grok-bot",
  "environment": "development",
  "mongo": "not_connected",
  "scanner": "not_ported"
}
```

`mongo` becomes `ok` or `error` once the API pings the database. `scanner` becomes `idle` or `running` once the worker records a heartbeat. The planning skeleton always reports `not_connected` and `not_ported`.

### `GET /api/v1/scanner/status`

Skeleton, public-as-the-other-v1-routes (API key rules apply).

```json
{
  "data": {
    "status": "not_ported",
    "interval_seconds": 900,
    "last_run": null
  }
}
```

Later, `last_run` is the latest `scan_runs` document (id, status, started_at, finished_at, signals_new, errors).

### `POST /api/v1/scanner/runs`

Phase 2. Body (all optional):

```json
{"symbols": ["BTCUSDT"], "timeframes": ["1d"]}
```

Starts one scan. `202` with `{"data": {"id": "<scan_run id>", "status": "running"}}`. The worker performs it. This route does not run detection inside the web process.

## Signals

### `GET /api/v1/signals`

Query: `symbol`, `timeframe`, `type`, `direction`, `status`, `market`, `close_time_from`, `close_time_to`, `page`, `limit`, `sort`.

`close_time_from` / `close_time_to` are ISO datetimes or `YYYY-MM-DD` (UTC day bounds).

Response items are the stored signal with `details` flattened onto the object, plus `id` and `signal_id`. Example item, matching the prototype's JSON:

```json
{
  "id": "664f0b0c0b0c0b0c0b0c0b0c",
  "signal_id": "ab12cd34ef56ab78",
  "type": "mode_confirmed",
  "symbol": "ETHBTC",
  "timeframe": "1d",
  "direction": "bearish",
  "close_time": "2021-09-17T23:59:00+00:00",
  "close_time_edmonton": "2021-09-17T17:59:00-06:00",
  "price": 0.07186,
  "level": 0.07402,
  "level_kind": "mode",
  "atr": 0.003,
  "atr_distance": 0.72,
  "tradingview_url": "https://www.tradingview.com/chart/?symbol=BINANCE:ETHBTC&interval=1D",
  "mode_length": 8,
  "mode_anchor": "HL",
  "confirmations": ["atr_expansion"],
  "body_crosses_mode": true,
  "trend": "down",
  "strategy_key": "time_mode",
  "market": "spot",
  "status": "new"
}
```

The numbers above are illustrative. The oracle for real values is the scanner.

### `GET /api/v1/signals/{signal_id}`

`signal_id` is the 16-char hash, not the Mongo id. `404` `not_found` when absent.

### `PATCH /api/v1/signals/{signal_id}`

Body: `{"status": "acknowledged"}` or `dismissed` or `new`. Does not edit price or level.

## Watchlists

### `GET /api/v1/watchlists`

Page of watchlists.

### `POST /api/v1/watchlists`

```json
{
  "name": "main",
  "symbols": [{"symbol": "BTCUSDT", "exchange": "binance", "market": "spot"}],
  "timeframes": ["1h", "6h", "1d", "1w"],
  "ltf_map": {},
  "strategy_key": "time_mode",
  "alert_channel_ids": [],
  "enabled": true
}
```

`201` and `{"data": ...}`. Unknown `strategy_key` is 422.

### `GET /api/v1/watchlists/{id}`

### `PUT /api/v1/watchlists/{id}`

Replaces the mutable fields. Same body as create. `{"data": ..., "status": "completed"}`.

### `DELETE /api/v1/watchlists/{id}`

`{"data": ..., "status": "completed"}`. Does not delete historical signals.

## Strategy parameters

### `GET /api/v1/strategies/time-mode`

The active `time_mode` config. Skeleton behavior (implemented now): reads `prototype/config.json` and returns it unsaved.

```json
{
  "data": {
    "id": null,
    "key": "time_mode",
    "version": 0,
    "active": true,
    "persisted": false,
    "source": "prototype/config.json",
    "params": {},
    "scanner": {
      "history_bars": 1000,
      "report_window_bars": 3,
      "data_sources": ["binance", "binance_vision", "bybit", "okx"],
      "ltf_map": {"1w": "1d", "1d": "6h", "6h": "1h", "1h": "15m"},
      "state_retention_days": 120
    },
    "symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT", "ARBUSDT"],
    "timeframes": ["1h", "6h", "1d", "1w"]
  }
}
```

`persisted`, `source`, `symbols`, and `timeframes` are skeleton fields. `symbols` and `timeframes` move to the default watchlist once seeding exists. `persisted` and `source` go away. `version` becomes `1` on the seeded document.

### `PUT /api/v1/strategies/time-mode`

Phase 2. Body is `{"params": {...}, "scanner": {...}, "notes": ""}`. Validates against the known param keys and types. Writes a new version, sets it active, leaves the previous version stored. `200` with the new document.

Unknown param keys are 422. The port does not silently ignore a typo in `confirm_atr_mult`.

## Market data

### `GET /api/v1/market-data/candles`

Query required: `symbol`, `timeframe`. Optional: `exchange` (default `binance`), `limit` (default 200, max 1000), `end`.

Phase 1 may proxy a live fetch (closed candles only) even before the cache is filled. Response envelope `data` is an array of `{open_time, close_time, open, high, low, close, volume}`.

The skeleton returns an empty page.

## Exchanges

### `GET /api/v1/exchanges`

Ordered kline sources. Skeleton: built from `prototype/config.json` `data_sources` plus the base URLs in `prototype/data.py`. Not persisted.

```json
{
  "data": [
    {
      "name": "binance",
      "priority": 1,
      "kind": "spot_klines",
      "base_url": "https://api.binance.com",
      "market": "spot",
      "enabled": true,
      "auth": "none"
    }
  ]
}
```

### `PUT /api/v1/exchanges/{name}`

Phase 2. Toggle `enabled` and `priority`. Cannot create an unknown source name until a fetcher exists for it.

## Alerts

### `GET /api/v1/alert-channels`

### `POST /api/v1/alert-channels`

```json
{
  "name": "miguel",
  "kind": "webhook",
  "enabled": true,
  "config": {"url": "https://example.com/hooks/signals", "headers": {}}
}
```

The response masks `config.url` to the scheme and host, and drops `headers`. `GET` one channel for editing can return the full config; list responses stay masked.

### `GET /api/v1/alert-channels/{id}`

### `PUT /api/v1/alert-channels/{id}`

### `DELETE /api/v1/alert-channels/{id}`

### `POST /api/v1/alert-channels/{id}/test`

Sends a fake payload `{"type": "test"}` through that channel's notifier. `200` `{"data": {"status": "sent"}}` or `502` `{"message": "...", "code": "delivery_failed"}`.

### `GET /api/v1/alerts`

Query: `signal_id`, `channel_id`, `status`, `page`, `limit`.

### `POST /api/v1/alerts/{id}/retry`

Sets `pending` and asks the worker to send again. `202`.

## Backtests

### `POST /api/v1/backtests`

```json
{
  "name": "ethbtc 2021",
  "symbols": ["ETHBTC"],
  "timeframes": ["1d", "1w"],
  "start": "2021-01-01",
  "end": "2021-12-31",
  "strategy_version": null
}
```

`strategy_version` null means the active config, snapshotted onto the backtest at start. `202` with the queued document.

### `GET /api/v1/backtests`

### `GET /api/v1/backtests/{id}`

Includes `summary`. Does not inline every event.

### `GET /api/v1/backtests/{id}/events`

Paged `backtest_events`, filters `type`, `symbol`, `timeframe`.

## Futures and arbitrage

No routes in the skeleton. When those phases start:

- `GET/POST /api/v1/positions` for futures positions
- `GET /api/v1/arbitrage/opportunities` once a rule set exists

Do not add the routes before the rules exist.

## Implemented in this planning skeleton

| Method | Path | Behavior |
| --- | --- | --- |
| GET | `/health` | Live status object |
| GET | `/api/v1/scanner/status` | `not_ported` |
| GET | `/api/v1/signals` | Empty page |
| GET | `/api/v1/watchlists` | Empty page |
| GET | `/api/v1/backtests` | Empty page |
| GET | `/api/v1/alerts` | Empty page |
| GET | `/api/v1/alert-channels` | Empty page |
| GET | `/api/v1/market-data/candles` | Empty page |
| GET | `/api/v1/exchanges` | Prototype source list, not stored |
| GET | `/api/v1/strategies/time-mode` | Prototype config, not stored |

`POST`, `PUT`, `PATCH`, and `DELETE` are specified above and are not mounted yet. Calling them is 404.
