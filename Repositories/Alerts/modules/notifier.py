"""Pluggable alert delivery.

The scan and the Signals module do not know how a channel is reached.
Phase 3 adds WebhookNotifier and registers it for kind `webhook`.
"""

from typing import Any, Protocol


class Notifier(Protocol):
    kind: str

    async def send(self, *, channel: dict[str, Any], payload: dict[str, Any]) -> None:
        """Deliver `payload` to `channel`. Raise on failure; the caller records it."""


class WebhookNotifier:
    """POST the signal JSON to channel['config']['url']. Not implemented in this pass."""

    kind = "webhook"

    async def send(self, *, channel: dict[str, Any], payload: dict[str, Any]) -> None:
        del channel, payload
        raise NotImplementedError(
            "Webhook delivery is roadmap phase 3. See docs/architecture.md."
        )
