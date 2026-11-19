"""User routes."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Users.controllers import user_controller
from Repositories.Users.middlewares.user_middleware import UserListQuery

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="List users. Planning skeleton: empty page.")
async def list_users(params: UserListQuery = Depends()) -> dict:
    return await user_controller.get(params)
