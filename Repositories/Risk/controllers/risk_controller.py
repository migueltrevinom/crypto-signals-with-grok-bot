"""Risk controller. The skeleton returns the unsaved seed."""

from Repositories.Risk.modules import risk_module


async def list_profiles() -> dict:
    data = await risk_module.list_profiles(auth_user=None)
    return {
        "data": data,
        "total": len(data),
        "limit": 20,
        "page": 1,
        "pages": 1 if data else 0,
    }
