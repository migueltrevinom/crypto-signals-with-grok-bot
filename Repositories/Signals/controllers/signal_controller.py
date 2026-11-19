"""Signal controller. Calls the module and shapes the list envelope."""

from Core.http import list_response
from Repositories.Signals.middlewares.signal_middleware import SignalListQuery
from Repositories.Signals.modules import signal_module


async def get(params: SignalListQuery) -> dict:
    data = await signal_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
