"""Publication controller."""

from Core.http import list_response
from Repositories.Publications.middlewares.publication_middleware import PublicationListQuery
from Repositories.Publications.modules import publication_module


async def get(params: PublicationListQuery) -> dict:
    data = await publication_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
