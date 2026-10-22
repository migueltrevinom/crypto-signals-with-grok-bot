"""Validation for Position list requests."""

from Core.schemas import PageQuery


class PositionListQuery(PageQuery):
    """Paging only until the filters in docs/repositories.md are implemented."""
