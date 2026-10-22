"""Alert feed controller."""

from Repositories.Alerts.modules import alert_feed_module


async def feed(params: dict) -> dict:
    return await alert_feed_module.feed(params, auth_user=None)
