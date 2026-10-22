"""Alert controller. Calls the module and shapes the list envelope."""

from Core.http import list_response
from Repositories.Alerts.middlewares.alert_middleware import AlertListQuery
from Repositories.Alerts.modules import alert_module


async def get(params: AlertListQuery) -> dict:
    data = await alert_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
