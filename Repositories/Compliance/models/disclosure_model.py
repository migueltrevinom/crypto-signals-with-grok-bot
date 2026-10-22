"""Versioned conflict or risk text attached to public signals."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Disclosure(Document):
    kind: Literal["conflict", "risk"]
    version: str
    body: str
    active: bool = False
    created_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "disclosures"
        indexes = [
            IndexModel(
                [("kind", ASCENDING), ("active", ASCENDING)],
                name="kind_active",
            ),
        ]
