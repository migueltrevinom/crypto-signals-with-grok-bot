"""Validation for User list requests."""

from Core.schemas import PageQuery


class UserListQuery(PageQuery):
    """Paging only until the filters in docs/repositories.md are implemented."""
