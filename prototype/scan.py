#!/usr/bin/env python3
"""time@mode scanner CLI.

  python3 scan.py                 # print NEW signals (JSON lines) from the last report_window_bars; update state.json
  python3 scan.py --all-recent N  # print every signal from the last N closed bars of each timeframe, ignore state
  python3 scan.py --prime         # record current signals in state.json without printing
"""
import argparse, hashlib, json, os, sys, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import data as D
import timemode as TM

EDM = ZoneInfo("America/Edmonton")
TV_IV = {"15m": "15", "30m": "30", "1h": "60", "4h": "240", "6h": "360", "1d": "1D", "1w": "1W"}
DIRS = {1: "bullish", -1: "bearish"}


def iso(ms, tz):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).astimezone(tz).isoformat(timespec="minutes")


def fmt(sym, tf, a, s, extra=None):
    ct = int(a["ct"][s["bar"]])
    out = dict(type=s["type"], symbol=sym, timeframe=tf,
               direction=DIRS[s["dir"]] if s["type"] not in ("block_breakout_entry", "exit")
               else ("long" if s["dir"] > 0 else "short"),
               close_time_utc=iso(ct, timezone.utc), close_time_edmonton=iso(ct, EDM),
               price=s["price"], level=s["level"],
               level_kind="block" if s["type"] in ("block_breakout_entry", "exit") else "mode",
               atr=round(s["atr"], 10), atr_distance=round(s["atr_dist"], 3),
               tradingview_url=f"https://www.tradingview.com/chart/?symbol=BINANCE:{sym}&interval={TV_IV[tf]}")
    step = D.INTERVAL_MS[tf]
    if s["type"] == "mode_confirmed":
        out.update(mode_length=s["length"], mode_anchor=s["kind"],
                   mode_anchor_time_utc=iso(int(a["t"][s["anchor"]]), timezone.utc),
                   mode_start_time_utc=iso(int(a["t"][s["start"]]), timezone.utc),
                   confirmations=s["confirmations"], body_crosses_mode=s["body_crosses_mode"],
                   projected_expiry_close_utc=iso(ct + (s["expiry_bar"] - s["bar"]) * step, timezone.utc),
                   projected_expiry_close_edmonton=iso(ct + (s["expiry_bar"] - s["bar"]) * step, EDM),
                   trend=s["trend"])
    elif s["type"] in ("bias_flip", "mode_expiry"):
        out.update(mode_length=s["length"],
                   mode_confirmed_close_utc=iso(int(a["ct"][s["mode_confirmed_bar"]]), timezone.utc),
                   trend=s["trend"])
        if s["type"] == "mode_expiry":
            out["expiry_bar_made_new_extreme"] = s["expiry_bar_made_new_extreme"]
    if extra:
        out.update(extra)
    key = f'{out["type"]}|{sym}|{tf}|{out["direction"]}|{ct}|{out.get("htf","")}|{s["level"]:.10g}'
    out["id"] = hashlib.sha1(key.encode()).hexdigest()[:16]
    return out


def run(cfg, now_ms=None):
    P = cfg["params"]
    now_ms = now_ms or int(time.time() * 1000)
    tfs = cfg["timeframes"]
    need = set(tfs) | {cfg["ltf_map"][tf] for tf in tfs if tf in cfg["ltf_map"]}
    sft = P.get("sma_filter_timeframe", "entry")
    if sft not in ("entry", "htf"):
        need.add(sft)
    jobs = [(s, tf) for s in cfg["symbols"] for tf in sorted(need)]
    series, sources, errors = {}, {}, []

    def job(st):
        s, tf = st
        return st, D.fetch(s, tf, cfg["history_bars"], cfg["data_sources"], now_ms=now_ms)

    with ThreadPoolExecutor(max_workers=8) as ex:
        for fut in [ex.submit(job, j) for j in jobs]:
            try:
                (s, tf), (src, rows) = fut.result()
                series[(s, tf)] = TM.arrays(rows); sources[src] = sources.get(src, 0) + 1
            except Exception as e:
                errors.append(str(e))
    signals = []
    for sym in cfg["symbols"]:
        for tf in tfs:
            a = series.get((sym, tf))
            if a is None or len(a["c"]) < 40:
                continue
            nbar = len(a["c"])
            p = TM.params_for(P, tf)
            for s in TM.detect_modes(a, p):
                o = fmt(sym, tf, a, s); o["_age"] = nbar - 1 - s["bar"]; signals.append(o)
            ltf = cfg["ltf_map"].get(tf)
            L = series.get((sym, ltf)) if ltf else None
            if L is None or len(L["c"]) < p["sma_length"] + 5:
                continue
            smas = None
            if sft == "htf":
                smas = (a["t"], TM.sma(a["c"], p["sma_length"]))
            elif sft != "entry" and (sym, sft) in series:
                S = series[(sym, sft)]
                smas = (S["ct"], TM.sma(S["c"], p["sma_length"]))
            for s in TM.detect_blocks(a, L, p, smas):
                extra = dict(htf=tf, htf_block_close_utc=iso(int(a["ct"][s["htf_block_bar"]]), timezone.utc))
                if "sma" in s:
                    extra.update(sma=s["sma"], expansion_candle=s["expansion"])
                if s["type"] == "exit":
                    extra["entry_close_utc"] = iso(int(L["ct"][s["entry_bar"]]), timezone.utc)
                o = fmt(sym, ltf, L, s, extra); o["_age"] = len(L["c"]) - 1 - s["bar"]; signals.append(o)
    signals.sort(key=lambda x: (x["close_time_utc"], x["symbol"], x["timeframe"], x["type"]))
    return signals, sources, errors


def main():
    ap = argparse.ArgumentParser(description="time@mode crypto scanner")
    ap.add_argument("--config", default=os.path.join(HERE, "config.json"))
    ap.add_argument("--all-recent", type=int, metavar="N",
                    help="print all signals from the last N closed bars per timeframe (ignores state)")
    ap.add_argument("--prime", action="store_true", help="record signals in state without printing")
    ap.add_argument("--symbols", help="comma list override")
    ap.add_argument("--timeframes", help="comma list override")
    ap.add_argument("--verbose", action="store_true", help="print data source / timing to stderr")
    args = ap.parse_args()
    cfg = json.load(open(args.config))
    if args.symbols:
        cfg["symbols"] = args.symbols.split(",")
    if args.timeframes:
        cfg["timeframes"] = args.timeframes.split(",")
    t0 = time.time()
    signals, sources, errors = run(cfg)
    for e in errors:
        print(f"[warn] {e}", file=sys.stderr)
    if args.verbose:
        print(f"[info] sources={sources} signals_total={len(signals)} elapsed={time.time()-t0:.1f}s",
              file=sys.stderr)
    if args.all_recent is not None:
        for s in signals:
            if s["_age"] < args.all_recent:
                s.pop("_age"); print(json.dumps(s))
        return
    sp = cfg["state_file"]
    sp = sp if os.path.isabs(sp) else os.path.join(HERE, sp)
    state = json.load(open(sp)) if os.path.exists(sp) else {"seen": {}}
    now = datetime.now(timezone.utc)
    win = cfg["report_window_bars"]
    new = []
    for s in signals:
        if s["_age"] >= win or s["id"] in state["seen"]:
            continue
        state["seen"][s["id"]] = s["close_time_utc"]
        s.pop("_age"); new.append(s)
    cutoff = (now - timedelta(days=cfg.get("state_retention_days", 120))).isoformat()
    state["seen"] = {k: v for k, v in state["seen"].items() if v >= cutoff}
    state["last_run_utc"] = now.isoformat(timespec="seconds")
    state["last_sources"] = sources
    tmp = sp + ".tmp"
    json.dump(state, open(tmp, "w"), indent=1, sort_keys=True)
    os.replace(tmp, sp)
    if not args.prime:
        for s in new:
            print(json.dumps(s))
    if errors and not signals:
        sys.exit(2)


if __name__ == "__main__":
    main()
