"""The read path exists and is not a private find()."""

import asyncio

import pytest

from Core.mongo_orm import build_query


def test_build_query_is_not_implemented() -> None:
    with pytest.raises(NotImplementedError, match="build_query"):
        asyncio.run(build_query({"findOne": True}, model=dict, allowed_populates=[]))
