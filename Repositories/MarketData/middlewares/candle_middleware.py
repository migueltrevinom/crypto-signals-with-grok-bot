"""Validation for Candle list requests."""

from Core.schemas import PageQuery


class CandleListQuery(PageQuery):
    """Paging only until the filters in docs/api-spec.md are implemented."""
