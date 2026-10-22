# time@mode strategy specification

This is the implementable form of Miguel's notes and the chart study. The prose notes are [time-mode-strategy-rules.md](references/time-mode-strategy-rules.md). The chart-by-chart evidence is [chart-analysis.md](references/chart-analysis.md). The code that already scores 18 of 23 documented checks is `prototype/timemode.py`.

## Precedence

When sources disagree, use this order until Miguel closes the question:

1. A direct answer from Miguel to an open question below.
2. A chart outcome in `docs/references/chart-analysis.md` that the notes and the code both already match.
3. `prototype/timemode.py`, as checked by `prototype/validate.py` (18/23, snapshot in `prototype/validation_results.txt`).
4. The prose notes.

Do not change the port to pick up the five missed checks unless the matching question is answered. Those misses are part of the baseline, not a punch list.

## Resolved decisions

Miguel answered these. They override the prototype and the chart pixels where they differ. The seed values live in `Core/planning_seeds.py` and are specified as Mongo documents in [repositories.md](repositories.md).

| Topic | Decision |
| --- | --- |
| Signals only | No. The system plans stops and position size. Settings are Mongo `risk_profiles`, per user, strategy, and symbol. The bot still does not send orders. |
| 70 SMA filter | Always the 6h SMA of closes, length 70, whatever timeframe the entry is on. Longs need price above it. Shorts need price below it. |
| Timeframe in control | Chosen dynamically on the ladder `4h`, `6h`, `8h`, `1d`, `3d`, `1w`, `1M`. The old fixed map `1w→1d→6h→1h→15m` is retired. `15m`, `30m`, and `1h` are not scan timeframes. |
| Missing venue bars | Resample onto Binance's grid from a lower native timeframe. Coverage is in the Exchanges section of the repositories doc. |
| Modes and blocks | They combine. A confluence score on the weekly, 3-day, and daily charts produces one entry plan, then the entry timeframe is chosen below that. |
| Symbols | USDT quotes are preferred. The monitored set is the `symbols` collection: any quote asset, any enabled venue, with tags and priority. |
| Alerts | The Grok Bot polls `GET /api/v1/alerts/feed` and acks `delivered` or `acked`. Webhooks and email are later pluggable kinds. |
| Arbitrage | Cross-venue between CEXes (Binance, Bybit, OKX, Coinbase, Kraken) and DEXes. Record the opportunity net of fees, slippage, and transfer or gas. Place no orders. |

## Scope

Spot is the first market. Futures uses the same detection functions on futures candles. It is not a second rule set. Contract type (USDT-M, coin-M, hedge mode) is still open. Arbitrage is specified as a detection domain in [repositories.md](repositories.md), not as a time@mode variant.

The bot does not place orders. It stores signals, an entry plan, a sized position with a stop and targets, and an alert row.

Part A (modes) and Part B (blocks) still emit their own signal rows, so the chart replay stays comparable. The live entry is the confluence plan that reads both, not either stream alone.

## Market data the detector assumes

- Candles are closed. The forming candle is dropped. Close time is open time plus the interval.
- The ladder, stored in Mongo, is `4h`, `6h`, `8h`, `1d`, `3d`, `1w`, `1M`.
- Where a venue lacks one of those bars, MarketData resamples from a lower native timeframe. Alignment is Binance's grid, including Monday 00:00 UTC weeks and calendar months. Details are in the repositories doc.
- ATR is TradingView `ta.atr(14)`: true range, Wilder/RMA, seeded with the SMA of the first 14 true ranges. Confirmations use the previous candle's ATR.
- The trend filter is the 6h SMA of closes, length 70. Not an EMA. Not the entry timeframe's own SMA. The chart study measured SMA 70 on whatever chart was open (the 1h chart was the 1h SMA). Miguel's answer replaces that: every entry, including a 4h or 8h entry, uses the 6h SMA.
- A higher timeframe is known to a lower one only after the higher candle has closed (`htf.close_time <= ltf.open_time`).

## Signal types

| `type` | `direction` | `level_kind` | Meaning |
| --- | --- | --- | --- |
| `mode_confirmed` | `bullish` or `bearish` | `mode` | A mode broke on this candle |
| `bias_flip` | opposite of the mode | `mode` | Engulfing expansion back through the mode |
| `mode_expiry` | same as the mode | `mode` | The mode's counted lifespan ended on this candle |
| `block_breakout_entry` | `long` or `short` | `block` | First close through an active block, on the right side of the 6h SMA |
| `exit` | `long` or `short` | `block` | Exit rule hit for an open block position |

`signal_id` and the stored fields stay as in [data-model.md](data-model.md) so the prototype hash still matches. `details.sma_timeframe` is `6h` on block entries.

These rows are inputs. The thing the bot acts on is an `entry_plan` from the confluence engine, then a `positions` document. Those are not signal types, so a confluence change does not rewrite old signal ids.

## Timeframe in control

Rule 4 from the notes is now this procedure. It runs on the ladder from low to high.

For each timeframe, using only closed candles:

1. Run the mode detector.
2. Take the best mode whose span ends on the last closed bar or whose confirmation is still inside its expiry window.
3. The timeframe **fails as too noisy** when the current consolidation is longer than 20 bars (the same `consolidation_limit`).
4. The timeframe **fails as too small** when that best mode's length is under 5, or the touch density is under `mode_touch_density`.
5. The timeframe **fits** when the mode length is from 5 through 20 and it did not fail the density check.

The timeframe in control is the lowest ladder timeframe that fits. If 4h fits, 4h is in control. If 4h is too noisy, try 6h, then 8h, and so on. `1M` is the ceiling: if nothing below it fits, `1M` is in control and confluence marks the plan low-confidence when the monthly mode itself does not fit.

"Unclear" means density below the threshold, or two opposite modes within one bar of the same length. An unclear timeframe does not fit, and the search moves up.

The result is `{timeframe, reason}` with `reason` of `fit`, `stepped_up`, or `ceiling`. It is stored on the entry plan and the position. It is not a signal type.

## Confluence and the entry decision

Modes and blocks combine here. Weights and thresholds are the `confluence_configs` document. The seed is in `Core/planning_seeds.py`.

The worker passes in, per symbol and per direction (`long` from bullish modes, `short` from bearish modes):

- mode confirmations and block breaks on each ladder timeframe, from the detector
- the timeframe in control and its mode direction
- whether the latest 6h close is above or below the 6h SMA 70

Score for one direction:

- Add `weights.mode_confirmed[tf]` for each decision or ladder timeframe that has a `mode_confirmed` in that direction whose expiry window still covers the latest bar.
- Add `weights.block_break[tf]` for each timeframe with a `block_breakout_entry` in that direction on a still-active block.
- Add `weights.sma_6h_agreement` when the 6h close is on the correct side of the 6h SMA.
- Add `weights.timeframe_in_control_agreement` when the timeframe in control's mode direction matches.
- Subtract `weights.htf_conflict_penalty` when any two of `1w`, `3d`, and `1d` have confirmations in opposite directions.

`require_sma_6h` true means a failing SMA check zeros the score. The seed is true.

Thresholds: `watch` (5) stores nothing by itself. `entry` (8) is the minimum to propose a plan. At least one of `1w`, `3d`, or `1d` must have contributed a mode or a block point in that direction. A lower-timeframe-only score does not enter, even if the number clears 8. That is the "confirm on the weekly, 3-day, and daily, then drill down" rule. One of the three is enough to pass the gate. More of them raise the score through the weights. Weekly is weighted highest on purpose.

Entry timeframe, once the score clears `entry`:

1. Consider `entry_timeframes` (`4h`, `6h`, `8h`) that are strictly below the lowest decision timeframe which contributed points.
2. Keep those that have a fresh trigger on their latest closed bar: a mode confirmation or a block break in the same direction, and a local mode length from 5 to 20.
3. Pick the first remaining name in `entry_timeframe_priority` (`4h`, then `6h`, then `8h`).
4. If none of the entry timeframes qualify, the entry timeframe is the lowest decision timeframe that contributed points. The plan does not invent a 1h or 30m entry. Those charts in the study stay historical evidence for what a block and an exit look like.

The plan's direction is `long` or `short`. The underlying mode signals keep `bullish` and `bearish` so the replay ids do not change.

A plan expires when a newer closed bar on the entry timeframe no longer holds the trigger. The worker sets `expired`. It does not delete the row.

## Part A — modes

### Trend context

A swing high (low) is an extreme versus `swing_lookback` bars on each side (default 5), confirmed that many bars later. The signal's `candle_close_time` is that confirming bar. The pivot bar is stored as context and is not the time the signal is credited or published. Trend at bar `i` uses the last two confirmed swing highs and lows: up when both are rising, down when both are falling, otherwise range. A close through the last swing extreme overrides that to `up (structure break)` or `down (structure break)`. With fewer than two swings on either side the trend is `unknown`.

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

Evaluated on each ladder timeframe. The old one-step LTF map is not used. A block on a timeframe is a component of the confluence score. The entry bar is chosen by the entry-timeframe rule above, and it still has to be a real close through that block (or through the mode) on that entry timeframe.

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
2. The close must be on the correct side of the **6h** SMA 70: above for a long, below for a short. This is `sma_filter_timeframe: "6h"` and it does not follow the entry timeframe. The 1h chart in the study showed a 1h SMA. That observation stands, and the live rule is the 6h SMA anyway, because that is the answer Miguel gave. The prototype's `entry` setting is not ported.
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
| SMA timeframe | **Resolved: always 6h SMA 70.** The prototype's `entry` value is not the live rule |
| Block window, wait, life, merge | 20 bars, 2 bars after, 30-bar life, merge inside 0.25 ATR |
| Exit | Seeded as `two_lower_closes` on the risk profile. The three-bar low sequence in the code is still an open reading of the chart callout |
| Shorts | On |
| Stop and size | **Resolved: stored on `risk_profiles`.** Seed is `below_structure` with a 0.25 ATR buffer, 1% of manual equity, trailing by expansion candle, targets at 2R and 3R. Equity itself is unset until he fills it in |
| Part A plus Part B | **Resolved: confluence engine.** Detector rows stay separate. The entry is one plan |
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
- ARBBTC 6h block 0.00003227, 1h long entry on 27 Dec 2023. The live ladder does not scan 1h. This check guards the block detector, not the entry-timeframe chooser.
- ETHUSDT 6h block about 2503.2, 30m entry 11 Feb 2024 00:30 UTC, an exit early on 12 Feb, and a re-entry 12 Feb 14:30 UTC. 30m is not on the live ladder either. Same split: the check guards the exit rule, and live entries are 4h, 6h, or 8h.

The block checks above were scored with the prototype's entry-timeframe SMA. The live filter is the 6h SMA. Re-running those three entries against the 6h SMA is part of the port, and a difference is expected to be reported rather than silently patched back to the old SMA.

These failed and stay failed under the current defaults:

- ETHBTC 1D bearish 9-bar mode expiring 28 Feb 2021. Not found.
- ETHBTC 1D bullish 6-bar mode expiring 11 Mar 2021. Not found.
- ETHBTC 1D bullish 5-bar and 6-bar modes expiring 2 Apr 2021. Not found.
- ETHBTC 1W 12 Apr 2021 bullish mode at about 0.03848, length 5, expiry 17 May 2021. Not found. The close was only about 0.3 ATR past the mode, under the 0.7 default.

The Feb–Apr daily misses are not explained by the 0.7 threshold alone. The detector found other confirmations in that window (listed in `validation_results.txt`) that do not line up with those expiry dates. Treat them as anchor-selection gaps, not as a license to loosen ATR.

## Known prototype limitations to fix in the port, not in the rules

- OKX inst id is `symbol[:-4] + "-USDT"`. That drops any non-USDT quote. The port uses `symbol_style: dash` (`ETH-BTC`, `BTC-USDT`) from the symbol's listing. Kraken is `alias` and is never sliced.
- `state.json` dedup is replaced by the unique `signal_id` index. Same id formula.
- Fetch uses threads and `urllib`. The port uses the async HTTP client. Candle results for a given closed range must match.

## Open questions

Answered, and specified above or in [repositories.md](repositories.md): stops and size as Mongo risk profiles, 6h SMA, the dynamic ladder and resampling, confluence of modes and blocks, the symbols collection, Grok Bot polling, and CEX/DEX arbitrage with no orders.

Still open:

1. Is 0.7 ATR strict? The 12 Apr 2021 weekly confirmation was about 0.3 ATR, and the prototype misses it on purpose.
2. When several wicks qualify, is "longest, then longest span, then nearest close" the anchor rule he wants to keep?
3. Can a doji confirm when the wick stays beyond the mode (19 Oct 2021)? The prototype says no.
4. What R.E.Signal V3.3 and the blue/grey triangles compute. Still unused.
5. Exit seed: the risk profile uses `two_lower_closes`, which in code also requires a three-bar run of lower lows. The chart callout reads as two closes. Which seed should stay?
6. Body-cross counting: daily confirming candle is #1, weekly confirming candle is part of the mode. Is that the rule for 3d, 8h, and 4h as well (treat them like daily)?
7. Block activation: the code waits two bars. The notes say those bars closed back inside the block. Which one?
8. Bias-flip expansion uses previous-range only, not `expansion_rule`. Should those match?
9. Keep `bullish`/`bearish` on mode signals and `long`/`short` on blocks and plans, or one vocabulary?
10. How long to keep signals and scan runs? Proposal: keep signals, drop scan runs after 90 days, drop `venue_quotes` after one day.
11. Where API, worker, and Mongo will run.
12. Futures contract: USDT-M, coin-M, or both, and hedge mode or one-way.
13. Confirm the numeric seeds: 1% equity, 0.25 ATR stop buffer, confluence entry threshold 8, arbitrage `min_net_spread_bps` 0, slippage 5 bps. They are editable in Mongo. Equity is blank until he sets `manual_equity`.
14. Slippage for arbitrage: the seed is a flat bps value. A book-depth model is not specified.
15. Which gas source a DEX quote should use, and which chains besides Ethereum to enable first.
16. The API key is still one shared secret, mapped to a single `users` row. Per-user keys are not specified.
17. Should the GitHub default branch move from `main` to `development` after this PR merges?
