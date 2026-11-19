"""Country and market gate. The Canada futures rule is a product hold, not a ruling."""

from typing import Literal

from beanie import Document
from pymongo import ASCENDING, IndexModel


class GeoRule(Document):
    country: str
    market: Literal["futures", "spot"]
    action: Literal["withhold", "allow"]
    reason: str

    class Settings:
        name = "geo_rules"
        indexes = [
            IndexModel(
                [("country", ASCENDING), ("market", ASCENDING)],
                unique=True,
                name="country_market",
            ),
        ]
