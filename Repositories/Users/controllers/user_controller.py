"""User controller."""

from Core.http import list_response
from Repositories.Users.middlewares.user_middleware import UserListQuery
from Repositories.Users.modules import user_module


async def get(params: UserListQuery) -> dict:
    data = await user_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
