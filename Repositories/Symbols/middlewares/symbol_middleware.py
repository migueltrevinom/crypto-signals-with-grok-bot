"""Validation for Symbol list requests."""

from Core.schemas import PageQuery


class SymbolListQuery(PageQuery):
    """Paging only until the filters in docs/repositories.md are implemented."""
