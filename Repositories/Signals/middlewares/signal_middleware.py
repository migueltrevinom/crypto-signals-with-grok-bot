"""Validation for Signal list requests."""

from Core.schemas import PageQuery


class SignalListQuery(PageQuery):
    """Paging only until the filters in docs/api-spec.md are implemented."""
