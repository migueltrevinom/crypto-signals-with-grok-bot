"""Shared request shapes. Domain middlewares extend these."""

from pydantic import BaseModel, Field


class PageQuery(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)
