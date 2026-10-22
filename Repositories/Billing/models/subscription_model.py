"""A user's plan and payment state."""

from datetime import UTC, datetime
from typing import Literal

from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Subscription(Document):
    user_id: PydanticObjectId
    plan_code: str
    status: Literal[
        "trialing",
        "active",
        "past_due",
        "grace",
        "canceled",
        "incomplete",
    ] = "incomplete"
    provider: Literal["stripe", "crypto"] = "stripe"
    provider_customer_id: str | None = None
    provider_subscription_id: str | None = None
    trial_ends_at: datetime | None = None
    grace_ends_at: datetime | None = None
    current_period_end: datetime | None = None
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "subscriptions"
        indexes = [
            IndexModel(
                [("user_id", ASCENDING), ("status", ASCENDING)],
                name="user_status",
            ),
            IndexModel(
                [("provider_subscription_id", ASCENDING)],
                unique=True,
                sparse=True,
                name="provider_subscription",
            ),
        ]
