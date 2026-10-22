"""Response envelopes shared by controllers. Matches the verifik list shape."""


def page_args(params: dict) -> tuple[int, int]:
    page = max(int(params.get("page") or 1), 1)
    limit = min(max(int(params.get("limit") or 20), 1), 100)
    return page, limit


def empty_page(page: int = 1, limit: int = 20) -> dict:
    """Planning-skeleton page. No Mongo read."""
    return {"docs": [], "total": 0, "limit": limit, "page": page, "pages": 0}


def list_response(result: dict) -> dict:
    return {
        "data": result.get("docs", []),
        "total": result.get("total", 0),
        "limit": result.get("limit", 20),
        "page": result.get("page", 1),
        "pages": result.get("pages", 0),
    }
