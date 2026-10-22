# time@mode strategy specification

This is the implementable form of Miguel's notes and the chart study. The prose notes are [time-mode-strategy-rules.md](references/time-mode-strategy-rules.md). The chart-by-chart evidence is [chart-analysis.md](references/chart-analysis.md). The code that already scores 18 of 23 documented checks is `prototype/timemode.py`.

## Precedence

When sources disagree, use this order until Miguel closes the question:

1. A direct answer from Miguel to an open question below.
2. A chart outcome in `docs/references/chart-analysis.md` that the notes and the code both already match.
3. `prototype/timemode.py`, as checked by `prototype/validate.py` (18/23, snapshot in `prototype/validation_results.txt`).
4. The prose notes.

Do not change the port to pick up the five missed checks unless the matching question is answered. Those misses are part of the baseline, not a punch list.

## Scope

Spot first. Futures uses the same functions later, on futures candles, and is not a second rule set. Arbitrage has no rules and is not specified here.

The bot does not place orders. It emits signals. Part A (modes) and Part B (trading blocks) are independent streams. Nothing in the prototype requires a mode confirmation before a block entry, or the reverse.

The scanner does not choose "the timeframe in control". The watchlist names the timeframes. The 20-bar limit is the lookback inside a timeframe (`consolidation_limit`), not an automatic jump to the next timeframe. Rule 4 from the notes (modes get small, move up a timeframe) is an open product question, not v1 behavior.

## Market data the detector assumes

- Candles are closed. The forming candle is dropped. Close time is open time plus the interval.
- Intervals: `15m`, `30m`, `1h`, `4h`, `6h`, `1d`, `1w`. Week and day boundaries match what Binance, Bybit, and OKX returned in the prototype (the same open times across those sources).
- ATR is TradingView `ta.atr(14)`: true range, Wilder/RMA, seeded with the SMA of the first 14 true ranges. Confirmations use the previous candle's ATR.
- SMA is the simple average of closes, length 70. Not an EMA. The chart fit was SMA 70 on that chart's own timeframe.
- A higher timeframe is "known" to a lower timeframe only after the HTF candle has closed (`htf.close_time <= ltf.open_time`).

## Signal types

| `type` | `direction` | `level_kind` | Meaning |
| --- | --- | --- | --- |
| `mode_confirmed` | `bullish` or `bearish` | `mode` | A mode broke on this candle |
| `bias_flip` | opposite of the mode | `mode` | Engulfing expansion back through the mode |
| `mode_expiry` | same as the mode | `mode` | The mode's counted lifespan ended on this candle |
| `block_breakout_entry` | `long` or `short` | `block` | First LTF close through an active HTF block, on the right side of the SMA |
| `exit` | `long` or `short` | `block` | Exit rule hit for an open block entry |

`signal_id`, field list, and `details` keys are in [data-model.md](data-model.md). They must stay stable so stored ids match the prototype.

Default ladder (`ltf_map`), used when a block is marked on the HTF and the entry is on the LTF:

| HTF | LTF |
| --- | --- |
| `1w` | `1d` |
| `1d` | `6h` |
| `6h` | `1h` |
| `1h` | `15m` |

Charts also used 4h→1d and 6h→30m. Those are not in the default map. A watchlist can add timeframes; it cannot express 6h→30m unless `ltf_map` is overridden. That override is allowed in the data model and is off by default.

## Part A — modes

### Trend context

A swing high (low) is an extreme versus `swing_lookback` bars on each side (default 5), confirmed that many bars later. Trend at bar `i` uses the last two confirmed swing highs and lows: up when both are rising, down when both are falling, otherwise range. A close through the last swing extreme overrides that to `up (structure break)` or `down (structure break)`. With fewer than two swings on either side the trend is `unknown`.

Trend is stored on the signal. It does not accept or reject a mode in the prototype. Counter-trend anchors are allowed, which matches the notes (a 5-bar swing can anchor a mode against the main bias).

### What a mode is

A mode is one horizontal price: a candle's wick low (`mode_anchor=HL`) or wick high (`LH`) inside a window of at most `consolidation_limit` bars (20) ending on the bar before the candidate confirmation. It is not a slope.

A candle in that window is connected when the level lies in `[low - tol, high + tol]`, `tol = 0.02 * ATR` of the previous bar (`mode_touch_tol_atr`).

A candidate span must:

- start and end on a connected candle,
- have at least `mode_touch_density` (0.75) of its candles connected,
- have a connected count (`mode_length`) from `mode_min_bars` (5) through `mode_max_bars` (20).

`mode_length` is the number of connected candles, which is how the charts' 8, 14, 12, 6, and 5 counts come out. On weekly bars, when `body_cross_count_rule` is `part_of_mode_next_bar` and the confirming body overlaps the level, that confirming candle adds one to the length.

Among candidates the confirming candle actually breaks, pick the longest length, then the longest span, then the level closest to the close.

A level confirms at most once. If an earlier expansion candle, after the anchor wick printed, already closed at least `confirm_atr_mult` ATR beyond that level, the level is consumed. A later confirmation of a level within 0.5 ATR of an already-consumed same-direction level whose span overlaps is skipped.

### Confirmation

The candidate candle must close beyond the level in its own direction (bullish close above, bearish close below). Any one of the configured `confirm_types` is enough:

1. `atr_expansion`. The candle is an expansion candle and the close is at least `confirm_atr_mult` (0.7) times the previous ATR past the level. Distance is `close - level` bullish and `level - close` bearish.
2. `close_outside_range`. The candle is an expansion candle and the close is outside the span's extreme (above the span high when bullish, below the span low when bearish).
3. `clear_gap`. The body is at least `body_range_ratio` (0.60) of the candle's range, the candle makes a higher high and higher low (or a lower high and lower low), and the wick does not touch the level (beyond the touch tolerance).

Record every type that matched in `confirmations`.

Expansion (`expansion_rule`, default `either`):

- `prev_range`: directional body greater than the previous candle's high-low range.
- `self_ratio`: directional body at least `body_range_ratio` of its own range.
- `both`: both.
- `either`: either.

The notes give the previous-range test for timeframes below 6h and the 60% body test as a refinement. The prototype accepts either definition on every timeframe. That is the default to port.

Closes of about 0.13 to 0.32 ATR past a mode were not treated as confirmations on the ETHBTC daily chart (4 and 5 Oct 2021). A close of 0.72 ATR was. The strict 0.7 default reproduces that and rejects the 12 Apr 2021 weekly confirmation, which the author marked at about 0.3 ATR. See open questions.

### Expiry

Let the confirming candle be bar `i`. If the body overlaps the level and `body_cross_count_rule` for that timeframe is `next_bar` or `part_of_mode_next_bar`, counting starts at `i + 1`. Otherwise it starts at `i` (the confirming candle is #1).

Default rule object: daily and below use `confirm_bar`; `1w` uses `part_of_mode_next_bar`. That matches Sep 17 and Oct 6 2021 (daily, confirming candle is #1) and the weekly "this expansion confirms but is still part of the mode" notes (29 Mar, 12 Apr, 7 Jun 2021).

The expiry bar is `count_start + mode_length - 1`. When that bar exists, emit `mode_expiry`. `expiry_bar_made_new_extreme` is true when a bearish expiry prints the lowest low from the confirmation through the expiry bar, or a bullish expiry prints the highest high. The 19 Oct 2021 daily expiry is that case (low 0.059323).

If a bias flip happened and `expiry_after_flip` is false (the default), do not emit expiry for that mode.

### Bias flip

Look at the next `flip_window_bars` candles (3), not counting the confirmation. The first candle that meets all of the following flips the bias:

- It closes back beyond the level in the opposite direction. There is no ATR minimum. The chart example is about 0.22 ATR (20 Oct 2021).
- If `flip_requires_expansion` (true): its directional body is greater than the previous candle's high-low range. This check does not call the shared `expansion_rule`. It is previous-range only.
- If `flip_requires_engulfing` (true): its body engulfs the previous candle's body.

Emit `bias_flip` with the opposite direction. One flip per confirmation.

## Part B — trading blocks

Evaluated per HTF series. Entries and exits are on the mapped LTF.

### Block definition

On each HTF bar, look back `consolidation_limit` closes (20).

- Long block: the highest close in that window.
- Short block: the lowest close. Shorts are on when `enable_shorts` is true.

The block price is that close, not the wick. The chart examples (ARBBTC daily 0.00003014 on 12 Dec 2023, ARBBTC 6h 0.00003227 on 22 Dec 2023 18:00 UTC, ETHUSDT 6h about 2503.20) are closes.

The prototype activates a block once `block_min_bars_after` (2) further HTF bars have printed. It does not check that those bars closed back inside the level. The notes and the prototype's own comment say the bars closed under (or above) the block. The code only counts elapsed bars. Port the code. The question is open.

A new block within `block_merge_atr` (0.25) times ATR of an existing same-direction block is ignored. A block stays active for `block_ttl_bars` (30) HTF bars after its own bar, so it can be broken, lost, and reclaimed.

### Entry

On the LTF, in order:

1. Resolve exits for any open position on this bar first.
2. The LTF close must be on the correct side of the SMA filter: above SMA for a long, below for a short. Default `sma_filter_timeframe` is `entry`, meaning the LTF's own SMA 70. `htf` uses the HTF SMA. Any other value is a timeframe name whose SMA is sampled at the LTF bar. The charts show the SMA of the chart being looked at (6h SMA on the 6h chart, 1h SMA on the 1h chart). The notes say H6. The default follows the charts.
3. The previous LTF close was on the other side of an active block and this close is beyond it.
4. If a position in that direction is already open, the new block must be further out (higher for longs, lower for shorts). That entry replaces the exit level.

Expansion is not required. The ETHUSDT 30m entry on 10 Feb 2024 19:30 America/Edmonton (11 Feb 00:30 UTC) is a small candle. `expansion_candle` is recorded and is not a gate.

When several blocks are crossed on the same bar, take the furthest one in the trade direction.

### Exit

`exit_rule` default `two_lower_closes`:

- This close and the previous close are back inside the entry level (below it for a long, above it for a short).
- The previous bar is after the entry bar.
- For a long, `low[j] < low[j-1]` and `low[j-1] < low[j-2]`. Shorts mirror that with highs.

So the code requires two closes inside the level and a three-bar run of lower lows (higher highs for shorts). The chart callout says "two consecutive lows / both close below the entry level". Whether the third low is required is open. Port the code.

`close_back_inside` is the looser option: one close back through the level. It is not the default.

After an exit the position is flat, so a later reclaim can enter again. The ETH 30m chart shows that re-entry.

## Defaults that are choices, not chart laws

All of these live in `strategy_configs.params` and can change without a code edit. The values are the prototype's.

| Question the notes leave open | Default we will port |
| --- | --- |
| Which wick is the mode | The candidate with the longest connected length, then the longest span, then the nearest close, among levels the confirmation actually breaks, with 75% density and 0.02 ATR tolerance |
| Body-cross candle is #1 or part of the mode | `confirm_bar` except `1w`, which uses `part_of_mode_next_bar` |
| How strict is 0.7 ATR | Strict 0.7. The 12 Apr 2021 weekly (~0.31 ATR) stays a miss |
| Doji or small confirmation | Not accepted. `clear_gap` needs a 60% body. Expansion needs a real body |
| Expansion definition | Either previous-range or 60% of own range |
| Flip window and margin | 3 bars, engulfing, previous-range expansion, no ATR margin |
| SMA timeframe | The entry timeframe's own SMA 70 |
| Block window, wait, life, merge | 20 bars, 2 bars after, 30-bar life, merge inside 0.25 ATR |
| Exit | `two_lower_closes` as implemented |
| Shorts | On |
| Stop and size | Not implemented |
| Part A plus Part B | Separate signal types |
| R.E.Signal V3.3 and the triangle markers | Not used |

## Validation baseline

`python3 prototype/validate.py` replays ETHBTC, ARBBTC, and ETHUSDT history. The checked-in score is 18/23. These passed and must keep passing after the port:

- ETHBTC 1D mode 1, 17 Sep 2021 bearish, length 8, level about 0.07402, expiry 24 Sep 2021, about 0.72 ATR.
- 4 Oct and 5 Oct 2021 are not confirmations.
- ETHBTC 1D mode 2, 6 Oct 2021 bearish, length 14, level about 0.06918, expiry 19 Oct 2021, and that expiry candle's low is 0.059323 with `expiry_bar_made_new_extreme`.
- ETHBTC 1D mode 3, 18 Oct 2021 bearish, length 8, level 0.06245, about 0.73 ATR.
- 20 Oct 2021 bullish engulfing bias flip, about 0.22 ATR.
- ETHBTC 1D bullish 12-bar and 6-bar modes expiring 25 Apr 2021.
- ETHBTC 1W 29 Mar 2021 bullish, level about 0.0314, length 6, expiry 10 May 2021.
- ETHBTC 1W 7 Jun 2021 bearish, level about 0.0735, length 5, expiry 12 Jul 2021.
- ARBBTC daily block 0.00003014, 6h long entry 22 Dec 2023 06:00 UTC, expansion candle.
- ARBBTC 6h block 0.00003227, 1h long entry on 27 Dec 2023.
- ETHUSDT 6h block about 2503.2, 30m entry 11 Feb 2024 00:30 UTC, an exit early on 12 Feb, and a re-entry 12 Feb 14:30 UTC.

These failed and stay failed under the current defaults:

- ETHBTC 1D bearish 9-bar mode expiring 28 Feb 2021. Not found.
- ETHBTC 1D bullish 6-bar mode expiring 11 Mar 2021. Not found.
- ETHBTC 1D bullish 5-bar and 6-bar modes expiring 2 Apr 2021. Not found.
- ETHBTC 1W 12 Apr 2021 bullish mode at about 0.03848, length 5, expiry 17 May 2021. Not found. The close was only about 0.3 ATR past the mode, under the 0.7 default.

The Feb–Apr daily misses are not explained by the 0.7 threshold alone. The detector found other confirmations in that window (listed in `validation_results.txt`) that do not line up with those expiry dates. Treat them as anchor-selection gaps, not as a license to loosen ATR.

## Known prototype limitations to fix in the port, not in the rules

- OKX inst id is `symbol[:-4] + "-USDT"`. That is correct for `BTCUSDT` and wrong for `ETHBTC` / `ARBBTC`. Binance and Bybit pass the symbol through. The port needs a real inst-id map per source.
- `state.json` dedup is replaced by the unique `signal_id` index. Same id formula.
- Fetch uses threads and `urllib`. The port uses the async HTTP client. Candle results for a given closed range must match.

## Open questions

Strategy, for Miguel:

1. Where does the initial stop go? No chart shows one. Below the block, below the expansion candle, below the last swing, or not in the bot at all?
2. Position size and risk per trade are not in the notes. Signals only, until he says otherwise?
3. SMA 70: always 6h, the entry chart's own SMA (what the charts show and what the prototype does), or both?
4. Timeframe ladder: keep the fixed table, or pick the nearest standard interval to 5x? Should 4h→1d and 6h→30m be defaults?
5. Is 0.7 ATR strict? One weekly confirmation was marked at about 0.3 ATR and the prototype misses it on purpose.
6. When several wicks qualify, is "longest, then longest span, then nearest close" the right anchor rule?
7. Can a doji or a small candle confirm when the wick stays beyond the mode (the 19 Oct 2021 discussion)? The prototype says no.
8. What do R.E.Signal V3.3 and the blue/grey triangles compute? Left out until defined.
9. Do Part A modes and Part B blocks ever combine into one entry, or do they stay two signal streams?
10. Exit: two closes back inside the level, or the stricter three-bar lower-low sequence the code uses? Which two ETH 30m candles are the callout?
11. Is the body-cross count really "daily confirming candle is #1, weekly confirming candle is part of the mode"?
12. Block activation: must the next bars close back inside the block, or is waiting two bars enough (what the code does)?
13. Bias-flip expansion ignores `expansion_rule` and always uses previous-range. Should it use the same expansion definition as confirmations?
14. Should the bot ever move itself up a timeframe when a consolidation exceeds 20 bars (Rule 4), or only scan the watchlist?
15. Direction labels: keep `bullish`/`bearish` on modes and `long`/`short` on blocks, or use one pair?

Product, for Miguel:

16. How long should signals and scan runs be kept? Proposal: keep signals, delete scan runs after 90 days.
17. Where will API, worker, and Mongo run?
18. First alert channel is a webhook. Is Telegram, email, or something else required for the first useful version?
19. One shared API key is the plan. Are there other users?
20. Symbol universe: USDT pairs only, or also BTC pairs like the chart examples? The port will support both on Binance-style symbols either way.
21. Futures: which exchange and contract (USDT-M, coin-M), and does a signal open a tracked position or only an alert?
22. Arbitrage: cross-exchange spot, funding, triangular, or something else? No module work until this is written down.
23. Should the GitHub default branch stay `main`, or move to `development` once this PR is merged? Should `main` later mirror `production`?
