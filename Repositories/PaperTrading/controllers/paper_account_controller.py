"""PaperAccount controller."""

from Core.http import list_response
from Repositories.PaperTrading.middlewares.paper_account_middleware import PaperAccountListQuery
from Repositories.PaperTrading.modules import paper_account_module


async def get(params: PaperAccountListQuery) -> dict:
    data = await paper_account_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
