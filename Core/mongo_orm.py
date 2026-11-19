"""Shared Mongo read path. Modules call this and nothing else for reads.

The parameter language matches verifik-backend's mongo-orm.buildQuery.
The public HTTP API does not expose these key names; modules translate
validated query params into them. See docs/architecture.md for the table.

Planning skeleton: execution is not implemented. Calling this is the signal
that a read belongs here rather than in a private collection.find.
"""

from typing import Any


async def build_query(
    params: dict[str, Any],
    model: type[Any],
    allowed_populates: list[str] | None = None,
) -> Any:
    """Run one read against `model`.

    `allowed_populates` is the relation allow-list for this call. Names not
    on the list are ignored once this is implemented. Pass [] when the
    document has no relations.
    """
    del params, model, allowed_populates
    raise NotImplementedError(
        "Mongo reads are not wired yet. Implement Core.mongo_orm.build_query "
        "and call it from the module. Do not query Motor or Beanie find() directly. "
        "See docs/architecture.md."
    )
