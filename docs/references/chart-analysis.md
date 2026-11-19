# time@mode: TradingView chart analysis

All 21 snapshots referenced in Miguel's two docs were downloaded (none failed) and inspected visually (full view + PIL crops/zooms). Where useful, chart contents were cross-checked numerically against Binance public kline data (ARBBTC 6h/1h, ETHUSDT 6h/30m, ETHBTC 1D/1W) by calibrating the chart pixels against the price axis.

- Local images: `/workspace/timemode/charts/<ID>.png` (full-resolution PNGs from `s3.tradingview.com/snapshots/...`)
- Crops/zooms used: `/workspace/timemode/view/`
- Helper data and scripts: `/workspace/timemode/*.json`, `fitma2.py`, `fit1h.py`, `markers.py`
- Grep of `/workspace/crypto_notes.txt` contains exactly the 9 Doc 1 links listed below (no extra links).

Author on every snapshot: **shemaelohim**. Doc 1 charts: published Feb 14, 2024 (between 18:10 and 18:41 UTC-5, which is 16:10 to 16:41 Edmonton time, MST). Doc 2 charts: published Nov 4, 2021 (12:23 to 13:31 UTC-6, the same clock time in Edmonton because Edmonton was on MDT that day).

Legend: **[seen]** means visible on the chart. **[data]** means verified against Binance kline data. **[inferred]** means my interpretation. **[uncertain]** means not resolvable from the image.

---

## Doc 1: Breakout and trading-block rules (ARB/BTC and ETH/USDT, white background)

Common to Doc 1: the indicator legend is hidden, so no indicator names or lengths are printed. A thin purple MA is drawn on the 6h and 1h charts. Small markers appear above and below candles: blue ▲ under some bullish candles and grey ▼ over some bearish ones. Neither indicator is labeled.

### 1. 9vCwbo5T: swing low example
- Link: https://www.tradingview.com/x/9vCwbo5T/ · File: `charts/9vCwbo5T.png`
- Cited for: an example swing low with no new lows for the next 5 bars.
- Chart: **ARB/Bitcoin, 4h, BINANCE** [seen]. Range: about late Oct 2023 to Jan 8, 2024. Price: about 0.0000200 to 0.0000385 BTC.
- Drawings: one **horizontal red line** at the Dec 6–7, 2023 low (about 0.0000241), extended right to about Dec 24 [seen]. No other annotations, no MA, no markers.
- What it shows: the low on Dec 6–7 is never undercut afterwards. Price ranges above it for about 2 weeks, then breaks out sharply upward around Dec 22. The swing low is marked at the **wick low** and drawn **horizontally**.

### 2. YhzQHas0: swing high example
- Link: https://www.tradingview.com/x/YhzQHas0/ · File: `charts/YhzQHas0.png`
- Cited for: an example swing high with no new highs for the next 5 bars.
- Chart: **ARB/Bitcoin, 4h, BINANCE** [seen]. Range: about Oct 5 to Dec 15, 2023. Price: about 0.0000200 to 0.0000390.
- Drawings: one **horizontal red line** at the Nov 9, 2023 wick high (about 0.0000333), extended right to about Nov 27 [seen].
- What it shows: after the Nov 9 spike high, no later candle exceeds it. The swing high is marked at the **wick high**, horizontally.

### 3. UfZCXJUi: step 2, trending vs consolidating (market structure break)
- Link: https://www.tradingview.com/x/UfZCXJUi/ · File: `charts/UfZCXJUi.png`
- Chart: **ARB/Bitcoin, 4h, BINANCE**. Range: about Nov 13, 2023 to Jan 9, 2024. Price: about 0.0000200 to 0.0000395.
- Drawings: three **horizontal red lines** [seen]:
  1. The Dec 2 swing high (about 0.0000285), extended to Dec 12.
  2. The Dec 6–7 swing low (about 0.0000241), extended to Dec 19.
  3. The Dec 12 spike wick high (about 0.0000303), extended to about Dec 25.
- What it shows: from the downtrend, price makes a swing low (Dec 6–7). The Dec 12 spike breaks the previous swing high (line 1), which is the market structure break. Price then breaks the next swing high (line 3) on Dec 22 and trends up. Structure levels are drawn at **wick highs and lows**, horizontally.

### 4. BMegbRmB: step 3, more than 20 bars means too much noise
- Link: https://www.tradingview.com/x/BMegbRmB/ · File: `charts/BMegbRmB.png`
- Chart: **ARB/Bitcoin, 4h, BINANCE**. Range: about Nov 20, 2023 to Jan 5, 2024. Price: about 0.0000195 to 0.0000355.
- Drawings: a TradingView date-range measurement from the Dec 6 low to about Dec 20, labeled **"86 bars, 14d 8h, Vol 30.237M"** [seen]. No other drawings.
- What it shows: the consolidation lasts 86 bars on 4h, far above the 20-bar limit, so the author moves up a timeframe. The next chart uses **1D**. Going from 4h to 1D is **6x**, not exactly 5x [seen, inferred].

### 5. wPhFlGvd: under 20 bars, the first two trading blocks
- Link: https://www.tradingview.com/x/wPhFlGvd/ · File: `charts/wPhFlGvd.png`
- Chart: **ARB/Bitcoin, 1D, BINANCE**. Range: about Nov 10, 2023 to Jan 13, 2024. Price: about 0.0000200 to 0.0000350.
- Drawings [seen]:
  - A date-range measurement from Dec 6 to Dec 21: **"15 bars, 15d, Vol 33.32M"**.
  - Two **horizontal red lines (trading blocks)**:
    - **Upper:** about 0.0000301, starting at the Dec 12 candle's body top and extended to about Dec 26. [data] The Dec 12 daily close was 0.00003014, the **highest close** in the range.
    - **Lower:** about 0.0000267, starting at the Dec 17–18 body top (the Dec 17 close / Dec 18 open, 0.00002674 [data]) and extended to about Dec 24.
- What it shows: the same range is only 15 bars on the daily, under 20, so the trading blocks are marked there. Both blocks are **horizontal lines at candle closes (body edges), not wicks**. The upper block is the highest close in the range. The lower block is a later, lower close-high inside the range. The Dec 22 expansion candle closes above both blocks.

### 6. cjaZgEEA: step 4, expansion-bar entry above the 70 MA (4h/6h)
- Link: https://www.tradingview.com/x/cjaZgEEA/ · File: `charts/cjaZgEEA.png`
- Chart: **ARB/Bitcoin, 6h, BINANCE**. Range: about Nov 24, 2023 to Jan 6, 2024. Price: about 0.0000205 to 0.0000385.
- Drawings [seen]:
  - The two daily blocks carried down to 6h as red lines, each labeled **"Daily"** in green: about 0.00003013 (upper) and 0.00002673 (lower). My pixel calibration matches the daily closes 0.00003014 and 0.00002674 [data].
  - A **blue arrow** pointing at the Dec 22 06:00 UTC 6h candle. That candle opened at 0.00002625 and closed at 0.00003046, with a body 5.3x the previous candle's range [data]. It closes above both Daily blocks and above the MA.
  - A measurement **"58 bars, 14d 12h"** covering the same Dec 6–21 range on 6h.
  - A purple MA.
  - Blue ▲ and grey ▼ markers.
- **MA identification [data]:** I traced the purple line's pixels and compared them to Binance ARBBTC 6h closes. A **70-period SMA of the 6h closes** matches with about 3 px RMS error. EMA70 is off by 64 px, and SMA65 or SMA75 by about 19 px. **The MA is a 70-period simple moving average.**
- **Markers [data, partial]:** 26 of 28 blue ▲ sit under bullish candles that close above the previous candle's high. Not every such candle is marked, though, so the indicator's exact rule is **[uncertain]**. Grey ▼ markers mirror this on bearish candles.
- What it shows: entry on a lower timeframe than the 1D blocks, using an expansion candle that closes above the HTF trading block while above the 70 SMA. The price crossed above the MA only about 1 candle before the breakout.

### 7. ECInquT9: step 5, follow the trade and find new blocks (17 bars)
- Link: https://www.tradingview.com/x/ECInquT9/ · File: `charts/ECInquT9.png`
- Chart: **ARB/Bitcoin, 6h, BINANCE**. Range: about Dec 3, 2023 to Jan 12, 2024. Price: about 0.0000230 to 0.0000410.
- Drawings [seen]:
  - The **"Daily"** red line at about 0.0000301.
  - A new red line labeled **"6hr"** at about 0.0000322. [data] The Dec 22 18:00 UTC 6h close was 0.00003227, the highest close of the new consolidation.
  - A measurement **"17 bars, 4d 6h, Vol 10.815M"** from about Dec 23 to Dec 27.
  - A **blue arrow** pointing at the Dec 27 6h candle, which closes just above the 6hr line. The next candle then expands upward.
  - A purple MA, which looks like the same 70 SMA, rising well below price.
- What it shows: after the breakout, price consolidates between the Daily block (support) and a new 6h block. The range is 17 bars, under 20, so the 6h timeframe stays. The new block is again the **highest close** in the range, drawn horizontally.

### 8. 8YKgoAU2: entry reduced to 1h by the rule of 5
- Link: https://www.tradingview.com/x/8YKgoAU2/ · File: `charts/8YKgoAU2.png`
- Chart: **ARB/Bitcoin, 1h, BINANCE**. Range: about Dec 20 to Dec 31, 2023. Price: about 0.0000270 to 0.0000390.
- Drawings [seen]: the **"6hr"** line (about 0.0000322) and the **"Daily"** line (about 0.0000301) as red horizontals, a purple MA, and blue ▲ / grey ▼ markers.
- **MA identification [data]:** compared with Binance ARBBTC 1h closes, the purple line is a **70-period SMA of the 1h closes** (about 2.4 px RMS). EMA70 is off by 64 px. A 6h SMA70 projected onto the chart is off by 514 px. **The MA on this chart is computed on the chart's own timeframe, not projected from H6.**
- What it shows: inside the 6h range, the 1h chart gives the entry. On Dec 27 a run of bullish 1h candles crosses above the 1h 70 SMA, closes above the 6hr block, and then expands strongly upward. The ladder here is 6h to 1h, which is **6x**.

### 9. vAZXVPFn: exit strategy
- Link: https://www.tradingview.com/x/vAZXVPFn/ · File: `charts/vAZXVPFn.png`
- Chart: **Ethereum/TetherUS (ETHUSDT), 30m, BINANCE** [seen]. Range: about Feb 8 to Feb 13, 2024. Price: about 2,410 to 2,625 USDT. No MA is visible.
- Drawings [seen]:
  - One horizontal red line labeled **"6hr"** at about 2,503–2,504. [data] This matches the ETHUSDT 6h close of 2,503.20 on Feb 9 06:00 UTC. The range's highest 6h close is 2,504.23.
  - A callout **"Entry Signal"** pointing at a 30m candle on Feb 10 (evening, chart time) that closes just above the line. [data] The Feb 10 19:30 UTC-5 candle closed at 2,504.08. It is a small candle, not an expansion candle.
  - A callout **"Exit signal: Two consecutive lows / Both close below the entry level"** pointing at candles early on Feb 12. [data] Candidates: the 03:30 and 04:00 UTC-5 candles closed at 2,490.0 and 2,486.0 with successively lower lows. **[uncertain]** I can't tell exactly which two candles the callout means.
  - A callout **"New entry."** pointing at the Feb 12 morning expansion candle. [data] The 09:30 UTC-5 candle went from 2,495 to 2,528, closing well above the line.
- What it shows: the 2-bar exit rule (two closes back inside or below the block with lower lows) and a re-entry when price reclaims the block. The ladder used is a **6h block with 30m entries (12x)**. The entry candle was not an expansion candle, so expansion isn't required for entry.

---

## Doc 2: The mode method (ETH/BTC, grey background, R.E.Signal V3.3 indicator)

Common to Doc 2:
- Symbol: **Ethereum/Bitcoin (ETHBTC), BINANCE**.
- Legend: shows an indicator **"R.E.Signal V3.3"** (values 0.000000), which draws the dark ▲/▼ markers. [uncertain] I can't tell what it signals.
- Price scale: **logarithmic** [data]. Axis labels are unevenly spaced, and calibrating with the 0.079550 and 0.059323 tags reproduces the 0.073025 last-price tag on a log scale but not on a linear one.
- **Modes are thick cyan horizontal lines**, not sloped lines.

### 10. 1z1q6U7f: step 1, mark the max and min of the trend
- Link: https://www.tradingview.com/x/1z1q6U7f/ · File: `charts/1z1q6U7f.png`
- Chart: **ETHBTC 1D**. Range: about Aug 20 to Nov 4, 2021. Price: about 0.0564 to 0.084.
- Drawings [seen]: two thin horizontal lines with price tags:
  - **0.079550** at the Sep 3, 2021 high [data: Sep 3 high 0.07955].
  - **0.059323** at the Oct 19, 2021 low [data: Oct 19 low 0.059323].
- What it shows: the trend range is bounded by the **wick** high and low. Between them are lower highs and lower lows (Sep 3 to Oct 19), then a recovery.

### 11. FfAo2y17: step 2, drawing the modes (without labels)
- Link: https://www.tradingview.com/x/FfAo2y17/ · File: `charts/FfAo2y17.png`
- Chart: **ETHBTC 1D**, same window as #10. R.E.Signal V3.3 is shown.
- Drawings [seen]:
  - **Mode 1:** a cyan horizontal at about **0.0739**, spanning about Sep 9 to 16.
  - **Mode 2:** a cyan horizontal at about **0.0691**, spanning about Sep 20 to Oct 4.
  - A small red ↑ arrow under the end of mode 1 and a red ↓ arrow pointing down at mode 2.
- Anchors [data, inferred]:
  - Mode 1 at about 0.07393 matches the **Sep 16 low (0.07402)**, a higher low.
  - Mode 2 at about 0.06912 matches the **Sep 25 high (0.06918)**, a lower high.
  - Each mode is a horizontal line from **one candle's wick extreme**, extended across the consolidation candles. It cuts through many candle bodies.

### 12. lGtu8B7T: step 2, the modes with labels
- Link: https://www.tradingview.com/x/lGtu8B7T/ · File: `charts/lGtu8B7T.png`
- The same drawings as #11, plus red text [seen]:
  - "**Aca tenemos un modo de 8 velas / Se uso el minimo mas alto para encontrarlo**" (an 8-candle mode found using the highest low). This is mode 1, about Sep 9–16.
  - "**Aca tenemos un modo de 14 velas / Se uso el maximo mas bajo para encontrarlo**" (a 14-candle mode found using the lowest high). This is mode 2, about Sep 20 to Oct 3–4.
- What it shows: mode length is the number of candles the horizontal line spans (8 and 14). Inside a downtrend, both a "highest low" mode and a "lowest high" mode are used.

### 13. CieRq8zo: confirmations and expiry (with ATR pane)
- Link: https://www.tradingview.com/x/CieRq8zo/ · File: `charts/CieRq8zo.png`
- Chart: **ETHBTC 1D**, about Aug 20 to Nov 4, 2021, with an **ATR** pane. The legend reads "ATR 0.002534" and the length isn't printed.
- **ATR identification [data]:** recomputing on ETHBTC 1D, including the partial Nov 4 candle shown in the legend, a **14-period ATR with RMA/Wilder smoothing** (TradingView's default) gives exactly 0.002534. The pane's local minimum (about 0.00204 near Aug 29) and maximum (about 0.00305 near Sep 10) also match RMA14 (0.00203 and 0.00304). An SMA14 ATR gives 0.002378 and an EMA14 ATR gives 0.002403, both wrong. **So the ATR is length 14 with RMA smoothing.**
- Drawings [seen]:
  - Callout "**Esta vela confirma el modo / Y se cuenta como #1 en la caida**" (this candle confirms the mode and counts as #1 in the drop), pointing at the **Sep 17** candle for mode 1.
  - A date-range measurement **"8 bars, 8d"** ending at a dashed vertical line at **24 Sep '21**, with the callout "**Aca se acaba el modo de 8**" (the 8-mode ends here).
  - A second identical callout at the confirming candle of mode 2 (**Oct 6**), with **"14 bars, 14d"** ending at a dashed line at **19 Oct '21**, and the callout "**Aca se acaba el modo de 14**" at the 0.059323 trend low.
  - A stray red "Text" placeholder.
- Checked against data [data], with the mode levels from #11:
  - **Mode 1 confirmation, Sep 17:** opened at 0.07474 (above the mode) and closed at 0.07186, below it. The body is 83% of the range and 1.36x the previous candle's range, so it's an expansion candle. It closes **0.72 ATR below the mode** (ATR from the previous candle), which meets the 0.7 ATR rule. With Sep 17 as #1, #8 is **Sep 24**, the dashed line.
  - **Mode 2 confirmation, Oct 6:** high 0.06881, which **doesn't touch the 0.0691 mode**. It's a lower high and lower low than Oct 5, with a body 84% of its range and 3.0x the previous range. It closes **1.82 ATR below the mode**, so it satisfies all three confirmation types. With Oct 6 as #1, #14 is **Oct 19**, which is **exactly the trend low (0.059323)**.
  - Important: **Oct 4 and Oct 5 had already closed below mode 2, but only by 0.13 and 0.32 ATR**. Oct 4 was even an expansion candle (body 1.41x the previous range). The author did **not** treat them as confirmation. This supports the ≥0.7 ATR threshold.
- What it shows: the expiry count starts with the confirming candle as #1 and ends N candles later. The 8-mode expiry (Sep 24) came before a longer consolidation (the 14-mode). The 14-mode expiry landed on the trend floor.

### 14. 07QsRZHl: confirmations (an earlier version of #13, no ATR pane)
- Link: https://www.tradingview.com/x/07QsRZHl/ · File: `charts/07QsRZHl.png`
- The same drawings as #13 without the ATR pane, published 12 minutes earlier. A **small blue circle** sits at the top of the Oct 6 confirming candle. **[uncertain]** It may just be a drawing-tool anchor handle. A zoom shows clearly that the Oct 6 candle's **wick high stays below the mode line**, which illustrates the "candle doesn't touch the mode" confirmation.

### 15. kQmYeI1D: invalidation and bias flip
- Link: https://www.tradingview.com/x/kQmYeI1D/ · File: `charts/kQmYeI1D.png`
- Chart: **ETHBTC 1D**, about Sep 27 to Nov 8, 2021, with the ATR pane (0.002534).
- Drawings [seen]:
  - Mode 2 with its "14 bars, 14d" measurement and confirmation callout.
  - A new **mode 3**: a cyan horizontal at about **0.06245**, spanning about Oct 10 to 17. [data] It matches the Oct 10 low of 0.06245.
  - Callout: "**El maximo de la vela esta por debajo del Modo / Esta vela confirma que vamos para abajo: Maximo por debajo del modo / Y nuevos minimos**" (the candle's high is below the mode; it confirms the move down: high below the mode and new lows).
  - Callout: "**Esta vela invalida el Modo / Vela expansiva (envolvente) hacia arriba / También cierra por encima del Modo**" (this candle invalidates the mode: a bullish engulfing expansion candle that also closes above the mode).
- Checked against data [data]:
  - **Oct 18:** a large bearish candle with a body 85% of its range. It closed **0.73 ATR below** the mode, but its high (0.06271) touched the mode.
  - **Oct 19:** high 0.06142, below the mode, and a new low (0.05932). Its **body is only 4% of its range (a doji)**. The "high below the mode + new lows" callout fits Oct 19 best. **[uncertain]** I can't be sure from the leader lines alone.
  - **Oct 20:** a bullish engulfing candle that opened at 0.06031 and closed at 0.06306, with a body 1.31x the previous range and 74% of its own. It closed above the mode by **only 0.22 ATR**, yet it invalidated the bearish setup, and price rallied afterwards.
- What it shows: an invalidation only needs an **engulfing expansion candle that closes back beyond the mode**. In this example it did **not** need the 0.7 ATR margin. The confirmation the author accepted here was a small candle, even though the notes say the clear-gap candle should be large. That may be why it failed.

### 16. ieuv9uNb: multiple confirmation examples (blue arrows)
- Link: https://www.tradingview.com/x/ieuv9uNb/ · File: `charts/ieuv9uNb.png`
- Chart: **ETHBTC 1D**, about Feb 1 to Apr 30, 2021. Price: about 0.0255 to 0.049 (log scale).
- Drawings [seen]:
  - About six cyan horizontal **modes** in early to mid Feb, late Feb to early Mar, late Mar, Apr 5–12, and Apr 16–19.
  - **Blue arrows** at the confirmation candles:
    - **↓** about Feb 20, with the callout "**Vela con minimos mas bajos / Y el maximo abre por debajo del modo**" (a candle with lower lows whose high opens below the mode).
    - **↑** about Mar 4, about Mar 30, about Apr 13, and about Apr 19.
  - Date-range projections ending at dashed verticals:
    - **9 bars, 9d** ending **28 Feb '21**.
    - **6 bars, 6d** ending **11 Mar '21**.
    - **5 bars, 5d** and **6 bars, 6d** both ending around **02 Apr '21**.
    - **12 bars, 12d** and **6 bars, 6d** both ending **25 Apr '21**.
  - **Purple arrows** showing the move that followed each confirmation: down into Feb 28, up into Mar 11, up into Apr 2, and up into late April.
- What it shows: each confirmation projects the mode's length forward. The projected end dates line up with swing turns or the end of a leg (Feb 28 low, Mar 11 high, Apr 2 top of the impulse). When two projections end on the same date, that's treated as a stronger timing point (25 Apr). All the modes are horizontal.

### 17. J2C6eUvo: all modes of the previous example, zoomed out
- Link: https://www.tradingview.com/x/J2C6eUvo/ · File: `charts/J2C6eUvo.png`
- Chart: **ETHBTC 1D**, about Dec 2020 to Jun 2021. Price: about 0.0193 to 0.082.
- Drawings: the same modes, arrows, callout, and projections as #16, now in context. The trend continues far beyond them, up to about 0.082 in May 2021 [seen].
- What it shows: the daily modes are tiny compared with the overall trend, which is the trigger for Rule 4 (re-evaluate on a higher timeframe).

### 18. dn3R54x5: daily, unclear, modes too big
- Link: https://www.tradingview.com/x/dn3R54x5/ · File: `charts/dn3R54x5.png`
- Chart: **ETHBTC 1D**, about Dec 2020 to Jun 2021. No modes are drawn.
- Drawings [seen]:
  - A horizontal at **0.046094** labeled "**Maximo anterior**" (previous high, early Feb 2021). [data] The Binance high on Feb 5 was 0.04618, so the line is about 0.2% lower.
  - A horizontal at **0.022623** from the late-Dec 2020 low, labeled "**Empezamos a marcar el modo desde el punto minimo / Ya sabemos que estamos en una tendencia alcista / Rompimos el maximo anterior y con eso nos confirma**" (we start marking the mode from the low point; we know we're in an uptrend; breaking the previous high confirms it). [data] The Binance low on Dec 27 was 0.022754.
- What it shows: on the HTF, the uptrend is confirmed by breaking the previous high. Modes are anchored from the trend's lowest point. On the daily, modes from that low would be far longer than 20 bars, so the author moves up to the weekly.

### 19. Mplsx7FC: switched to weekly
- Link: https://www.tradingview.com/x/Mplsx7FC/ · File: `charts/Mplsx7FC.png`
- Chart: **ETHBTC 1W**, about Nov 2020 to Aug 2021. Price: about 0.0204 to 0.083 (log scale).
- Drawings [seen]: the same "Maximo anterior" (0.046094) and low (0.022623) lines and labels, plus two cyan **modes**:
  - **Upper:** about **0.0386**, spanning from late Jan to the Apr 12 week. [data] It matches the **Feb 1 week low (0.03848)**, a higher low.
  - **Lower:** about **0.0314**, spanning the Mar 1 to Mar 22 weeks. [data] It sits near the Feb 22 close / Mar 1 open (0.03144) and the Mar 8 close (0.03133).
- Projections:
  - **"6 bars, 42d"** starting at the Mar 29 week.
  - **"5 bars, 35d"** starting at the Apr 12 week.
  - A purple arrow up.
- Checked against data [data]:
  - **Mar 29 week:** a bullish expansion candle with a body 89% of its range and 2.57x the previous range. It closed 0.97 ATR above the lower mode, but its body crosses the mode.
  - **Apr 12 week:** body 2.09x the previous range, closing above the upper mode by only about 0.3 ATR. Its body also crosses the mode.
  - The two projections end one week apart (May 10 and May 17). That's the "they don't coincide, but one week apart is fine" remark in the notes.

### 20. FyFW7pdN: weekly, two bullish modes plus a bearish mode
- Link: https://www.tradingview.com/x/FyFW7pdN/ · File: `charts/FyFW7pdN.png`
- The same as #19, plus [seen]:
  - A dashed vertical at **10 May '21**, where the 6-bar projection ends. [data] The May 10 week made the top, with a high of 0.0824.
  - A new **bearish mode**: a cyan horizontal at about **0.0735**, spanning the May 17 to Jun 7 weeks. [data] It is consistent with the **May 24 week high (0.07374)**, a lower high, though it's hard to read from the image.
  - **"5 bars, 35d"** from the Jun 7 week to a dashed vertical at **12 Jul '21**, with a purple arrow down.
- Checked against data [data]: the **Jun 7 week** opened at 0.07575 and closed at 0.06431, with a body 77% of its range and 1.15x the previous range. It closed **1.12 ATR below** the mode, and its body crosses the mode. Counting starts after it: the Jun 14 week is #1 and the **Jul 12 week is #5**, matching the dashed line. Price falls from the mode into July.

### 21. nE8Kv6wH: expansion candles whose bodies touch the mode
- Link: https://www.tradingview.com/x/nE8Kv6wH/ · File: `charts/nE8Kv6wH.png`
- Chart: **ETHBTC 1W**, same view as #20.
- Drawings [seen]: three callouts reading "**Vela Expansiva / Confirma pero sigue siendo parte del modo**" (an expansion candle: it confirms but is still part of the mode). They point at:
  - the **Mar 29 week** (lower bullish mode)
  - the **Apr 12 week** (upper bullish mode, whose cyan line extends up to this candle)
  - the **Jun 7 week** (bearish mode)

  The "5 bars, 35d" projection to **12 Jul '21** is kept. The 6- and 5-bar bullish projections are removed in this version.
- What it shows: when the confirming expansion candle's **body crosses or touches the mode**, the candle counts as both part of the mode and the confirmation, and the expiry count starts on the **next** candle. Compare #13–14: there, the confirming candle's wick didn't touch the mode (Oct 6), or the candle opened at or above the mode and closed well below it (Sep 17), and the count starts **at** the confirming candle (#1). **[inferred]** The Sep 17 case is ambiguous: its body did start above the mode.

---

## What the charts clarify (answers to the skill's open questions)

1. **Is a mode a sloped trendline or a horizontal level?** It's a **horizontal level**. Every mode in Doc 2 is a cyan horizontal line, and all trading blocks and swing levels in Doc 1 are horizontal red or grey lines.
   - **Anchor:** [data] the mode levels match a single candle's **wick extreme**: a highest low (Sep 16, 2021 low; Oct 10 low; Feb 1, 2021 weekly low) or a lowest high (Sep 25 high; May 24, 2021 weekly high). The line is then extended across the consolidation candles and cuts through their bodies.
   - **Length:** the number of candles it spans. 8, 14, 9, 6, 5, and 12 bars all appear.
   - **"Beyond the mode":** simply close minus the fixed mode price.
2. **Is the 70 MA simple or exponential?** It's **Simple (SMA), length 70, on closes** [data: about 2–3 px fit on both the 6h and 1h charts, versus about 64 px for EMA70]. It's plotted **on the chart's own timeframe**: the 6h chart shows SMA70(6h) and the 1h chart shows SMA70(1h), not a projected H6 line. The rule text says "H6 70 MA," so a bot should compute SMA70 on 6h candles for the filter. Whether lower-timeframe charts should also require price above their own SMA70 isn't stated (see open questions).
3. **ATR length:** **14, with Wilder/RMA smoothing** (TradingView's default ATR) [data: matches 0.002534 exactly and the pane's min and max]. On the documented examples, the "≥0.7 x ATR(previous candle)" close rule fits:
   - Sep 17, 2021 closed 0.72 ATR beyond the mode and was accepted.
   - Oct 4–5 closed only 0.13–0.32 ATR beyond and were **not** treated as confirmations.
   - Oct 6 closed 1.82 ATR beyond and was accepted.
   - Jun 7, 2021 (weekly) closed 1.12 ATR beyond and was accepted.
   - Exceptions: the Apr 12, 2021 weekly candle was called a confirmation at only about 0.3 ATR (its body crossed the mode, and it was an expansion candle 2.09x the previous range). The Oct 20 invalidation needed only 0.22 ATR.
4. **Mode expiry counting:**
   - If the confirming candle **doesn't overlap the mode with its body**, it is **#1** of the count. Examples: Sep 17 (#1) to Sep 24 (#8), and Oct 6 (#1) to Oct 19 (#14).
   - If the confirming expansion candle's **body touches or crosses the mode**, it's still part of the mode and the count starts **on the next candle**. Example: Jun 7 week, then Jun 14 is #1 and Jul 12 is #5.
   - Expiry dates landed on the trend low (Oct 19, 2021), the top (May 10, 2021 weekly), and swing turns (Feb 28 and Mar 11, 2021). Two projections ending together (25 Apr '21), or within a week of each other on the weekly, are highlighted.
5. **Timeframe ladder actually used:** 4h to **1D** for the block (6x), 1D blocks with **6h** entries (4x), 6h blocks with **1h** entries (6x), a 6h block with **30m** entries (12x), and 1D to **1W** for modes. So the "5x" rule is applied loosely, using standard exchange intervals (30m, 1h, 4h, 6h, 1D, 1W).
6. **Trading block definition:** confirmed as the **highest candle close** in the HTF range. For example, the daily block 0.00003014 is the Dec 12 daily close, the 6h block 0.00003227 is the Dec 22 18:00 UTC 6h close, and the ETH 6h block is about 2,503–2,504. Blocks are drawn as horizontal lines at closes, not wicks.
7. **Swing and structure levels:** drawn at **wick** highs and lows. A structure break is a close or breakout above the previous swing-high wick (UfZCXJUi).
8. **Entry trigger:** the first lower-timeframe candle that closes above the HTF block (ETH: 2,504.08 versus a 2,503.20 block). **An expansion candle is not required** (the ETH entry candle was small), but the ARB examples all broke out on large expansion candles.
9. **Exit:** demonstrated as **two consecutive candles with lower lows closing below the entry level**, followed by a **re-entry** when an expansion candle reclaims the block.
10. **Invalidation:** a bullish engulfing expansion candle closing back above a bearish mode, even by a small margin (0.22 ATR), flips the bias.
11. **Stops:** **no stop-loss level is drawn on any chart.** The only exit evidence is the 2-bar close-back-inside rule (vAZXVPFn).

## Questions still open

1. **Initial stop placement:** not shown on any chart. Options include below the block, below the expansion candle's low, or below the last swing low.
2. **Position sizing and risk per trade:** not shown.
3. Does the **SMA70 filter use H6 always**, or the entry chart's own SMA70? The charts show it on each chart's own timeframe (6h and 1h), and the 30m ETH chart shows none.
4. **Exact timeframe ladder for a bot:** the charts use 4x–12x jumps on standard intervals. Does the bot pick the nearest standard interval to 5x, or use a fixed table (e.g., 30m → 2h/1h → 6h → 1D → 1W)?
5. **Is the ≥0.7 ATR requirement strict?** One weekly confirmation (Apr 12, 2021) was accepted at about 0.3 ATR when the body crossed the mode. And should invalidation need any ATR margin?
6. **Which wick anchors a mode** when several candidates exist: the first highest low, or the one that maximizes touches? And what counts as the mode's start and end candle for the length count?
7. **The "clear-gap" confirmation in kQmYeI1D** was a doji (4% body), even though the notes require a large candle. Is a small candle acceptable if its high stays below the mode with new lows?
8. **R.E.Signal V3.3** (Doc 2) and the **blue ▲ / grey ▼ markers** (Doc 1): what do they compute? On ARB 6h, blue ▲ mostly sit on bullish candles that close above the prior high (26 of 28), but not every such candle is marked.
9. **How Part A (modes and time expiry) and Part B (trading blocks and entries) combine:** the Doc 1 charts use blocks and the MA, the Doc 2 charts use modes and ATR. No chart shows both together.
10. **Exit callout exact candles** on vAZXVPFn: data points to the Feb 12 03:30 and 04:00 UTC-5 30m candles, but the chart's timezone isn't shown.
