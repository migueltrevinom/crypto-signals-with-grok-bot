"""Validation for Backtest list requests."""

from Core.schemas import PageQuery


class BacktestListQuery(PageQuery):
    """Paging only until the filters in docs/api-spec.md are implemented."""
