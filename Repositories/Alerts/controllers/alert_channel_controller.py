"""AlertChannel controller. Calls the module and shapes the list envelope."""

from Core.http import list_response
from Repositories.Alerts.middlewares.alert_channel_middleware import AlertChannelListQuery
from Repositories.Alerts.modules import alert_channel_module


async def get(params: AlertChannelListQuery) -> dict:
    data = await alert_channel_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
