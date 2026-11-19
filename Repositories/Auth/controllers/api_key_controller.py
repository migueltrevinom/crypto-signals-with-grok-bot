"""ApiKey controller."""

from Core.http import list_response
from Repositories.Auth.middlewares.api_key_middleware import ApiKeyListQuery
from Repositories.Auth.modules import api_key_module


async def get(params: ApiKeyListQuery) -> dict:
    data = await api_key_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
