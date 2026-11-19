"""Validation for Alert list requests."""

from Core.schemas import PageQuery


class AlertListQuery(PageQuery):
    """Paging only until the filters in docs/api-spec.md are implemented."""
