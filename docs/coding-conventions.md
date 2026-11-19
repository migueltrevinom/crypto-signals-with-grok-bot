# Coding conventions

Python 3.12. Format and lint with Ruff (`line-length` 100, rules E, F, I, UP). The CI command is `ruff check app Core Repositories tests`.

Domain folders are PascalCase (`Repositories/Signals`) even though PEP 8 prefers lowercase packages. That is deliberate, so the tree matches verifik-backend. Modules inside them are snake_case.

## File roles

| Suffix | May do | May not do |
| --- | --- | --- |
| `_route.py` | Declare `APIRouter`, path, status code, dependencies | Business logic, Mongo, HTTP calls to exchanges |
| `_middleware.py` | Pydantic models for that route, auth dependencies | Decide a trade, write the database |
| `_controller.py` | Call modules, shape `{data, total, limit, page, pages}` | `build_query`, exchange HTTP, rule math |
| `_module.py` | Rules, orchestration of one domain's data | Import another domain's module, read Mongo except through `build_query` |
| `_model.py` | Beanie document, indexes, embedded Pydantic models | Request handling |
| `helpers/` | Pure functions used by that domain | I/O |

Shared pieces go in `Core/`: `config`, `database`, `mongo_orm`, `errors`, `http` (response envelopes), `http_client`, `cache`, `auth`, `logging`, `schemas` (`PageQuery`), `prototype_config` (temporary).

## Errors

Raise `Core.errors.AppError(message, status_code, code)`. Do not catch it in the controller. The handler writes `{message, code}`.

Use these codes when they fit: `not_found` (404), `conflict` (409), `unauthorized` (401), `server_misconfigured` (500), `mongo_unavailable` (503), `delivery_failed` (502), `not_implemented` (501).

Unexpected exceptions are logged server-side. The client receives `internal_error` and a fixed message.

## Mongo

Reads:

```python
await build_query(
    {"where_signal_id": signal_id, "findOne": True},
    Signal,
    allowed_populates=[],
)
```

Writes: construct the Beanie document and `insert()` / `save()` / `delete()`. Bulk upserts for the scanner can use the model's collection only inside the Signals module, and only for the write. A find-before-upsert is still a `build_query`.

`build_query` is unimplemented in the planning skeleton. Until phase 2, a module that has nothing to read returns `empty_page` and says so in its docstring. Do not "temporarily" call `Signal.find`.

Register new active documents in `app/documents.py`. Reserved future models stay unregistered.

## Async

I/O functions are `async def`. The detector, once ported, can stay synchronous if it is numpy on an in-memory array; the worker awaits the fetch and then calls it. Do not hide blocking exchange HTTP inside a request handler. Fetching belongs to the worker and to an explicit market-data route.

## Types and models

Public function arguments and returns are annotated. Prefer `str | None` over `Optional`.

Pydantic models use `Field(default_factory=...)` for dicts and lists. Do not use a mutable default. Timestamps use `default_factory=lambda: datetime.now(timezone.utc)`.

Literal unions for `type`, `direction`, `status`, and `kind` live next to the document that stores them. Do not rename the prototype's direction words (`bullish`/`bearish` vs `long`/`short`) inside the port.

## Naming

- Functions and variables: `snake_case`.
- Classes: `PascalCase`. The document class is the singular noun (`Signal`), the module file is `signal_module.py`.
- Collection names: plural snake_case, set explicitly.
- Routes: plural nouns, `/api/v1/signals`, `/api/v1/alert-channels`.
- Strategy path is singular on the key: `/api/v1/strategies/time-mode`.

## Logging

`Core.logging.configure_logging`. Log scan failures and alert failures with the symbol, timeframe, and signal id. Do not log webhook URLs, headers, or the API key.

## Tests

Domain tests live in that domain's `tests/`. App-level HTTP tests live in `/tests`. A test that needs the network or a real database is not part of the default pytest run until it is marked and the workflow opts in.

## Prototype

`prototype/` is reference code. Bugfixes to detection happen in the port, under `Repositories/Strategies/TimeMode`, and only with a failing replay test that Miguel's answer justifies. Do not silently "improve" `prototype/timemode.py` while porting it.

## Comments

Comment a non-obvious rule (why a weekly bar counts from the next candle, why the id hash uses `.10g`). Do not comment the control flow.
