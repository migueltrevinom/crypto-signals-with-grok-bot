"""time@mode rule engine (pure, deterministic). Operates on lists of closed candles.

Part A: trend/structure, modes (flat wick levels), confirmations, bias flips, expiry.
Part B: HTF trading blocks + LTF breakout entries (70 SMA filter) + exits.
"""
import numpy as np

# ---------------------------------------------------------------- indicators

def arrays(candles):
    f = lambda k: np.array([x[k] for x in candles], dtype=float)
    return dict(t=np.array([x["t"] for x in candles], dtype=np.int64),
                ct=np.array([x["ct"] for x in candles], dtype=np.int64),
                o=f("o"), h=f("h"), l=f("l"), c=f("c"))


def atr_rma(h, l, c, n):
    """TradingView ta.atr: true range smoothed with RMA, seeded by SMA of first n TRs."""
    tr = np.empty(len(c))
    tr[0] = h[0] - l[0]
    if len(c) > 1:
        pc = c[:-1]
        tr[1:] = np.maximum.reduce([h[1:] - l[1:], np.abs(h[1:] - pc), np.abs(l[1:] - pc)])
    out = np.full(len(c), np.nan)
    if len(c) >= n:
        out[n - 1] = tr[:n].mean()
        for i in range(n, len(c)):
            out[i] = (out[i - 1] * (n - 1) + tr[i]) / n
    return out


def sma(x, n):
    out = np.full(len(x), np.nan)
    if len(x) >= n:
        cs = np.cumsum(np.insert(x, 0, 0.0))
        out[n - 1:] = (cs[n:] - cs[:-n]) / n
    return out


def swings(h, l, lb):
    """Pivot highs/lows: extreme vs lb bars on each side. Confirmed lb bars later."""
    n = len(h); sh, sl = [], []
    for k in range(lb, n - lb):
        if h[k] > h[k + 1:k + lb + 1].max() and h[k] >= h[k - lb:k].max():
            sh.append(k)
        if l[k] < l[k + 1:k + lb + 1].min() and l[k] <= l[k - lb:k].min():
            sl.append(k)
    return sh, sl


def trend_at(i, a, sh, sl, lb):
    """Market structure as of bar i using only swings confirmed by bar i."""
    hs = [k for k in sh if k + lb <= i][-2:]
    ls = [k for k in sl if k + lb <= i][-2:]
    h, l, c = a["h"], a["l"], a["c"]
    if len(hs) < 2 or len(ls) < 2:
        return "unknown"
    hh, hl = h[hs[1]] > h[hs[0]], l[ls[1]] > l[ls[0]]
    t = "up" if hh and hl else "down" if (not hh and not hl) else "range"
    # market-structure break overrides: close through last swing extreme
    if t != "up" and c[i] > h[hs[1]]:
        t = "up (structure break)"
    elif t != "down" and c[i] < l[ls[1]]:
        t = "down (structure break)"
    return t


def is_expansion(a, i, d, p):
    o, h, l, c = a["o"][i], a["h"][i], a["l"][i], a["c"][i]
    body = (c - o) * d
    if body <= 0:
        return False
    big_vs_prev = body > (a["h"][i - 1] - a["l"][i - 1])
    big_vs_self = body >= (h - l) * p["body_range_ratio"]
    rule = p.get("expansion_rule", "either")
    return {"prev_range": big_vs_prev, "self_ratio": big_vs_self,
            "both": big_vs_prev and big_vs_self}.get(rule, big_vs_prev or big_vs_self)


# ---------------------------------------------------------------- params

def params_for(p, tf):
    """Params may be per-timeframe: {"default": x, "1w": y}. Resolve for one timeframe."""
    return {k: (v.get(tf, v.get("default")) if isinstance(v, dict) and "default" in v else v)
            for k, v in p.items()}


# ---------------------------------------------------------------- Part A: modes

def detect_modes(a, p):
    """Return list of signal dicts (bar index based) for mode_confirmed / bias_flip / mode_expiry."""
    o, h, l, c = a["o"], a["h"], a["l"], a["c"]
    n = len(c)
    atr = atr_rma(h, l, c, p["atr_length"])
    lb = p["swing_lookback"]
    sh, sl = swings(h, l, lb)
    mult, ratio = p["confirm_atr_mult"], p["body_range_ratio"]
    mn, mx = p["mode_min_bars"], p["mode_max_bars"]
    span_max = p["consolidation_limit"]
    dens, tolk = p["mode_touch_density"], p["mode_touch_tol_atr"]
    types = set(p["confirm_types"])
    sigs, consumed = [], []  # consumed: (level, start, conf_bar, dir)
    start_i = max(p["atr_length"] + 1, span_max + 1)
    for i in range(start_i, n):
        rng = h[i] - l[i]
        if rng <= 0 or c[i] == o[i] or np.isnan(atr[i - 1]):
            continue
        d = 1 if c[i] > o[i] else -1
        body = abs(c[i] - o[i])
        exp_ = is_expansion(a, i, d, p)
        gap_shape = body >= ratio * rng and (
            (h[i] > h[i - 1] and l[i] > l[i - 1]) if d > 0 else (h[i] < h[i - 1] and l[i] < l[i - 1]))
        if not exp_ and not gap_shape:
            continue  # cheap prefilter: cannot confirm anything
        A = atr[i - 1]; tol = A * tolk
        e = i - 1; w0 = e - span_max + 1
        idx = np.arange(w0, e + 1)
        levels = np.concatenate([l[idx], h[idx]])
        kinds = ["HL"] * len(idx) + ["LH"] * len(idx)
        anchors = np.concatenate([idx, idx])
        M = (l[idx][None, :] - tol <= levels[:, None]) & (levels[:, None] <= h[idx][None, :] + tol)
        T_from = np.cumsum(M[:, ::-1], axis=1)[:, ::-1]  # T_from[L, s] = touches in [s..e]
        best = None
        rule = p["body_cross_count_rule"]
        bc_all = (np.minimum(o[i], c[i]) <= levels) & (levels <= np.maximum(o[i], c[i]))
        extra = (bc_all & (rule == "part_of_mode_next_bar")).astype(int)
        for si in range(0, len(idx) - mn + 2):
            s = idx[si]; N = e - s + 1
            T = T_from[:, si]
            eff = T + extra
            ok = M[:, si] & M[:, -1] & (eff >= mn) & (eff <= mx) & (T >= dens * N)
            # anchor must lie inside the span
            ok &= anchors >= s
            if not ok.any():
                continue
            for L_i in np.nonzero(ok)[0]:
                L = levels[L_i]
                if (c[i] - L) * d <= 0:
                    continue  # must close beyond the mode in candle direction
                dist = (c[i] - L) * d / A
                conf = []
                if "atr_expansion" in types and exp_ and dist >= mult:
                    conf.append("atr_expansion")
                if "close_outside_range" in types and exp_ and (
                        c[i] > h[s:e + 1].max() if d > 0 else c[i] < l[s:e + 1].min()):
                    conf.append("close_outside_range")
                if "clear_gap" in types and gap_shape and (
                        l[i] > L + tol if d > 0 else h[i] < L - tol):
                    conf.append("clear_gap")
                if not conf:
                    continue
                # first decisive close: no earlier bar in span already closed >= mult ATR beyond
                # first decisive close since the anchor wick printed (the level did not exist before)
                ak = int(anchors[L_i])
                if any((c[q] - L) * d / atr[q - 1] >= mult and is_expansion(a, q, d, p)
                       for q in range(ak + 1, e + 1)):
                    continue
                if any(dc == d and sc <= e and ic >= s and abs(L - Lc) <= 0.5 * A
                       for Lc, sc, ic, dc in consumed):
                    continue
                key = (-int(eff[L_i]), -N, abs(L - c[i]))
                if best is None or key < best[0]:
                    best = (key, dict(level=float(L), kind=kinds[L_i], anchor=int(anchors[L_i]),
                                      start=int(s), end=int(e), length=int(eff[L_i]), touches_before=int(T[L_i]), span=int(N),
                                      atr=float(A), atr_dist=float(dist), confirmations=conf))
        if best is None:
            continue
        m = best[1]
        L = m["level"]
        body_cross = min(o[i], c[i]) <= L <= max(o[i], c[i])
        count_start = i + 1 if (body_cross and rule in ("next_bar", "part_of_mode_next_bar")) else i
        expiry = count_start + m["length"] - 1
        consumed.append((L, m["start"], i, d))
        sigs.append(dict(type="mode_confirmed", bar=i, dir=d, price=float(c[i]), **m,
                         body_crosses_mode=bool(body_cross), count_start_bar=count_start,
                         expiry_bar=expiry, trend=trend_at(i, a, sh, sl, lb),
                         expansion=bool(exp_)))
        # ---- invalidation / bias flip
        flipped = False
        for b in range(i + 1, min(n, i + 1 + p["flip_window_bars"])):
            if (c[b] - o[b]) * -d <= 0 or (c[b] - L) * -d <= 0:
                continue
            if p["flip_requires_expansion"] and not ((c[b] - o[b]) * -d > h[b - 1] - l[b - 1]):
                continue
            if p["flip_requires_engulfing"]:
                lo, hi = min(o[b - 1], c[b - 1]), max(o[b - 1], c[b - 1])
                if not (min(o[b], c[b]) <= lo and max(o[b], c[b]) >= hi):
                    continue
            sigs.append(dict(type="bias_flip", bar=b, dir=-d, price=float(c[b]), level=L,
                             atr=float(atr[b - 1]), atr_dist=float((c[b] - L) * -d / atr[b - 1]),
                             mode_confirmed_bar=i, length=m["length"],
                             trend=trend_at(b, a, sh, sl, lb)))
            flipped = True
            break
        # ---- expiry
        if expiry < n and (not flipped or p["expiry_after_flip"]):
            seg = slice(i, expiry + 1)
            new_ext = (l[expiry] <= l[seg].min()) if d < 0 else (h[expiry] >= h[seg].max())
            sigs.append(dict(type="mode_expiry", bar=expiry, dir=d, price=float(c[expiry]), level=L,
                             atr=float(atr[expiry - 1]),
                             atr_dist=float((c[expiry] - L) * d / atr[expiry - 1]),
                             mode_confirmed_bar=i, length=m["length"],
                             expiry_bar_made_new_extreme=bool(new_ext),
                             trend=trend_at(expiry, a, sh, sl, lb)))
    return sigs


# ---------------------------------------------------------------- Part B: trading blocks

def htf_blocks(H, p):
    """Persistent trading blocks. A long block is the highest HTF close of the last
    consolidation_limit bars once at least block_min_bars_after bars closed below it; a short
    block mirrors it with the lowest close. A block stays active for block_ttl_bars HTF bars
    after its own bar, so it can be broken, lost, and re-taken (re-entry).
    Returns {k: [(dir, level, block_bar), ...]} of blocks active after HTF bar k closes."""
    c = H["c"]; lim = p["consolidation_limit"]; ma = p["block_min_bars_after"]
    ttl = p.get("block_ttl_bars", 30)
    merge = p.get("block_merge_atr", 0.25)
    atr = atr_rma(H["h"], H["l"], c, p["atr_length"])
    known = {}  # (dir, bar) -> level
    out = {}
    for k in range(lim - 1, len(c)):
        w0 = k - lim + 1
        for d, b in ((1, int(np.argmax(c[w0:k + 1])) + w0), (-1, int(np.argmin(c[w0:k + 1])) + w0)):
            if k - b >= ma and (d, b) not in known:
                near = [kk for kk, v in known.items() if kk[0] == d and abs(v - c[b]) <= merge * atr[k]]
                if not near:  # ignore a new block that is just a re-print of an existing one
                    known[(d, b)] = float(c[b])
        out[k] = [(d, lv, b) for (d, b), lv in known.items() if k - b <= ttl]
        known = {key: v for key, v in known.items() if k - key[1] <= ttl}
    return out


def detect_blocks(H, Lw, p, sma_series=None):
    """Entries/exits on the LTF against HTF blocks.

    Entry: first LTF close beyond an active HTF block (prev close on the other side), with the
    close on the right side of the 70 SMA. While a position is open, a new entry is only taken
    on a further block (higher for longs / lower for shorts), which also moves the exit level.
    sma_series: optional (t_array, sma_array) used for the trend filter instead of the entry
    timeframe's own SMA (for sma_filter_timeframe != 'entry').
    """
    o, h, l, c, t = Lw["o"], Lw["h"], Lw["l"], Lw["c"], Lw["t"]
    n = len(c)
    atr = atr_rma(h, l, c, p["atr_length"])
    ma = sma(c, p["sma_length"])
    blocks = htf_blocks(H, p)
    hct = H["ct"]
    sigs = []
    pos = {1: None, -1: None}
    dirs = [1, -1] if p.get("enable_shorts", True) else [1]
    k_ptr = -1
    for j in range(2, n):
        while k_ptr + 1 < len(hct) and hct[k_ptr + 1] <= t[j]:
            k_ptr += 1
        # --- exits first
        for d in dirs:
            ps = pos[d]
            if ps is None or j <= ps["bar"]:
                continue
            E = ps["level"]
            if p["exit_rule"] == "close_back_inside":
                hit = (c[j] - E) * d < 0
            else:  # two consecutive closes beyond entry level with lower lows (higher highs for shorts)
                ext = l if d > 0 else h
                hit = ((c[j] - E) * d < 0 and (c[j - 1] - E) * d < 0 and j - 1 > ps["bar"]
                       and (ext[j] - ext[j - 1]) * d < 0 and (ext[j - 1] - ext[j - 2]) * d < 0)
            if hit:
                sigs.append(dict(type="exit", bar=j, dir=d, price=float(c[j]), level=E,
                                 atr=float(atr[j - 1]), atr_dist=float((c[j] - E) * d / atr[j - 1]),
                                 entry_bar=ps["bar"], htf_bar=ps["htf_bar"],
                                 htf_block_bar=ps["block_bar"]))
                pos[d] = None
        if k_ptr not in blocks or np.isnan(ma[j]) or np.isnan(atr[j - 1]):
            continue
        if sma_series is not None:
            st, sv = sma_series
            q = np.searchsorted(st, t[j], side="right") - 1
            filt = sv[q] if q >= 0 else np.nan
        else:
            filt = ma[j]
        if np.isnan(filt):
            continue
        for d in dirs:
            if (c[j] - filt) * d <= 0:
                continue
            crossed = [(lv, b) for dd, lv, b in blocks[k_ptr] if dd == d
                       and (c[j] - lv) * d > 0 and (c[j - 1] - lv) * d <= 0
                       and (pos[d] is None or (lv - pos[d]["level"]) * d > 0)]
            if not crossed:
                continue
            B, bb = max(crossed, key=lambda x: x[0] * d)  # furthest block crossed
            exp_ = (c[j] - o[j]) * d > (h[j - 1] - l[j - 1])
            sigs.append(dict(type="block_breakout_entry", bar=j, dir=d, price=float(c[j]),
                             level=B, atr=float(atr[j - 1]),
                             atr_dist=float((c[j] - B) * d / atr[j - 1]),
                             sma=float(filt), expansion=bool(exp_),
                             htf_bar=int(k_ptr), htf_block_bar=int(bb)))
            pos[d] = dict(bar=j, level=B, htf_bar=int(k_ptr), block_bar=int(bb))
    return sigs
