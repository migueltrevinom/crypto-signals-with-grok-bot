"""Feed query for the Grok Bot."""

from pydantic import BaseModel, Field


class AlertFeedQuery(BaseModel):
    status: str = "pending"
    limit: int = Field(50, ge=1, le=100)
    cursor: str | None = None
