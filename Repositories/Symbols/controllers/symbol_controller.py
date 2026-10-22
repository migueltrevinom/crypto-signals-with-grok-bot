"""Symbol controller."""

from Core.http import list_response
from Repositories.Symbols.middlewares.symbol_middleware import SymbolListQuery
from Repositories.Symbols.modules import symbol_module


async def get(params: SymbolListQuery) -> dict:
    data = await symbol_module.get(params.model_dump(), auth_user=None)
    return list_response(data)
