"""Pluggable alert delivery.

grok_chat is a pull feed: the worker inserts a row and the bot polls it.
webhook and email are the same protocol and are not implemented.
"""

from typing import Any, Protocol


class Notifier(Protocol):
    kind: str

    async def send(self, *, channel: dict[str, Any], payload: dict[str, Any]) -> None:
        """Push `payload`. grok_chat does not use this."""


class GrokChatNotifier:
    """No push. Delivery is the alert row plus GET /api/v1/alerts/feed."""

    kind = "grok_chat"

    async def send(self, *, channel: dict[str, Any], payload: dict[str, Any]) -> None:
        del channel, payload
        raise NotImplementedError(
            "grok_chat is pulled by the bot. Insert an alert row instead of calling send."
        )


class WebhookNotifier:
    """POST the payload to channel['config']['url']. Later phase."""

    kind = "webhook"

    async def send(self, *, channel: dict[str, Any], payload: dict[str, Any]) -> None:
        del channel, payload
        raise NotImplementedError("Webhook delivery is a later roadmap phase.")


class EmailNotifier:
    """Send channel['config']['to']. Later phase."""

    kind = "email"

    async def send(self, *, channel: dict[str, Any], payload: dict[str, Any]) -> None:
        del channel, payload
        raise NotImplementedError("Email delivery is a later roadmap phase.")
