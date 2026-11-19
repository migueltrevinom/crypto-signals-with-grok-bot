"""ApiKey routes."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Auth.controllers import api_key_controller
from Repositories.Auth.middlewares.api_key_middleware import ApiKeyListQuery

router = APIRouter(
    prefix="/api-keys",
    tags=["auth"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="List user API keys. Empty. Raw keys are never stored.")
async def list_api_keys(params: ApiKeyListQuery = Depends()) -> dict:
    return await api_key_controller.get(params)
