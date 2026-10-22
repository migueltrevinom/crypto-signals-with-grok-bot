"""Compliance gate payload. This module does not give legal advice."""

from typing import Any

from Core.planning_seeds import COMPLIANCE_GATE


async def show_gate(auth_user: dict | None = None) -> dict[str, Any]:
    del auth_user
    return dict(COMPLIANCE_GATE)


def futures_allowed(country: str | None) -> bool:
    """Canada is withheld until counsel says otherwise. Not a legal conclusion."""
    if country is None:
        return False
    return country.upper() != "CA"
