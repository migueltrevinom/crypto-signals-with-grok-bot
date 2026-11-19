"""Validation for AlertChannel list requests."""

from Core.schemas import PageQuery


class AlertChannelListQuery(PageQuery):
    """Paging only until the filters in docs/api-spec.md are implemented."""
