"""Validation for Watchlist list requests."""

from Core.schemas import PageQuery


class WatchlistListQuery(PageQuery):
    """Paging only until the filters in docs/api-spec.md are implemented."""
