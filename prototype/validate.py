#!/usr/bin/env python3
"""Replay the detector over the documented chart examples (chart-analysis.md) and score it."""
import json, os, sys
from datetime import datetime, timezone
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import data as D, timemode as TM

cfg = json.load(open(os.path.join(HERE, "config.json"))); P = dict(cfg["params"])
ms = lambda s: int(datetime.fromisoformat(s).replace(tzinfo=timezone.utc).timestamp() * 1000)
day = lambda a, i: datetime.fromtimestamp(a["t"][i] / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M")
cache = {}
def series(sym, tf, end):
    k = (sym, tf, end)
    if k not in cache:
        _, rows = D.fetch(sym, tf, 1000, cfg["data_sources"], end_ms=ms(end))
        cache[k] = TM.arrays(rows)
    return cache[k]
def bar(a, s):  # index of candle opening at s
    return int(list(a["t"]).index(ms(s)))

results = []
def check(name, ok, detail):
    results.append((name, ok, detail)); print(("PASS " if ok else "MISS ") + name + " :: " + detail)

def find(sigs, typ, b, d=None):
    return [s for s in sigs if s["type"] == typ and s["bar"] == b and (d is None or s["dir"] == d)]

# ---------------- Part A: ETHBTC 1D Sep-Oct 2021 (charts 13-15)
a_tf = "1d"; a = series("ETHBTC", "1d", "2021-12-31"); S = TM.detect_modes(a, TM.params_for(P, a_tf))
def mode_case(name, conf, d, lvl, length, expiry=None, lvl_tol=0.0005):
    b = bar(a, conf); f = find(S, "mode_confirmed", b, d)
    if not f:
        check(name, False, f"no {('bull','bear')[d<0]} confirmation on {conf}"); return None
    s = f[0]; ok = abs(s["level"] - lvl) <= lvl_tol * lvl * 10 and s["length"] == length
    det = (f"conf {conf} level {s['level']:.6g} (doc {lvl}) len {s['length']} (doc {length}) "
           f"dist {s['atr_dist']:.2f} ATR {s['confirmations']} body_crosses={s['body_crosses_mode']} "
           f"-> expiry {day(a, s['expiry_bar'])[:10]}")
    check(name, ok, det)
    if expiry:
        check(name + " expiry", day(a, s["expiry_bar"])[:10] == expiry,
              f"detector {day(a, s['expiry_bar'])[:10]} vs doc {expiry}")
    return s
mode_case("ETHBTC 1D mode1 Sep17 bear 0.72ATR", "2021-09-17", -1, 0.07402, 8, "2021-09-24")
for dd in ("2021-10-04", "2021-10-05"):
    check(f"ETHBTC 1D {dd} NOT a confirmation (0.13/0.32 ATR)",
          not find(S, "mode_confirmed", bar(a, dd), -1), "correctly ignored" if not find(S, "mode_confirmed", bar(a, dd), -1) else "false confirmation")
m2 = mode_case("ETHBTC 1D mode2 Oct6 bear 1.82ATR", "2021-10-06", -1, 0.06918, 14, "2021-10-19")
ex = [s for s in S if s["type"] == "mode_expiry" and s["bar"] == bar(a, "2021-10-19")]
check("ETHBTC 1D Oct19 expiry lands on trend low 0.059323",
      bool(ex) and abs(a["l"][bar(a, "2021-10-19")] - 0.059323) < 1e-9 and ex[0]["expiry_bar_made_new_extreme"],
      f"expiry signal={bool(ex)} low={a['l'][bar(a,'2021-10-19')]} new_extreme={ex[0]['expiry_bar_made_new_extreme'] if ex else None}")
mode_case("ETHBTC 1D mode3 Oct18 bear (0.73ATR)", "2021-10-18", -1, 0.06245, 8)
fl = find(S, "bias_flip", bar(a, "2021-10-20"), 1)
check("ETHBTC 1D Oct20 engulfing bias flip to bullish", bool(fl),
      f"flip level {fl[0]['level']:.6g} dist {fl[0]['atr_dist']:.2f} ATR" if fl else "no flip")

# ---------------- ETHBTC 1D Feb-Apr 2021 (chart 16): projected expiry end dates
a_tf = "1d"; a = series("ETHBTC", "1d", "2021-08-31"); S = TM.detect_modes(a, TM.params_for(P, a_tf))
doc16 = [("2021-02-28", 9, -1), ("2021-03-11", 6, 1), ("2021-04-02", 5, 1), ("2021-04-02", 6, 1),
         ("2021-04-25", 12, 1), ("2021-04-25", 6, 1)]
lo, hi = bar(a, "2021-02-01"), bar(a, "2021-04-30")
conf16 = [s for s in S if s["type"] == "mode_confirmed" and lo <= s["bar"] <= hi]
print("   detector confirmations Feb-Apr 2021:", [(day(a, s["bar"])[:10], ('bear','bull')[s['dir']>0], s['length'],
      round(s['level'], 5), day(a, s['expiry_bar'])[:10]) for s in conf16])
for end, ln, d in doc16:
    hit = [s for s in conf16 if s["dir"] == d and abs(s["expiry_bar"] - bar(a, end)) <= 1]
    exact = [s for s in hit if s["expiry_bar"] == bar(a, end) and s["length"] == ln]
    check(f"ETHBTC 1D {('bear','bull')[d>0]} {ln}-bar mode expiring {end}", bool(exact),
          ("exact" if exact else (f"near: {[(day(a,s['bar'])[:10], s['length'], day(a,s['expiry_bar'])[:10]) for s in hit]}" if hit else "not found")))

# ---------------- ETHBTC 1W 2021 (charts 19-21)
a_tf = "1w"; a = series("ETHBTC", "1w", "2021-12-31"); S = TM.detect_modes(a, TM.params_for(P, a_tf))
for conf, d, lvl, ln, end in [("2021-03-29", 1, 0.0314, 6, "2021-05-10"), ("2021-04-12", 1, 0.03848, 5, "2021-05-17"),
                              ("2021-06-07", -1, 0.0735, 5, "2021-07-12")]:
    f = find(S, "mode_confirmed", bar(a, conf), d)
    if f:
        s = f[0]
        check(f"ETHBTC 1W {conf} {('bear','bull')[d>0]} mode {lvl}/{ln} bars -> {end}",
              abs(s["level"] - lvl) / lvl < 0.02 and day(a, s["expiry_bar"])[:10] == end,
              f"level {s['level']:.5g} len {s['length']} dist {s['atr_dist']:.2f} {s['confirmations']} expiry {day(a, s['expiry_bar'])[:10]}")
    else:
        near = [(day(a, s['bar'])[:10], s['type'], round(s['level'], 5)) for s in S if abs(s['bar'] - bar(a, conf)) <= 2 and s['type'] == 'mode_confirmed']
        check(f"ETHBTC 1W {conf} {('bear','bull')[d>0]} mode {lvl}/{ln} bars -> {end}", False, f"not detected; nearby {near}")

# ---------------- Part B: ARBBTC daily block -> 6h entry (charts 5-6), 6h block -> 1h entry (7-8)
H = series("ARBBTC", "1d", "2024-01-15"); L = series("ARBBTC", "6h", "2024-01-15")
B = TM.detect_blocks(H, L, TM.params_for(P, "x"))
e = [s for s in B if s["type"] == "block_breakout_entry" and s["dir"] > 0 and ms("2023-12-20") <= L["t"][s["bar"]] <= ms("2023-12-24")]
check("ARBBTC 1D block 0.00003014 -> 6h long entry Dec 22 06:00 UTC",
      bool(e) and abs(e[0]["level"] - 3.014e-5) < 2e-8 and day(L, e[0]["bar"]) == "2023-12-22 06:00",
      f"{[(day(L,s['bar']), f'{s['level']:.8f}', round(s['atr_dist'],2), 'exp' if s['expansion'] else '') for s in e]}")
H = L; L = series("ARBBTC", "1h", "2024-01-05")
B = TM.detect_blocks(H, L, TM.params_for(P, "x"))
e = [s for s in B if s["type"] == "block_breakout_entry" and s["dir"] > 0 and ms("2023-12-26") <= L["t"][s["bar"]] <= ms("2023-12-28 12:00")]
check("ARBBTC 6h block 0.00003227 -> 1h long entry Dec 27",
      any(abs(s["level"] - 3.227e-5) < 2e-8 and day(L, s["bar"]).startswith("2023-12-27") for s in e),
      f"{[(day(L,s['bar']), f'{s['level']:.8f}', round(s['atr_dist'],2)) for s in e]}")

# ---------------- ETHUSDT 6h block -> 30m entry / exit / re-entry (chart 9)
H = series("ETHUSDT", "6h", "2024-02-20"); L = series("ETHUSDT", "30m", "2024-02-14")
B = TM.detect_blocks(H, L, TM.params_for(P, "x"))
w = [s for s in B if s["dir"] > 0 and ms("2024-02-10") <= L["t"][s["bar"]] <= ms("2024-02-13")]
print("   ETH 30m long signals Feb 10-13:", [(s["type"], day(L, s["bar"]), round(s["level"], 2), round(s["price"], 2)) for s in w])
ent = [s for s in w if s["type"] == "block_breakout_entry"]; exi = [s for s in w if s["type"] == "exit"]
check("ETHUSDT 6h block ~2503-2504 -> 30m entry Feb 11 00:30 UTC (Feb 10 19:30 UTC-5)",
      any(day(L, s["bar"]) == "2024-02-11 00:30" for s in ent), f"entries {[ (day(L,s['bar']), round(s['level'],2)) for s in ent]}")
check("ETHUSDT 30m exit early Feb 12 (~08:30-09:00 UTC)",
      any(day(L, s["bar"]).startswith("2024-02-12 0") for s in exi), f"exits {[day(L,s['bar']) for s in exi]}")
check("ETHUSDT 30m re-entry Feb 12 14:30 UTC (09:30 UTC-5)",
      any(day(L, s["bar"]) == "2024-02-12 14:30" for s in ent), f"entries {[day(L,s['bar']) for s in ent]}")

n_ok = sum(r[1] for r in results)
print(f"\nSCORE: {n_ok}/{len(results)} documented checks reproduced")
