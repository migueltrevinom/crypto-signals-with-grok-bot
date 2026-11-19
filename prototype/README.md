Copied here from Miguel's scanner so the detection logic is not lost. The API does not import this folder yet. The port is roadmap phase 1, and these files stay the behavior reference. Run the commands below from this directory. The chart study this README mentions is `docs/references/chart-analysis.md`.

# time@mode scanner

Turns Miguel's time@mode rules (skill: `time-mode-trading-techniques`, evidence: `../chart-analysis.md`)
into a deterministic scanner over live Binance spot data. Python 3 + numpy, no API keys.

## Run
```
python3 scan.py                  # NEW signals only, one JSON object per line (nothing if none); updates state.json
python3 scan.py --all-recent 3   # every signal from the last 3 closed bars per timeframe, ignores state (review)
python3 scan.py --prime          # record current signals in state.json without printing
python3 scan.py --verbose        # + data source and timing on stderr
python3 scan.py --symbols BTCUSDT --timeframes 1d,1w
python3 validate.py              # replay the documented chart examples (results in validation_results.txt)
```
"New" means: not in state.json, and the signal's candle is within the last `report_window_bars` (3)
closed bars of its timeframe. So a schedule of every 15–60 min never misses a signal and never repeats
one. Exit code 2 only if every data request failed.

A full scan of 4 symbols × (1h, 6h, 1d, 1w + 15m for entries) is 20 requests and takes about 4–8 s.

## Data
`data_sources` is tried in order per request: `binance` (api.binance.com, which works from the box) →
`binance_vision` (data-api.binance.vision) → `bybit` (v5 spot) → `okx` (history-candles, UTC-aligned bars).
All were tested and return the same bar open times. Only **closed** candles are used: the still-forming
candle is dropped.

## Signal fields
`type` (mode_confirmed | bias_flip | mode_expiry | block_breakout_entry | exit), `symbol`, `timeframe`,
`direction` (bullish/bearish for modes, long/short for blocks), `close_time_utc`, `close_time_edmonton`,
`price` (close), `level` + `level_kind` (mode | block), `atr` (ATR14 RMA of the previous bar), `atr_distance`
(close beyond the level in ATRs, signed so positive = in the signal's direction), `tradingview_url`, `id`.
Extras: for mode_confirmed, `mode_length`, `mode_anchor` (HL = wick low, LH = wick high), anchor/start time,
`confirmations`, `body_crosses_mode`, `projected_expiry_close_utc/edmonton`, `trend`; for blocks, `htf`,
`htf_block_close_utc`, `sma`, `expansion_candle`, `entry_close_utc` (exits).

## How the rules are coded (timemode.py)
- **ATR** is TradingView's `ta.atr(14)` (RMA). Confirmations use the previous candle's ATR. **SMA** is the 70-period SMA of closes.
- **Swings / trend:** a pivot has 5 bars on each side. Trend = up (higher highs and higher lows) / down / range from the last two confirmed swings, with "structure break" when the close crosses the last swing extreme. Reported as context on mode signals.
- **Mode:** a flat line at one candle's wick (a low or a high) inside the last ≤20 bars ending at the bar before the confirming candle. A candle is "connected" if the line lies within its high–low range (±0.02 ATR). **Mode length = number of connected candles**, which is how the charts' 8/14/12/6/5 counts come out. The span must start and end on a connected candle, at least 75% of the span's candles must touch, and the length must be 5–20. Among valid lines the confirming candle breaks, the scanner picks the longest mode, then the longest span, then the line nearest the close.
- **Confirmation** (any one; recorded in `confirmations`):
  1. `atr_expansion`: an expansion candle in the direction that closes ≥0.7×ATR(prev) beyond the line.
  2. `close_outside_range`: an expansion candle that closes beyond the span's extreme.
  3. `clear_gap`: body ≥60% of range, higher high and higher low (or lower high and lower low), and the wick doesn't touch the line.
  An expansion candle has body > previous candle's range OR body ≥60% of its own range (`expansion_rule`). A level only confirms once: an earlier expansion close ≥0.7 ATR beyond it (after its anchor printed) blocks it.
- **Expiry:** the expiry candle is #length, counted from the confirming candle (#1) or from the next candle (see `body_cross_count_rule`). `expiry_bar_made_new_extreme` flags when the expiry candle prints the extreme of the move (the Oct 19 2021 case).
- **Bias flip:** within 3 bars after a confirmation, an engulfing expansion candle that closes back beyond the line the other way. No ATR margin is required (the chart example was 0.22 ATR). Flipped modes don't emit an expiry.
- **Trading block** (HTF = the scanned timeframe): the highest close of the last 20 HTF bars, once ≥2 bars have closed under it (the lowest close mirrors this for shorts). A block stays active for 30 HTF bars, and a new block within 0.25 ATR of an existing one is ignored. Entry happens on the LTF (1w→1d, 1d→6h, 6h→1h, 1h→15m): the first LTF close beyond an active block (the previous close was on the other side), with the close on the right side of the LTF 70 SMA. While a position is open, only a further block triggers a new entry (and moves the exit level).
- **Exit:** two consecutive LTF closes back below the entry block, with successively lower lows (mirrored for shorts). Re-entry is allowed on the next reclaim.

## Defaults chosen for ambiguous rules (all in config.json → params)
| Open question | Default | Option(s) |
|---|---|---|
| Which wick anchors the mode | the most-connected wick level (5–20 candles, ≥75% density) | `mode_touch_density`, `mode_touch_tol_atr` |
| Body-crossing confirming candle: #1 or "part of the mode"? | per timeframe: `confirm_bar` (daily and below), `part_of_mode_next_bar` (1w). The daily charts (Sep 17, Apr 14, Apr 20) count the candle as #1, while the weekly charts (Mar 29, Apr 12, Jun 7) count it in the mode and start on the next bar, as the "punto importante" note says | `body_cross_count_rule`: `confirm_bar` / `next_bar` / `part_of_mode_next_bar`, or a {"default":…, "1w":…} dict |
| How strict is 0.7 ATR | strict 0.7 (Apr 12 2021 weekly at 0.31 ATR will be missed) | `confirm_atr_mult` |
| Small or doji confirmation candles | not accepted (clear_gap needs body ≥60%) | `body_range_ratio`, `confirm_types` |
| Expansion definition | either of the two definitions in the notes | `expansion_rule`: either / prev_range / self_ratio / both |
| Flip window and margin | 3 bars, engulfing + expansion, no ATR margin | `flip_window_bars`, `flip_requires_*` |
| SMA filter timeframe | the entry chart's own timeframe (what the charts show) | `sma_filter_timeframe`: entry / htf / "6h" |
| Block range and lifetime | last 20 HTF bars, ≥2 bars after the block, 30-bar lifetime, merge within 0.25 ATR | `consolidation_limit`, `block_min_bars_after`, `block_ttl_bars`, `block_merge_atr` |
| Exit | two lower closes below the block | `exit_rule`: two_lower_closes / close_back_inside |
| Shorts | on | `enable_shorts` |
| Stop-loss / sizing | **not implemented** (no chart shows one) | (none) |
| How Part A and Part B combine | emitted as independent signal types | (none) |
| R.E.Signal V3.3 indicator | not used | (none) |

## Validation (python3 validate.py)
18 of 23 documented checks reproduced, using Binance history (ETHBTC 1D/1W 2021, ARBBTC 1D/6h/1h Dec 2023, ETHUSDT 6h/30m Feb 2024).
See validation_results.txt for the exact output.

## Files
`scan.py` CLI · `timemode.py` rules · `data.py` fetch and fallback · `config.json` · `state.json` (seen ids, 120-day retention) · `validate.py`.
