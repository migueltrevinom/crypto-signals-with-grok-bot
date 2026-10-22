"""Validation for PositionEvent list requests."""

from Core.schemas import PageQuery


class PositionEventListQuery(PageQuery):
    """Paging only until the filters in docs/repositories.md are implemented."""
