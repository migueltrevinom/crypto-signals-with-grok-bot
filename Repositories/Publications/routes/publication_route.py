"""Publication routes."""

from fastapi import APIRouter, Depends

from Core.auth import require_api_key
from Repositories.Publications.controllers import publication_controller
from Repositories.Publications.middlewares.publication_middleware import PublicationListQuery

router = APIRouter(
    prefix="/publications",
    tags=["publications"],
    dependencies=[Depends(require_api_key)],
)


@router.get("", summary="List signal publications. Empty.")
async def list_publications(params: PublicationListQuery = Depends()) -> dict:
    return await publication_controller.get(params)
