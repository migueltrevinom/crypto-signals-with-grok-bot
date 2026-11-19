"""Public, key-less kline fetchers with fallback. Returns only CLOSED candles.

Each candle: dict(t=open_ms, ct=close_ms (open + interval), o,h,l,c,v floats).
"""
import json, time, urllib.request, urllib.parse

INTERVAL_MS = {"15m": 900_000, "30m": 1_800_000, "1h": 3_600_000, "4h": 14_400_000,
               "6h": 21_600_000, "1d": 86_400_000, "1w": 604_800_000}
_UA = {"User-Agent": "timemode-scanner/1.0"}


def _get(url, timeout=15):
    req = urllib.request.Request(url, headers=_UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def _binance(base, symbol, interval, limit, end_ms=None, start_ms=None):
    out = []
    remaining = limit
    end = end_ms
    while remaining > 0:
        q = {"symbol": symbol, "interval": interval, "limit": min(1000, remaining)}
        if end is not None:
            q["endTime"] = end
        if start_ms is not None and end is None:
            q["startTime"] = start_ms
        rows = _get(f"{base}/api/v3/klines?" + urllib.parse.urlencode(q))
        if isinstance(rows, dict):
            raise RuntimeError(f"binance error: {rows}")
        if not rows:
            break
        batch = [dict(t=int(r[0]), o=float(r[1]), h=float(r[2]), l=float(r[3]),
                      c=float(r[4]), v=float(r[5])) for r in rows]
        out = batch + out
        remaining -= len(batch)
        if len(batch) < q["limit"] or start_ms is not None:
            break
        end = batch[0]["t"] - 1
    return out


def fetch_binance(symbol, interval, limit, **kw):
    return _binance("https://api.binance.com", symbol, interval, limit, **kw)


def fetch_binance_vision(symbol, interval, limit, **kw):
    return _binance("https://data-api.binance.vision", symbol, interval, limit, **kw)


def fetch_bybit(symbol, interval, limit, end_ms=None, start_ms=None):
    iv = {"15m": "15", "30m": "30", "1h": "60", "4h": "240", "6h": "360", "1d": "D", "1w": "W"}[interval]
    out, end, remaining = [], end_ms, limit
    while remaining > 0:
        q = {"category": "spot", "symbol": symbol, "interval": iv, "limit": min(1000, remaining)}
        if end is not None:
            q["end"] = end
        if start_ms is not None and end is None:
            q["start"] = start_ms
        j = _get("https://api.bybit.com/v5/market/kline?" + urllib.parse.urlencode(q))
        if j.get("retCode") != 0:
            raise RuntimeError(f"bybit error: {j.get('retMsg')}")
        rows = j["result"]["list"][::-1]
        if not rows:
            break
        batch = [dict(t=int(r[0]), o=float(r[1]), h=float(r[2]), l=float(r[3]),
                      c=float(r[4]), v=float(r[5])) for r in rows]
        out = batch + out
        remaining -= len(batch)
        if len(batch) < q["limit"] or start_ms is not None:
            break
        end = batch[0]["t"] - 1
    return out


def fetch_okx(symbol, interval, limit, end_ms=None, start_ms=None):
    iv = {"15m": "15m", "30m": "30m", "1h": "1H", "4h": "4Hutc", "6h": "6Hutc",
          "1d": "1Dutc", "1w": "1Wutc"}[interval]
    inst = symbol[:-4] + "-USDT" if symbol.endswith("USDT") else symbol
    out, after, remaining = [], end_ms, limit
    while remaining > 0:
        q = {"instId": inst, "bar": iv, "limit": min(100, remaining)}
        if after is not None:
            q["after"] = after
        j = _get("https://www.okx.com/api/v5/market/history-candles?" + urllib.parse.urlencode(q))
        if j.get("code") != "0":
            raise RuntimeError(f"okx error: {j.get('msg')}")
        rows = j["data"][::-1]
        if not rows:
            break
        batch = [dict(t=int(r[0]), o=float(r[1]), h=float(r[2]), l=float(r[3]),
                      c=float(r[4]), v=float(r[5])) for r in rows]
        out = batch + out
        remaining -= len(batch)
        if len(batch) < q["limit"]:
            break
        after = batch[0]["t"]
        if start_ms is not None and after <= start_ms:
            break
    return out


SOURCES = {"binance": fetch_binance, "binance_vision": fetch_binance_vision,
           "bybit": fetch_bybit, "okx": fetch_okx}


def fetch(symbol, interval, limit, sources, now_ms=None, retries=2, **kw):
    """Try each source in order; drop the still-forming candle. Returns (source, candles)."""
    now_ms = now_ms or int(time.time() * 1000)
    step = INTERVAL_MS[interval]
    errors = []
    for name in sources:
        for attempt in range(retries):
            try:
                rows = SOURCES[name](symbol, interval, limit, **kw)
                rows = [r for r in rows if r["t"] + step <= now_ms]  # closed candles only
                for r in rows:
                    r["ct"] = r["t"] + step
                # de-dup / sort
                seen, clean = set(), []
                for r in sorted(rows, key=lambda r: r["t"]):
                    if r["t"] not in seen:
                        seen.add(r["t"]); clean.append(r)
                if clean:
                    return name, clean
                errors.append(f"{name}: empty")
                break
            except Exception as e:  # network / geo-block / API error -> retry, then next source
                errors.append(f"{name}: {e}")
                time.sleep(0.5 * (attempt + 1))
    raise RuntimeError(f"all sources failed for {symbol} {interval}: {errors}")
