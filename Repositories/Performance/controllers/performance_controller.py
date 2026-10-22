"""Performance controller."""

from Repositories.Performance.modules import performance_module


async def track_record(sample: str = "forward") -> dict:
    return {"data": await performance_module.track_record(sample)}
