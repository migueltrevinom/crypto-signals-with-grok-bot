"""Async JSON GET with retries. Public market data only. No API keys."""

import asyncio
from typing import Any

import httpx

_CLIENT: httpx.AsyncClient | None = None


def set_client(client: httpx.AsyncClient | None) -> None:
    """Tests inject a MockTransport client. Production leaves this unset."""
    global _CLIENT
    _CLIENT = client


def _client() -> httpx.AsyncClient:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = httpx.AsyncClient(
            timeout=20.0,
            headers={"User-Agent": "crypto-signals-with-grok-bot/0.1"},
        )
    return _CLIENT


async def get_json(
    url: str,
    timeout: float = 20.0,
    params: dict | None = None,
    retries: int = 5,
) -> Any:
    delay = 0.4
    last_error: Exception | None = None
    client = _client()
    for _attempt in range(retries):
        try:
            response = await client.get(url, params=params, timeout=timeout)
        except httpx.HTTPError as exc:
            last_error = exc
            await asyncio.sleep(delay)
            delay = min(delay * 2, 8)
            continue
        if response.status_code in {418, 429, 500, 502, 503}:
            last_error = httpx.HTTPStatusError(
                "retryable",
                request=response.request,
                response=response,
            )
            await asyncio.sleep(delay)
            delay = min(delay * 2, 8)
            continue
        response.raise_for_status()
        return response.json()
    raise RuntimeError(f"GET failed for {url}: {last_error}")
