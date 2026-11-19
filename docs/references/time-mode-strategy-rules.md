---
name: time@mode trading techniques
description: >-
  Use this when analyzing a crypto chart, spotting or checking a trade setup,
  backtesting, or coding a bot with the time@mode techniques (trend and modes,
  mode expiry, ATR and expansion-candle confirmations, timeframe in control,
  20-bar rule, 5x timeframe jumps, trading blocks, 70 SMA filter).
---
# time@mode trading techniques

A multi-timeframe trend, mode, and breakout system for crypto spot and futures. You're in the business of exploiting price movements: read the trend, draw the modes, wait for a confirmation, mark the level on the higher timeframe, and enter on the lower one.

## Part A: The time@mode method (trend, modes, confirmations)

The source notes are in Spanish. A *modo* (mode) is a **flat horizontal line** set at one candle's wick, either the highest low or the lowest high inside the current trend range. It extends across the consolidation and has a lifespan measured in candles.

### Step 1: Establish the trend
- Mark the highest and lowest point of the current trend.
- Lower highs and lower lows mean a downtrend.
- Higher highs and higher lows confirm an uptrend.

### Step 2: Draw the modes
- Draw each mode as a horizontal line at a candle's wick: the higher low (bullish) or the lower high (bearish).
- Only use highs and lows inside the established range.
- In an uptrend, modes start from a low. In a downtrend, they start from a high.
- A swing high with no new highs for 5 bars, or a swing low with no new lows for 5 bars, also counts as a mode anchor, even against the main bias.
- Modes on the example charts spanned 5 to 14 bars.

### Step 3: Mode expiry
- A mode lasts as many candles as it connects. A mode spanning N candles expires N candles later.
- How to count:
  - If the confirming candle's body doesn't cross the mode, that candle is #1.
  - If its body touches or crosses the mode, counting starts on the next candle. That candle is still part of the mode and is also the confirmation.
- When a mode expires, one of two things happens:
  1. Price returns to the mode's starting point, or
  2. Price consolidates for at least as long as its previous consolidation.
- On the example charts, expiry candles lined up with tops, bottoms, and turning points. One example: a 14-bar mode expired exactly at the trend low.

### Step 3b: Confirmations
Any of these confirms a break of the mode:
1. **ATR expansion close:** an expansion candle in the expected direction closes beyond the mode by at least 0.7 x ATR(14), using TradingView's default RMA smoothing and the previous candle's ATR value. Since the mode is flat, measure the distance as `close - modePrice` (bullish) or `modePrice - close` (bearish). On the charts, closes 0.13 to 0.32 ATR past the mode were ignored, and closes of 0.72 ATR or more counted. 0.7 is a tunable parameter.
2. **Close outside the range:** the expansion candle closes outside the range.
3. **Clear-gap candle:** a large candle whose low (bullish) or high (bearish) doesn't touch the mode. Its body is at least 60% of its high-to-low range, and it makes a higher high and higher low (bullish), or a lower high and lower low (bearish), than the previous candle.

### Invalidation and bias flip
- If a candle confirms a break of the mode and the next candle is an expansion engulfing candle that closes back beyond the mode the other way, the setup is invalidated and the bias flips. On the example, the flip candle closed only about 0.22 ATR past the mode, so no ATR margin seems to be required for a flip.

### Rule 4: Find the timeframe in control
- Once the modes get small and the trend keeps going, re-evaluate which timeframe is in control and find that timeframe's mode.
- Move up a timeframe and start from scratch (for example daily, then weekly).
- Valid modes are 5 to 20 bars long. If they're too large or unclear, go up again.
- On a higher timeframe, a mode that ends slightly off the trend's end (for example by one week on the weekly) is fine.

## Part B: Breakout and trading-block rules

### Core principles
- Understand the emotional moves. Volatility inside a range usually means the range is ending, price is stale, or participants are trapped on both sides.
- Never fade a higher-timeframe (HTF) breakout or retake.
- Mark levels on the HTF and enter on the lower timeframe (LTF).
- Focus your trading on the setups where you make the most money.

### Rules
1. Never fade a high-timeframe breakout.
2. **Rule of 5x magnitude:** the HTF is roughly 5x the LTF, rounded to standard exchange intervals. The charts use 4h to 1D, 1D to 6h, 6h to 1h, 6h to 30m, and 1D to 1W, so the actual steps range from about 4x to 12x.
3. **Trend filter:** take longs above the 70 SMA (a simple average of closes) and shorts below it. The notes say H6, but the charts show the 70 SMA on each chart's own timeframe.
4. **20-bar rule:** a consolidation longer than 20 bars is too noisy, so move up a timeframe.
5. Expansion candles add weight but aren't required. On one example, the entry candle was small.
6. Use expansion candles to move the stop.
7. **Entry trigger:** the first LTF close above (long) or below (short) the trading block.

### Definitions
- **Expansion (Exp) candle, for timeframes below 6H:** the body is bigger than the previous candle's high-to-low range.
  - Bullish: `close - open > prevHigh - prevLow`. Bearish is the mirror image.
  - Refinement: `abs(close - open) > (high - low) * 0.60`
- **ATR:** ATR(14) with TradingView's default RMA smoothing.
- **Trading block / order block:** the highest candle **close** in a higher-timeframe range, drawn flat at the close, not the wick.
- **Swing low / high:** a low not undercut, or a high not exceeded, for the next 5 bars. Swing and structure levels are drawn at the wicks.
- **Market structure break:** a previous swing high breaks while coming out of a downtrend (mirror case for bearish).

### Expansion candle range play
After a large move followed by sideways consolidation, bid within the expansion candle's range, and cut the trade if price closes below that candle. Big expansion candles also mark the range high or low.

### Consolidation and range process
1. Find the swing point (5 bars with no new lows or highs).
2. Classify the market as trending or consolidating using market structure breaks.
3. Pick the timeframe. With more than 20 bars in the consolidation, move up and use the highest close. With 20 or fewer, mark the first trading blocks.
4. Drop down for entries: an LTF close beyond the trading block, above the 70 SMA.
5. Manage and repeat, stepping down for entries while the range stays under 20 bars.

### Exit strategy
- Exit on a close back inside the trading block, or the stricter version: two lower lows closing below the entry level.
- Re-enter when a big candle takes the level back.
- Trail the stop with expansion candles.

## Still open (confirm with the strategy owner before automating)
- Where the initial stop goes. No chart shows one.
- Position sizing and risk per trade.
- Whether the 70 SMA filter always uses 6h or the entry chart's own timeframe.
- How strict the 0.7 ATR threshold is. One weekly confirmation counted at about 0.3 ATR.
- Which wick to anchor a mode on when there are several candidates.
- Whether a small or doji candle can confirm a mode. One example that did later failed.
- What the unlabeled "R.E.Signal V3.3" indicator and its blue and grey triangles compute. The blue triangles mostly sit under candles that closed above the previous high.
- How Part A modes and Part B trading blocks combine into a single entry rule.

## Reference material
The example charts and a per-chart analysis are on the box at `/workspace/timemode/chart-analysis.md` and `/workspace/timemode/charts/`.
