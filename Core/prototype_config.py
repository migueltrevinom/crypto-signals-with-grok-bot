"""Temporary reader for prototype/config.json.

Phase 2 deletes this once `strategy_configs` and the default watchlist are
seeded in Mongo. Do not grow new features on it.
"""

import json
from functools import lru_cache
from typing import Any

from Core.config import REPO_ROOT


@lru_cache
def load_prototype_config() -> dict[str, Any]:
    path = REPO_ROOT / "prototype" / "config.json"
    return json.loads(path.read_text(encoding="utf-8"))
