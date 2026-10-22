"""Validation for confluence reads."""

from Core.schemas import PageQuery


class EntryPlanListQuery(PageQuery):
    """Paging only. Filters arrive with the entry-plan implementation."""
