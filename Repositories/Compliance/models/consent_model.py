"""Recorded acceptance of a disclosure version."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Consent(Document):
    user_id: PydanticObjectId
    document: Literal["tos", "risk", "conflicts"]
    version: str
    accepted_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "consents"
        indexes = [
            IndexModel(
                [
                    ("user_id", ASCENDING),
                    ("document", ASCENDING),
                    ("version", ASCENDING),
                ],
                name="user_document_version",
            ),
        ]
