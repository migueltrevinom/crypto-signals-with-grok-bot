"""Per-IP and per-key limits. Not enforced in this pass.

Auth routes will be limited per IP. Other `/api/v1` routes will be limited
per API key. A miss is 429 `rate_limited`. See docs/saas.md.
"""


def check_rate_limit(key: str) -> None:
    del key
    raise NotImplementedError("Rate limiting is specified and not enforced yet.")
