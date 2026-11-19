# Exit variants

Same signals and the same 0.7 ATR readings. Only the exit setting changes.
baseline: fixed stop or two closes. trail: stop ratchets to the confirmed
5-bar swing or the new block on the timeframe in control. opposite: an
opposite confirmed signal closes the trade and may reverse. two_close:
the two-close rule only. all: stop, trail, opposite, and two closes together.
The portfolio is the equal-weight of each pair's daily return, both exchanges together.
A variant that beats that portfolio's buy-and-hold Sharpe in 2017-2022 and does not
beat it in 2023-now is marked in-sample only.

| Variant | Sample | Pairs | Return | Sharpe | Sortino | CAGR | BH return | BH Sharpe | BH Sortino | Beats BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 2017-2022 in sample | 20 | 480.6% | 0.99 | 1.42 | 38.8% | 2117.4% | 1.10 | 1.57 | no |
| baseline | 2023-now out of sample | 20 | 62.9% | 0.51 | 0.74 | 13.4% | 97.0% | 0.59 | 0.86 | no |
| trail | 2017-2022 in sample | 20 | 93.6% | 0.97 | 1.73 | 13.1% | 2117.4% | 1.10 | 1.57 | no |
| trail | 2023-now out of sample | 20 | -16.0% | -0.30 | -0.50 | -4.4% | 97.0% | 0.59 | 0.86 | no |
| opposite | 2017-2022 in sample | 20 | 411.2% | 1.82 | 2.98 | 35.5% | 2117.4% | 1.10 | 1.57 | yes |
| opposite | 2023-now out of sample | 20 | 60.3% | 0.92 | 1.43 | 12.9% | 97.0% | 0.59 | 0.86 | yes |
| two_close | 2017-2022 in sample | 20 | 402.5% | 0.93 | 1.31 | 35.1% | 2117.4% | 1.10 | 1.57 | no |
| two_close | 2023-now out of sample | 20 | 63.7% | 0.52 | 0.74 | 13.5% | 97.0% | 0.59 | 0.86 | no |
| all | 2017-2022 in sample | 20 | 84.1% | 0.91 | 1.60 | 12.0% | 2117.4% | 1.10 | 1.57 | no |
| all | 2023-now out of sample | 20 | -18.7% | -0.37 | -0.60 | -5.2% | 97.0% | 0.59 | 0.86 | no |

In-sample only: trail (Sortino only), all (Sortino only).

Out of sample, these variants beat equal-weight buy-and-hold Sharpe: opposite.

## binance BTCUSDT

### baseline

Blocked signals 4237. Exits: open 2, stop 34, two_lower_closes 8.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 27 | 0.0% | -0.94 | -22.5% | 363.1% | 0.76 | 1.09 | 31.8% | 98.5% | 59.89 | 76.6% | 340.5% | 287.6% | 0.72 |
| 2023-now out of sample | 15 | 0.0% | -1.07 | -11.6% | 1602.2% | 0.97 | 1.50 | 41.0% | 100.0% | 78.91 | 53.3% | 280.1% | 281.3% | 0.97 |

### trail

Blocked signals 3401. Exits: open 1, stop 416, trail 463.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 515 | 32.0% | 0.25 | 187.6% | 0.7% | 0.94 | 1.74 | 21.8% | 69.2% | 2.67 | 34.4% | 188.3% | 287.6% | 0.72 |
| 2023-now out of sample | 364 | 28.8% | -0.11 | -106.3% | 5.1% | -0.46 | -0.73 | -10.7% | 69.6% | 2.76 | 47.8% | -35.6% | 281.3% | 0.97 |

### opposite

Blocked signals 3917. Exits: open 1, opposite_signal 160, stop 203.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 200 | 25.5% | 0.97 | 440.3% | 3.9% | 1.24 | 2.05 | 37.1% | 92.7% | 9.03 | 20.2% | 444.3% | 287.6% | 0.72 |
| 2023-now out of sample | 163 | 19.0% | 0.39 | 326.1% | 24.3% | 0.64 | 1.00 | 13.5% | 92.6% | 8.07 | 20.4% | 63.5% | 281.3% | 0.97 |

### two_close

Blocked signals 4239. Exits: open 2, two_lower_closes 40.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 25 | 0.0% | -1.32 | -28.5% | 345.4% | 0.74 | 1.07 | 30.4% | 98.7% | 65.09 | 76.8% | 316.9% | 287.6% | 0.72 |
| 2023-now out of sample | 15 | 0.0% | -1.30 | -12.7% | 1525.6% | 0.97 | 1.50 | 41.2% | 100.0% | 80.04 | 53.3% | 281.6% | 281.3% | 0.97 |

### all

Blocked signals 3379. Exits: open 1, opposite_signal 44, stop 384, trail 440, two_lower_closes 33.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 532 | 30.6% | 0.22 | 157.6% | 0.6% | 0.85 | 1.56 | 19.3% | 67.9% | 2.52 | 37.4% | 158.3% | 287.6% | 0.72 |
| 2023-now out of sample | 369 | 28.7% | -0.10 | -90.0% | 4.7% | -0.41 | -0.65 | -10.0% | 69.3% | 2.66 | 46.5% | -33.5% | 281.3% | 0.97 |

## binance ETHUSDT

### baseline

Blocked signals 4106. Exits: open 2, stop 29, two_lower_closes 4.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 29 | 0.0% | -0.99 | -25.2% | 238.8% | 0.66 | 0.96 | 23.7% | 98.5% | 68.13 | 75.1% | 213.6% | 297.3% | 0.76 |
| 2023-now out of sample | 4 | 0.0% | -1.10 | -3.2% | 358.8% | 0.43 | 0.64 | 8.6% | 100.0% | 338.38 | 64.5% | 37.6% | 48.6% | 0.47 |

### trail

Blocked signals 3315. Exits: open 1, stop 378, trail 447.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 465 | 34.4% | 0.15 | 81.1% | 0.6% | 0.66 | 1.11 | 11.8% | 67.0% | 2.87 | 23.8% | 82.1% | 297.3% | 0.76 |
| 2023-now out of sample | 360 | 31.7% | 0.01 | -8.4% | 5.2% | 0.07 | 0.13 | -0.5% | 70.3% | 2.82 | 41.7% | -1.8% | 48.6% | 0.47 |

### opposite

Blocked signals 3811. Exits: open 1, opposite_signal 160, stop 169.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 171 | 26.9% | 1.17 | 495.5% | 0.9% | 1.47 | 2.32 | 39.4% | 90.9% | 10.35 | 23.2% | 496.5% | 297.3% | 0.76 |
| 2023-now out of sample | 158 | 21.5% | 0.38 | 367.2% | 25.6% | 0.72 | 1.18 | 13.9% | 94.9% | 8.55 | 27.4% | 65.6% | 48.6% | 0.47 |

### two_close

Blocked signals 4109. Exits: open 2, two_lower_closes 30.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 26 | 0.0% | -1.58 | -34.3% | 108.0% | 0.46 | 0.64 | 10.8% | 98.7% | 60.23 | 68.5% | 73.7% | 297.3% | 0.76 |
| 2023-now out of sample | 4 | 0.0% | -1.55 | -4.0% | 155.9% | 0.36 | 0.54 | 6.0% | 100.0% | 339.50 | 59.3% | 25.5% | 48.6% | 0.47 |

### all

Blocked signals 3278. Exits: open 1, opposite_signal 45, stop 359, trail 416, two_lower_closes 42.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 480 | 33.8% | 0.13 | 66.9% | 0.6% | 0.59 | 0.99 | 10.1% | 66.2% | 2.73 | 23.5% | 67.7% | 297.3% | 0.76 |
| 2023-now out of sample | 382 | 29.6% | -0.02 | -22.2% | 4.4% | -0.03 | -0.05 | -2.9% | 68.7% | 2.55 | 45.6% | -10.7% | 48.6% | 0.47 |

## binance SOLUSDT

### baseline

Blocked signals 2919. Exits: open 2, stop 34, two_lower_closes 7.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 18 | 0.0% | -1.01 | -16.8% | 94.9% | 0.73 | 1.08 | 27.4% | 97.4% | 15.52 | 91.3% | 78.2% | 200.1% | 1.05 |
| 2023-now out of sample | 23 | 0.0% | -1.00 | -17.2% | 550.5% | 0.80 | 1.24 | 37.5% | 100.0% | 52.32 | 73.9% | 245.1% | 638.6% | 1.02 |

### trail

Blocked signals 2358. Exits: open 1, stop 283, trail 320.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 226 | 35.0% | 0.20 | 49.4% | 0.0% | 0.95 | 1.65 | 18.3% | 68.5% | 2.68 | 28.0% | 49.4% | 200.1% | 1.05 |
| 2023-now out of sample | 377 | 30.2% | 0.03 | 3.1% | 2.4% | 0.14 | 0.25 | 0.9% | 68.0% | 2.59 | 36.0% | 3.6% | 638.6% | 1.02 |

### opposite

Blocked signals 2735. Exits: open 1, opposite_signal 110, stop 116.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 78 | 20.5% | 3.10 | 344.4% | 23.4% | 2.06 | 3.79 | 90.9% | 92.3% | 10.10 | 18.8% | 367.9% | 200.1% | 1.05 |
| 2023-now out of sample | 148 | 25.7% | 0.44 | 309.4% | 50.7% | 0.72 | 1.14 | 15.0% | 94.0% | 8.87 | 21.1% | 72.1% | 638.6% | 1.02 |

### two_close

Blocked signals 2925. Exits: open 2, two_lower_closes 35.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 18 | 0.0% | -1.53 | -24.4% | 91.5% | 0.70 | 1.04 | 24.0% | 97.4% | 16.88 | 91.8% | 67.0% | 200.1% | 1.05 |
| 2023-now out of sample | 17 | 0.0% | -1.53 | -17.5% | 545.6% | 0.81 | 1.26 | 39.1% | 100.0% | 71.80 | 74.3% | 260.3% | 638.6% | 1.02 |

### all

Blocked signals 2344. Exits: open 1, opposite_signal 31, stop 250, trail 305, two_lower_closes 31.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 231 | 34.2% | 0.18 | 44.8% | 0.0% | 0.89 | 1.53 | 16.8% | 67.7% | 2.59 | 27.9% | 44.8% | 200.1% | 1.05 |
| 2023-now out of sample | 386 | 29.8% | 0.05 | 14.5% | 2.5% | 0.24 | 0.42 | 2.9% | 66.9% | 2.47 | 31.3% | 11.7% | 638.6% | 1.02 |

## binance ARBUSDT

### baseline

Blocked signals 1657. Exits: open 2, stop 43, two_lower_closes 4.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 0 | n/a | n/a | 0.0% | 0.0% | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2023-now out of sample | 47 | 0.0% | -1.04 | -38.9% | 12.7% | -0.31 | -0.46 | -8.0% | 97.2% | 17.14 | 38.7% | -26.2% | -90.4% | -0.17 |

### trail

Blocked signals 1372. Exits: open 1, stop 163, trail 170.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 0 | n/a | n/a | 0.0% | 0.0% | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2023-now out of sample | 333 | 33.9% | -0.06 | -22.5% | 0.1% | -0.30 | -0.48 | -6.7% | 66.6% | 2.71 | 26.6% | -22.4% | -90.4% | -0.17 |

### opposite

Blocked signals 1562. Exits: open 1, opposite_signal 61, stop 82.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 0 | n/a | n/a | 0.0% | 0.0% | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2023-now out of sample | 143 | 22.4% | 0.16 | 16.7% | 2.5% | 0.33 | 0.53 | 4.9% | 90.4% | 8.41 | 20.0% | 19.1% | -90.4% | -0.17 |

### two_close

Blocked signals 1668. Exits: open 2, two_lower_closes 36.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 0 | n/a | n/a | 0.0% | 0.0% | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2023-now out of sample | 36 | 0.0% | -1.35 | -38.8% | 13.2% | -0.25 | -0.37 | -7.8% | 97.4% | 26.48 | 45.6% | -25.6% | -90.4% | -0.17 |

### all

Blocked signals 1361. Exits: open 1, opposite_signal 16, stop 149, trail 162, two_lower_closes 17.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 0 | n/a | n/a | 0.0% | 0.0% | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2023-now out of sample | 344 | 33.1% | -0.06 | -22.4% | 0.1% | -0.30 | -0.48 | -6.7% | 65.8% | 2.57 | 27.4% | -22.4% | -90.4% | -0.17 |

## binance BNBUSDT

### baseline

Blocked signals 4180. Exits: open 2, stop 45, two_lower_closes 9.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 22 | 0.0% | -0.96 | -19.1% | 1076.9% | 0.99 | 1.63 | 60.9% | 98.7% | 46.05 | 68.6% | 1057.8% | 15546.1% | 1.39 |
| 2023-now out of sample | 32 | 0.0% | -1.09 | -23.9% | 2534.6% | 0.67 | 0.99 | 23.0% | 100.0% | 33.77 | 57.6% | 123.4% | 136.6% | 0.69 |

### trail

Blocked signals 3409. Exits: open 1, stop 393, trail 433.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 452 | 33.6% | 0.09 | 33.9% | 0.2% | 0.37 | 0.61 | 5.9% | 69.5% | 2.94 | 35.5% | 34.2% | 15546.1% | 1.39 |
| 2023-now out of sample | 374 | 27.5% | -0.13 | -59.7% | 3.7% | -0.50 | -0.86 | -13.0% | 68.6% | 2.64 | 51.9% | -41.8% | 136.6% | 0.69 |

### opposite

Blocked signals 3874. Exits: open 1, opposite_signal 179, stop 182.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 187 | 25.1% | 2.86 | 926.0% | 62.8% | 1.24 | 2.44 | 59.0% | 91.6% | 9.11 | 32.2% | 988.8% | 15546.1% | 1.39 |
| 2023-now out of sample | 174 | 17.8% | 0.38 | 544.8% | 34.7% | 0.49 | 0.78 | 10.5% | 93.6% | 7.64 | 47.1% | 47.6% | 136.6% | 0.69 |

### two_close

Blocked signals 4190. Exits: open 2, two_lower_closes 44.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 20 | 0.0% | -1.47 | -25.7% | 1073.1% | 0.99 | 1.62 | 60.6% | 98.7% | 51.69 | 68.9% | 1047.4% | 15546.1% | 1.39 |
| 2023-now out of sample | 24 | 0.0% | -1.49 | -22.5% | 2534.1% | 0.67 | 1.00 | 23.2% | 100.0% | 47.88 | 57.7% | 125.0% | 136.6% | 0.69 |

### all

Blocked signals 3369. Exits: open 1, opposite_signal 69, stop 346, trail 406, two_lower_closes 45.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 469 | 32.2% | 0.07 | 28.5% | 0.2% | 0.33 | 0.54 | 5.0% | 68.5% | 2.75 | 37.8% | 28.7% | 15546.1% | 1.39 |
| 2023-now out of sample | 397 | 27.2% | -0.14 | -60.3% | 3.4% | -0.54 | -0.92 | -14.0% | 67.5% | 2.41 | 52.3% | -44.3% | 136.6% | 0.69 |

## binance XRPUSDT

### baseline

Blocked signals 3718. Exits: open 2, stop 48, two_lower_closes 11.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 48 | 0.0% | -1.00 | -38.5% | 14.2% | -0.05 | -0.07 | -5.8% | 98.3% | 27.58 | 46.6% | -24.3% | -61.2% | 0.37 |
| 2023-now out of sample | 11 | 0.0% | -1.05 | -6.7% | 43.3% | 0.36 | 0.59 | 7.0% | 100.0% | 117.55 | 54.1% | 29.8% | 185.5% | 0.70 |

### trail

Blocked signals 3014. Exits: open 1, stop 391, trail 373.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 406 | 30.5% | 0.09 | 26.9% | 0.0% | 0.34 | 0.62 | 5.2% | 67.5% | 2.90 | 25.8% | 26.9% | -61.2% | 0.37 |
| 2023-now out of sample | 358 | 27.4% | -0.12 | -50.2% | 0.4% | -0.58 | -0.94 | -12.0% | 69.1% | 2.83 | 45.7% | -39.2% | 185.5% | 0.70 |

### opposite

Blocked signals 3417. Exits: open 1, opposite_signal 150, stop 211.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 169 | 21.3% | 0.17 | 21.5% | 3.5% | 0.31 | 0.49 | 4.9% | 91.7% | 8.90 | 28.6% | 25.1% | -61.2% | 0.37 |
| 2023-now out of sample | 192 | 14.6% | -0.13 | -41.3% | 18.7% | -0.16 | -0.26 | -5.9% | 92.4% | 6.92 | 45.5% | -21.1% | 185.5% | 0.70 |

### two_close

Blocked signals 3738. Exits: open 2, two_lower_closes 39.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 30 | 0.0% | -1.78 | -42.9% | 12.9% | -0.12 | -0.18 | -7.4% | 98.3% | 50.50 | 45.5% | -30.0% | -61.2% | 0.37 |
| 2023-now out of sample | 9 | 0.0% | -1.46 | -7.1% | 38.8% | 0.35 | 0.56 | 6.4% | 100.0% | 145.26 | 53.6% | 27.2% | 185.5% | 0.70 |

### all

Blocked signals 2980. Exits: open 1, opposite_signal 63, stop 354, trail 346, two_lower_closes 35.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 419 | 29.4% | 0.11 | 38.5% | 0.0% | 0.42 | 0.78 | 7.2% | 66.9% | 2.73 | 23.0% | 38.5% | -61.2% | 0.37 |
| 2023-now out of sample | 379 | 25.1% | -0.12 | -58.5% | 0.4% | -0.61 | -0.99 | -13.1% | 68.1% | 2.56 | 48.1% | -41.9% | 185.5% | 0.70 |

## binance ADAUSDT

### baseline

Blocked signals 4137. Exits: open 2, stop 21, two_lower_closes 3.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 24 | 0.0% | -1.02 | -22.0% | 188.8% | 0.64 | 1.01 | 23.2% | 98.5% | 62.16 | 89.6% | 166.8% | 1.3% | 0.55 |
| 2023-now out of sample | 0 | n/a | n/a | 0.0% | 109.8% | 0.23 | 0.38 | -8.6% | 100.0% | n/a | 83.3% | -29.6% | -38.4% | 0.26 |

### trail

Blocked signals 3358. Exits: open 1, stop 394, trail 410.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 427 | 35.4% | 0.12 | 50.1% | 0.0% | 0.54 | 0.90 | 9.0% | 69.5% | 2.84 | 25.4% | 50.1% | 1.3% | 0.55 |
| 2023-now out of sample | 377 | 30.8% | -0.10 | -54.3% | 1.9% | -0.50 | -0.80 | -10.5% | 69.8% | 2.72 | 43.4% | -34.9% | -38.4% | 0.26 |

### opposite

Blocked signals 3812. Exits: open 1, opposite_signal 170, stop 180.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 171 | 22.8% | 0.73 | 182.4% | 7.5% | 1.07 | 1.73 | 25.4% | 92.2% | 8.97 | 24.5% | 189.9% | 1.3% | 0.55 |
| 2023-now out of sample | 179 | 20.1% | 0.20 | 79.5% | 30.6% | 0.46 | 0.73 | 8.1% | 92.4% | 7.43 | 28.6% | 35.4% | -38.4% | 0.26 |

### two_close

Blocked signals 4138. Exits: open 2, two_lower_closes 23.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 23 | 0.0% | -1.73 | -33.9% | 168.1% | 0.61 | 0.95 | 19.8% | 98.5% | 65.97 | 89.7% | 134.2% | 1.3% | 0.55 |
| 2023-now out of sample | 0 | n/a | n/a | 0.0% | 97.6% | 0.23 | 0.38 | -8.8% | 100.0% | n/a | 83.7% | -30.1% | -38.4% | 0.26 |

### all

Blocked signals 3333. Exits: open 1, opposite_signal 65, stop 344, trail 384, two_lower_closes 36.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 440 | 34.1% | 0.11 | 46.3% | 0.0% | 0.52 | 0.86 | 8.4% | 69.0% | 2.70 | 26.8% | 46.3% | 1.3% | 0.55 |
| 2023-now out of sample | 389 | 29.3% | -0.10 | -52.3% | 1.9% | -0.56 | -0.84 | -10.3% | 68.4% | 2.49 | 43.2% | -34.4% | -38.4% | 0.26 |

## binance DOGEUSDT

### baseline

Blocked signals 3338. Exits: open 2, stop 24, two_lower_closes 3.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 27 | 0.0% | -1.06 | -25.1% | 1207.1% | 0.95 | 2.81 | 107.7% | 96.9% | 17.85 | 92.0% | 1182.0% | 1667.4% | 0.95 |
| 2023-now out of sample | 0 | n/a | n/a | 0.0% | 1033.4% | 0.35 | 0.53 | -4.3% | 100.0% | n/a | 87.2% | -15.7% | -16.3% | 0.36 |

### trail

Blocked signals 2709. Exits: open 1, stop 312, trail 345.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 286 | 33.2% | 0.20 | 60.7% | -0.4% | 0.70 | 1.32 | 14.8% | 64.9% | 2.99 | 23.8% | 62.0% | 1667.4% | 0.95 |
| 2023-now out of sample | 371 | 32.1% | 0.21 | 115.8% | -0.2% | 0.72 | 1.37 | 15.0% | 70.0% | 2.73 | 22.0% | 71.9% | -16.3% | 0.36 |

### opposite

Blocked signals 3104. Exits: open 1, opposite_signal 124, stop 138.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 121 | 24.8% | 0.64 | 87.5% | 9.4% | 0.74 | 1.31 | 21.4% | 90.4% | 9.37 | 21.6% | 96.9% | 1667.4% | 0.95 |
| 2023-now out of sample | 141 | 22.7% | 0.92 | 315.8% | 78.2% | 1.02 | 1.69 | 32.3% | 94.1% | 9.30 | 25.2% | 196.4% | -16.3% | 0.36 |

### two_close

Blocked signals 3354. Exits: open 1, two_lower_closes 12.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 12 | 0.0% | -26.92 | -231.3% | 1148.8% | 0.99 | 2.59 | 94.4% | 97.2% | 45.92 | 93.6% | 917.5% | 1667.4% | 0.95 |
| 2023-now out of sample | 0 | n/a | n/a | 0.0% | 982.6% | 0.38 | 0.59 | -5.2% | 100.0% | n/a | 89.5% | -18.9% | -16.3% | 0.36 |

### all

Blocked signals 2669. Exits: open 1, opposite_signal 56, stop 277, trail 326, two_lower_closes 38.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 306 | 31.0% | 0.11 | 25.3% | -0.3% | 0.39 | 0.65 | 6.9% | 64.3% | 2.71 | 25.9% | 26.4% | 1667.4% | 0.95 |
| 2023-now out of sample | 391 | 30.7% | 0.13 | 40.4% | -0.1% | 0.42 | 0.76 | 7.4% | 69.3% | 2.52 | 28.3% | 32.1% | -16.3% | 0.36 |

## binance AVAXUSDT

### baseline

Blocked signals 2912. Exits: open 2, stop 14, two_lower_closes 1.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 15 | 0.0% | -1.01 | -14.1% | 32.3% | 0.44 | 0.68 | 7.6% | 94.2% | 15.14 | 71.0% | 18.2% | 104.4% | 0.93 |
| 2023-now out of sample | 0 | n/a | n/a | 0.0% | 23.5% | 0.10 | 0.14 | -2.0% | 100.0% | n/a | 54.0% | -7.5% | -35.5% | 0.30 |

### trail

Blocked signals 2356. Exits: open 1, stop 260, trail 312.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 190 | 40.0% | 0.37 | 85.3% | 4.6% | 1.52 | 3.02 | 32.6% | 68.9% | 3.00 | 12.4% | 89.9% | 104.4% | 0.93 |
| 2023-now out of sample | 382 | 33.2% | -0.01 | -20.9% | 4.9% | -0.05 | -0.09 | -2.9% | 69.4% | 2.61 | 37.0% | -10.8% | -35.5% | 0.30 |

### opposite

Blocked signals 2701. Exits: open 1, opposite_signal 105, stop 122.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 65 | 21.5% | 2.52 | 236.0% | 15.4% | 1.55 | 3.11 | 73.9% | 89.2% | 11.16 | 27.6% | 251.4% | 104.4% | 0.93 |
| 2023-now out of sample | 162 | 18.5% | 0.56 | 286.1% | 35.5% | 0.77 | 1.25 | 17.5% | 92.0% | 8.00 | 33.7% | 87.2% | -35.5% | 0.30 |

### two_close

Blocked signals 2916. Exits: open 2, two_lower_closes 11.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 11 | 0.0% | -1.39 | -14.3% | 32.9% | 0.45 | 0.69 | 7.8% | 94.3% | 22.17 | 71.6% | 18.5% | 104.4% | 0.93 |
| 2023-now out of sample | 0 | n/a | n/a | 0.0% | 23.8% | 0.10 | 0.14 | -2.0% | 100.0% | n/a | 54.8% | -7.7% | -35.5% | 0.30 |

### all

Blocked signals 2334. Exits: open 1, opposite_signal 34, stop 234, trail 292, two_lower_closes 34.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 197 | 38.1% | 0.35 | 81.6% | 4.5% | 1.48 | 2.93 | 31.5% | 67.1% | 2.80 | 13.4% | 86.2% | 104.4% | 0.93 |
| 2023-now out of sample | 397 | 32.0% | -0.03 | -32.3% | 4.4% | -0.15 | -0.25 | -4.8% | 67.7% | 2.43 | 40.4% | -17.3% | -35.5% | 0.30 |

## binance LINKUSDT

### baseline

Blocked signals 3791. Exits: open 2, stop 36, two_lower_closes 6.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 42 | 0.0% | -0.98 | -34.0% | 33.4% | 0.45 | 0.63 | -0.2% | 97.3% | 17.84 | 82.1% | -0.7% | 1018.5% | 1.11 |
| 2023-now out of sample | 0 | n/a | n/a | 0.0% | 68.1% | 0.42 | 0.64 | 7.8% | 100.0% | n/a | 64.7% | 33.7% | 62.9% | 0.56 |

### trail

Blocked signals 3069. Exits: open 1, stop 372, trail 393.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 386 | 32.4% | 0.03 | 4.7% | 1.3% | 0.17 | 0.29 | 1.5% | 67.0% | 2.57 | 36.8% | 5.9% | 1018.5% | 1.11 |
| 2023-now out of sample | 379 | 28.8% | -0.11 | -40.2% | 1.1% | -0.52 | -0.84 | -11.4% | 72.7% | 2.74 | 48.5% | -37.4% | 62.9% | 0.56 |

### opposite

Blocked signals 3497. Exits: open 1, opposite_signal 153, stop 184.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 147 | 23.8% | 0.72 | 144.8% | 6.0% | 1.06 | 1.72 | 26.2% | 90.0% | 8.72 | 23.3% | 150.8% | 1018.5% | 1.11 |
| 2023-now out of sample | 190 | 16.8% | 0.03 | -9.3% | 22.5% | 0.15 | 0.24 | 0.8% | 93.6% | 6.87 | 35.3% | 3.0% | 62.9% | 0.56 |

### two_close

Blocked signals 3809. Exits: open 2, two_lower_closes 24.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 24 | 0.0% | -1.37 | -28.3% | 145.5% | 0.68 | 0.99 | 21.7% | 97.6% | 17.78 | 85.8% | 117.2% | 1018.5% | 1.11 |
| 2023-now out of sample | 0 | n/a | n/a | 0.0% | 246.9% | 0.48 | 0.73 | 10.0% | 100.0% | n/a | 70.0% | 44.8% | 62.9% | 0.56 |

### all

Blocked signals 3043. Exits: open 1, opposite_signal 54, stop 327, trail 362, two_lower_closes 48.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 401 | 31.7% | 0.03 | 5.6% | 1.3% | 0.18 | 0.31 | 1.7% | 65.5% | 2.38 | 39.9% | 6.9% | 1018.5% | 1.11 |
| 2023-now out of sample | 390 | 27.7% | -0.08 | -33.4% | 1.3% | -0.38 | -0.60 | -9.0% | 71.7% | 2.58 | 43.7% | -30.6% | 62.9% | 0.56 |

## kucoin BTCUSDT

### baseline

Blocked signals 4206. Exits: open 2, stop 49, two_lower_closes 7.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 37 | 0.0% | -1.05 | -32.6% | 284.7% | 0.71 | 1.03 | 27.4% | 98.8% | 37.88 | 75.6% | 252.0% | 223.2% | 0.69 |
| 2023-now out of sample | 19 | 0.0% | -1.06 | -12.3% | 1224.6% | 0.96 | 1.47 | 39.5% | 100.0% | 62.41 | 53.0% | 264.8% | 281.3% | 0.98 |

### trail

Blocked signals 3377. Exits: open 1, stop 444, trail 442.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 509 | 29.9% | 0.03 | -0.8% | 0.3% | 0.10 | 0.17 | -0.1% | 68.0% | 2.57 | 43.6% | -0.5% | 223.2% | 0.69 |
| 2023-now out of sample | 377 | 27.6% | -0.17 | -49.4% | 1.4% | -0.71 | -1.05 | -15.8% | 71.1% | 2.71 | 58.3% | -48.7% | 281.3% | 0.98 |

### opposite

Blocked signals 3891. Exits: open 1, opposite_signal 172, stop 200.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 202 | 23.8% | 0.92 | 380.8% | 3.5% | 1.15 | 1.94 | 35.4% | 91.0% | 8.46 | 25.4% | 384.3% | 223.2% | 0.69 |
| 2023-now out of sample | 170 | 18.2% | 0.16 | 76.6% | 15.7% | 0.30 | 0.45 | 4.4% | 92.4% | 7.75 | 26.4% | 18.2% | 281.3% | 0.98 |

### two_close

Blocked signals 4214. Exits: open 2, two_lower_closes 48.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 32 | 0.0% | -1.51 | -38.9% | 263.7% | 0.68 | 0.99 | 25.4% | 98.8% | 44.48 | 75.7% | 224.8% | 223.2% | 0.69 |
| 2023-now out of sample | 16 | 0.0% | -1.16 | -10.4% | 1136.3% | 0.96 | 1.48 | 39.7% | 100.0% | 76.41 | 53.0% | 266.8% | 281.3% | 0.98 |

### all

Blocked signals 3355. Exits: open 1, opposite_signal 54, stop 408, trail 422, two_lower_closes 24.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 523 | 29.1% | 0.07 | 17.2% | 0.3% | 0.25 | 0.43 | 3.2% | 67.1% | 2.45 | 39.1% | 17.6% | 223.2% | 0.69 |
| 2023-now out of sample | 385 | 26.5% | -0.16 | -59.1% | 1.6% | -0.72 | -1.06 | -16.0% | 70.4% | 2.59 | 58.9% | -49.3% | 281.3% | 0.98 |

## kucoin ETHUSDT

### baseline

Blocked signals 4114. Exits: open 2, stop 26, two_lower_closes 5.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 27 | 0.0% | -0.97 | -23.3% | 250.4% | 0.69 | 1.00 | 25.6% | 98.8% | 68.86 | 75.3% | 227.1% | 306.8% | 0.78 |
| 2023-now out of sample | 4 | 0.0% | -1.10 | -3.3% | 376.5% | 0.43 | 0.64 | 8.6% | 100.0% | 338.38 | 64.6% | 37.9% | 48.6% | 0.47 |

### trail

Blocked signals 3322. Exits: open 1, stop 379, trail 445.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 468 | 33.3% | 0.09 | 39.0% | 0.0% | 0.42 | 0.68 | 6.5% | 68.8% | 2.81 | 28.9% | 39.0% | 306.8% | 0.78 |
| 2023-now out of sample | 356 | 32.9% | 0.05 | 14.9% | 4.7% | 0.27 | 0.46 | 3.5% | 70.5% | 2.86 | 38.6% | 14.1% | 48.6% | 0.47 |

### opposite

Blocked signals 3836. Exits: open 1, opposite_signal 148, stop 162.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 162 | 26.5% | 1.09 | 382.7% | 0.8% | 1.38 | 2.16 | 35.4% | 91.9% | 10.63 | 23.8% | 383.5% | 306.8% | 0.78 |
| 2023-now out of sample | 148 | 24.3% | 0.51 | 432.5% | 24.4% | 0.87 | 1.42 | 18.6% | 93.9% | 9.04 | 22.1% | 94.2% | 48.6% | 0.47 |

### two_close

Blocked signals 4119. Exits: open 2, two_lower_closes 26.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 22 | 0.0% | -1.42 | -27.3% | 118.2% | 0.50 | 0.71 | 13.2% | 98.8% | 67.03 | 68.3% | 90.9% | 306.8% | 0.78 |
| 2023-now out of sample | 4 | 0.0% | -1.54 | -4.4% | 170.7% | 0.36 | 0.54 | 6.0% | 100.0% | 339.50 | 59.2% | 25.5% | 48.6% | 0.47 |

### all

Blocked signals 3296. Exits: open 1, opposite_signal 42, stop 353, trail 413, two_lower_closes 42.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 478 | 32.2% | 0.09 | 37.0% | 0.0% | 0.41 | 0.65 | 6.2% | 67.9% | 2.69 | 26.8% | 37.0% | 306.8% | 0.78 |
| 2023-now out of sample | 372 | 31.2% | 0.04 | 9.9% | 4.5% | 0.23 | 0.39 | 2.6% | 69.0% | 2.63 | 40.5% | 10.5% | 48.6% | 0.47 |

## kucoin SOLUSDT

### baseline

Blocked signals 2347. Exits: open 2, stop 42, two_lower_closes 2.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 27 | 0.0% | -1.05 | -24.8% | 20.8% | -0.01 | -0.01 | -2.9% | 95.1% | 11.35 | 34.8% | -4.0% | -72.3% | -0.14 |
| 2023-now out of sample | 17 | 0.0% | -1.06 | -12.6% | 61.4% | 0.37 | 0.55 | 6.8% | 100.0% | 69.47 | 60.7% | 29.3% | 638.2% | 1.02 |

### trail

Blocked signals 1888. Exits: open 1, stop 230, trail 274.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 131 | 32.8% | 0.10 | 10.7% | 5.7% | 0.63 | 1.05 | 11.4% | 65.6% | 2.60 | 24.4% | 16.4% | -72.3% | -0.14 |
| 2023-now out of sample | 373 | 31.1% | 0.07 | 17.2% | 2.0% | 0.24 | 0.42 | 2.9% | 69.0% | 2.65 | 35.2% | 11.9% | 638.2% | 1.02 |

### opposite

Blocked signals 2199. Exits: open 1, opposite_signal 98, stop 95.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 51 | 13.7% | 0.36 | 17.2% | 6.3% | 0.84 | 1.38 | 16.1% | 88.9% | 8.66 | 18.8% | 23.4% | -72.3% | -0.14 |
| 2023-now out of sample | 142 | 26.1% | 0.58 | 114.8% | 15.6% | 0.88 | 1.41 | 19.6% | 93.9% | 9.23 | 19.0% | 100.7% | 638.2% | 1.02 |

### two_close

Blocked signals 2356. Exits: open 2, two_lower_closes 35.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 19 | 0.0% | -1.49 | -25.0% | 8.3% | -0.41 | -0.60 | -12.2% | 95.1% | 16.75 | 42.0% | -16.7% | -72.3% | -0.14 |
| 2023-now out of sample | 16 | 0.0% | -1.39 | -15.2% | 61.0% | 0.44 | 0.65 | 10.0% | 100.0% | 76.39 | 61.4% | 45.0% | 638.2% | 1.02 |

### all

Blocked signals 1876. Exits: open 1, opposite_signal 27, stop 201, trail 261, two_lower_closes 27.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 134 | 31.3% | 0.10 | 10.7% | 5.7% | 0.63 | 1.05 | 11.4% | 65.0% | 2.50 | 23.7% | 16.4% | -72.3% | -0.14 |
| 2023-now out of sample | 382 | 30.6% | 0.09 | 28.0% | 2.1% | 0.35 | 0.61 | 5.1% | 67.8% | 2.52 | 30.6% | 21.3% | 638.2% | 1.02 |

## kucoin ARBUSDT

### baseline

Blocked signals 1676. Exits: open 2, stop 43, two_lower_closes 4.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 0 | n/a | n/a | 0.0% | 0.0% | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2023-now out of sample | 47 | 0.0% | -1.04 | -39.0% | 13.2% | -0.31 | -0.47 | -7.8% | 97.4% | 17.34 | 42.7% | -25.8% | -90.3% | -0.17 |

### trail

Blocked signals 1382. Exits: open 1, stop 169, trail 173.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 0 | n/a | n/a | 0.0% | 0.0% | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2023-now out of sample | 342 | 32.2% | -0.07 | -25.5% | 1.6% | -0.31 | -0.50 | -7.2% | 68.0% | 2.69 | 32.7% | -23.9% | -90.3% | -0.17 |

### opposite

Blocked signals 1580. Exits: open 1, opposite_signal 58, stop 86.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 0 | n/a | n/a | 0.0% | 0.0% | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2023-now out of sample | 144 | 21.5% | 0.07 | 3.6% | 2.3% | 0.18 | 0.28 | 1.6% | 90.9% | 8.41 | 25.5% | 5.9% | -90.3% | -0.17 |

### two_close

Blocked signals 1687. Exits: open 2, two_lower_closes 36.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 0 | n/a | n/a | 0.0% | 0.0% | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2023-now out of sample | 36 | 0.0% | -1.36 | -39.1% | 13.3% | -0.31 | -0.48 | -7.8% | 97.4% | 26.21 | 45.6% | -25.7% | -90.3% | -0.17 |

### all

Blocked signals 1377. Exits: open 1, opposite_signal 18, stop 153, trail 159, two_lower_closes 17.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 0 | n/a | n/a | 0.0% | 0.0% | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2023-now out of sample | 347 | 32.0% | -0.06 | -22.8% | 1.7% | -0.26 | -0.41 | -6.3% | 67.2% | 2.59 | 30.5% | -21.1% | -90.3% | -0.17 |

## kucoin BNBUSDT

### baseline

Blocked signals 3443. Exits: open 2, stop 38, two_lower_closes 3.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 17 | 0.0% | -1.05 | -16.5% | 260.0% | 0.84 | 1.34 | 41.8% | 98.4% | 43.62 | 64.0% | 243.5% | 599.9% | 1.04 |
| 2023-now out of sample | 24 | 0.0% | -1.13 | -19.9% | 624.2% | 0.62 | 0.92 | 19.5% | 100.0% | 45.10 | 55.9% | 100.0% | 136.6% | 0.69 |

### trail

Blocked signals 2810. Exits: open 1, stop 316, trail 359.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 315 | 32.7% | -0.01 | -10.3% | 3.5% | -0.03 | -0.05 | -3.0% | 68.5% | 2.84 | 37.8% | -10.1% | 599.9% | 1.04 |
| 2023-now out of sample | 360 | 29.2% | -0.10 | -32.3% | 2.8% | -0.36 | -0.61 | -9.8% | 66.8% | 2.66 | 40.2% | -32.9% | 136.6% | 0.69 |

### opposite

Blocked signals 3202. Exits: open 1, opposite_signal 140, stop 143.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 134 | 20.9% | 2.52 | 352.2% | 28.8% | 1.18 | 2.24 | 56.0% | 91.0% | 8.63 | 33.8% | 381.0% | 599.9% | 1.04 |
| 2023-now out of sample | 149 | 22.1% | 0.69 | 563.4% | 22.2% | 0.82 | 1.33 | 21.9% | 92.7% | 8.81 | 34.5% | 115.9% | 136.6% | 0.69 |

### two_close

Blocked signals 3454. Exits: open 2, two_lower_closes 30.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 13 | 0.0% | -3.68 | -40.9% | 191.0% | 0.71 | 1.11 | 29.6% | 98.4% | 61.73 | 64.4% | 150.1% | 599.9% | 1.04 |
| 2023-now out of sample | 17 | 0.0% | -1.52 | -13.5% | 459.0% | 0.63 | 0.93 | 19.8% | 100.0% | 66.88 | 56.0% | 101.5% | 136.6% | 0.69 |

### all

Blocked signals 2777. Exits: open 1, opposite_signal 54, stop 276, trail 339, two_lower_closes 39.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 330 | 31.5% | -0.03 | -15.4% | 3.3% | -0.10 | -0.17 | -4.6% | 67.6% | 2.64 | 40.5% | -15.2% | 599.9% | 1.04 |
| 2023-now out of sample | 378 | 28.6% | -0.12 | -34.6% | 2.4% | -0.45 | -0.74 | -11.6% | 65.9% | 2.45 | 44.8% | -38.0% | 136.6% | 0.69 |

## kucoin XRPUSDT

### baseline

Blocked signals 3395. Exits: open 2, stop 42, two_lower_closes 9.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 40 | 0.0% | -1.05 | -34.6% | 14.9% | -0.01 | -0.01 | -5.2% | 96.5% | 22.65 | 46.7% | -19.7% | -3.0% | 0.55 |
| 2023-now out of sample | 11 | 0.0% | -1.05 | -7.2% | 46.0% | 0.37 | 0.59 | 7.0% | 100.0% | 117.55 | 54.0% | 30.1% | 185.5% | 0.70 |

### trail

Blocked signals 2743. Exits: open 1, stop 361, trail 343.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 327 | 31.5% | 0.15 | 46.8% | 0.0% | 0.52 | 0.93 | 9.9% | 63.5% | 2.88 | 29.0% | 46.8% | -3.0% | 0.55 |
| 2023-now out of sample | 377 | 27.9% | -0.08 | -48.1% | 1.7% | -0.39 | -0.65 | -9.3% | 68.4% | 2.65 | 40.1% | -31.6% | 185.5% | 0.70 |

### opposite

Blocked signals 3101. Exits: open 1, opposite_signal 139, stop 207.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 143 | 21.0% | 0.26 | 32.7% | 3.7% | 0.43 | 0.68 | 7.9% | 88.2% | 8.75 | 20.2% | 36.4% | -3.0% | 0.55 |
| 2023-now out of sample | 203 | 14.3% | -0.05 | -35.4% | 3.4% | -0.23 | -0.36 | -7.6% | 91.9% | 6.45 | 42.6% | -26.5% | 185.5% | 0.70 |

### two_close

Blocked signals 3406. Exits: open 2, two_lower_closes 40.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 31 | 0.0% | -2.04 | -48.4% | 12.2% | -0.16 | -0.23 | -10.4% | 97.8% | 30.89 | 48.2% | -36.2% | -3.0% | 0.55 |
| 2023-now out of sample | 9 | 0.0% | -1.46 | -6.4% | 38.3% | 0.37 | 0.60 | 7.2% | 100.0% | 145.26 | 55.4% | 31.2% | 185.5% | 0.70 |

### all

Blocked signals 2715. Exits: open 1, opposite_signal 53, stop 331, trail 323, two_lower_closes 25.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 340 | 30.9% | 0.15 | 50.1% | 0.0% | 0.53 | 0.96 | 10.5% | 63.1% | 2.70 | 27.6% | 50.1% | -3.0% | 0.55 |
| 2023-now out of sample | 392 | 26.0% | -0.08 | -52.4% | 1.6% | -0.41 | -0.69 | -10.1% | 67.7% | 2.46 | 39.3% | -33.8% | 185.5% | 0.70 |

## kucoin ADAUSDT

### baseline

Blocked signals 3449. Exits: open 2, stop 40, two_lower_closes 4.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 44 | 0.0% | -1.02 | -36.3% | 133.4% | 0.64 | 1.00 | 21.4% | 95.7% | 11.02 | 89.1% | 97.1% | 211.1% | 0.85 |
| 2023-now out of sample | 0 | n/a | n/a | 0.0% | 78.0% | 0.23 | 0.37 | -8.2% | 100.0% | n/a | 82.3% | -28.1% | -38.4% | 0.26 |

### trail

Blocked signals 2769. Exits: open 1, stop 355, trail 370.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 359 | 32.0% | 0.15 | 50.2% | 0.0% | 0.61 | 1.14 | 12.3% | 67.7% | 2.45 | 21.1% | 50.2% | 211.1% | 0.85 |
| 2023-now out of sample | 366 | 33.3% | -0.13 | -61.6% | 1.8% | -0.59 | -0.94 | -12.3% | 69.8% | 2.74 | 48.0% | -39.9% | -38.4% | 0.26 |

### opposite

Blocked signals 3169. Exits: open 1, opposite_signal 139, stop 186.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 158 | 16.5% | 0.26 | 23.6% | 3.3% | 0.39 | 0.55 | 7.1% | 88.6% | 6.82 | 36.7% | 26.9% | 211.1% | 0.85 |
| 2023-now out of sample | 167 | 18.0% | -0.10 | -24.7% | 6.3% | -0.17 | -0.25 | -4.7% | 91.5% | 7.88 | 28.2% | -17.1% | -38.4% | 0.26 |

### two_close

Blocked signals 3467. Exits: open 2, two_lower_closes 26.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 26 | 0.0% | -1.96 | -40.6% | 139.1% | 0.64 | 1.01 | 21.7% | 96.9% | 22.73 | 89.5% | 98.5% | 211.1% | 0.85 |
| 2023-now out of sample | 0 | n/a | n/a | 0.0% | 80.9% | 0.23 | 0.38 | -8.5% | 100.0% | n/a | 83.1% | -29.3% | -38.4% | 0.26 |

### all

Blocked signals 2739. Exits: open 1, opposite_signal 49, stop 321, trail 346, two_lower_closes 39.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 375 | 30.4% | 0.11 | 32.1% | 0.0% | 0.46 | 0.85 | 8.3% | 66.5% | 2.28 | 23.5% | 32.1% | 211.1% | 0.85 |
| 2023-now out of sample | 380 | 31.3% | -0.14 | -59.1% | 1.5% | -0.77 | -1.15 | -13.7% | 68.7% | 2.53 | 51.1% | -43.6% | -38.4% | 0.26 |

## kucoin DOGEUSDT

### baseline

Blocked signals 2572. Exits: open 1, stop 21.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 11 | 0.0% | -1.07 | -11.1% | 8.2% | 0.05 | 0.09 | -1.6% | 94.3% | 44.67 | 32.7% | -2.9% | -2.3% | 0.69 |
| 2023-now out of sample | 10 | 0.0% | -1.19 | -10.0% | 7.7% | 0.17 | 0.26 | -3.0% | 100.0% | 138.80 | 70.6% | -11.2% | -16.3% | 0.36 |

### trail

Blocked signals 2073. Exits: open 1, stop 248, trail 272.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 135 | 34.1% | 0.16 | 21.1% | -0.3% | 0.59 | 1.06 | 11.2% | 59.9% | 3.14 | 19.5% | 22.1% | -2.3% | 0.69 |
| 2023-now out of sample | 385 | 29.1% | 0.05 | 6.2% | -0.1% | 0.17 | 0.28 | 1.3% | 68.5% | 2.61 | 33.9% | 5.1% | -16.3% | 0.36 |

### opposite

Blocked signals 2378. Exits: open 1, opposite_signal 91, stop 124.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 57 | 17.5% | 0.45 | 23.5% | 3.1% | 0.58 | 0.94 | 13.3% | 86.8% | 10.39 | 20.3% | 26.6% | -2.3% | 0.69 |
| 2023-now out of sample | 158 | 22.2% | 0.85 | 217.5% | 12.8% | 0.98 | 1.60 | 30.5% | 92.5% | 8.22 | 25.1% | 181.3% | -16.3% | 0.36 |

### two_close

Blocked signals 2574. Exits: open 1, two_lower_closes 19.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 10 | 0.0% | -1.59 | -14.9% | 3.3% | -0.13 | -0.20 | -6.3% | 94.6% | 51.04 | 38.2% | -11.6% | -2.3% | 0.69 |
| 2023-now out of sample | 9 | 0.0% | -1.94 | -13.7% | 2.7% | 0.15 | 0.23 | -4.6% | 100.0% | 155.06 | 72.4% | -16.6% | -16.3% | 0.36 |

### all

Blocked signals 2042. Exits: open 1, opposite_signal 37, stop 229, trail 255, two_lower_closes 30.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 142 | 32.4% | 0.14 | 18.4% | -0.3% | 0.53 | 0.95 | 9.8% | 59.3% | 2.91 | 21.3% | 19.4% | -2.3% | 0.69 |
| 2023-now out of sample | 409 | 28.1% | -0.03 | -26.6% | -0.1% | -0.21 | -0.33 | -6.4% | 67.7% | 2.38 | 35.7% | -22.5% | -16.3% | 0.36 |

## kucoin AVAXUSDT

### baseline

Blocked signals 2629. Exits: open 2, stop 32, two_lower_closes 4.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 16 | 0.0% | -1.03 | -15.4% | 14.3% | 0.23 | 0.34 | -0.6% | 94.4% | 39.84 | 62.1% | -1.1% | -55.4% | 0.36 |
| 2023-now out of sample | 20 | 0.0% | -1.03 | -15.8% | 15.7% | 0.06 | 0.09 | -4.0% | 100.0% | 47.92 | 54.6% | -14.6% | -35.5% | 0.30 |

### trail

Blocked signals 2132. Exits: open 1, stop 254, trail 280.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 155 | 36.1% | 0.20 | 29.5% | 3.7% | 0.96 | 1.69 | 17.1% | 68.5% | 2.93 | 14.6% | 33.3% | -55.4% | 0.36 |
| 2023-now out of sample | 379 | 32.5% | -0.02 | -19.7% | 3.2% | -0.10 | -0.17 | -4.1% | 68.5% | 2.60 | 39.8% | -15.0% | -35.5% | 0.30 |

### opposite

Blocked signals 2478. Exits: open 1, opposite_signal 87, stop 101.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 48 | 22.9% | 1.69 | 82.2% | 8.4% | 1.25 | 2.05 | 42.5% | 90.4% | 12.19 | 17.4% | 90.6% | -55.4% | 0.36 |
| 2023-now out of sample | 140 | 21.4% | 0.60 | 152.2% | 40.7% | 0.83 | 1.33 | 19.1% | 93.2% | 9.32 | 29.9% | 96.9% | -35.5% | 0.30 |

### two_close

Blocked signals 2642. Exits: open 2, two_lower_closes 23.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 12 | 0.0% | -1.73 | -19.1% | 13.9% | 0.19 | 0.27 | -2.9% | 94.6% | 55.81 | 62.9% | -5.2% | -55.4% | 0.36 |
| 2023-now out of sample | 11 | 0.0% | -1.45 | -12.0% | 15.2% | 0.09 | 0.12 | -3.0% | 100.0% | 98.66 | 55.7% | -11.3% | -35.5% | 0.30 |

### all

Blocked signals 2118. Exits: open 1, opposite_signal 22, stop 233, trail 266, two_lower_closes 27.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 161 | 35.4% | 0.17 | 25.2% | 3.6% | 0.85 | 1.50 | 14.9% | 67.3% | 2.76 | 18.8% | 28.8% | -55.4% | 0.36 |
| 2023-now out of sample | 387 | 31.3% | -0.01 | -15.7% | 3.2% | -0.06 | -0.10 | -3.3% | 67.9% | 2.48 | 38.3% | -12.4% | -35.5% | 0.30 |

## kucoin LINKUSDT

### baseline

Blocked signals 2955. Exits: open 2, stop 49, two_lower_closes 7.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 46 | 0.0% | -0.99 | -36.9% | 3.2% | -0.82 | -1.04 | -15.9% | 93.7% | 12.72 | 36.0% | -33.6% | -65.9% | 0.25 |
| 2023-now out of sample | 10 | 0.0% | -1.08 | -6.5% | 13.5% | 0.26 | 0.40 | 1.4% | 100.0% | 16.78 | 55.3% | 5.7% | 63.0% | 0.56 |

### trail

Blocked signals 2424. Exits: open 1, stop 293, trail 295.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 228 | 31.6% | -0.17 | -34.3% | 0.8% | -1.06 | -1.51 | -15.8% | 64.9% | 2.52 | 39.0% | -33.5% | -65.9% | 0.25 |
| 2023-now out of sample | 360 | 28.6% | -0.02 | -9.9% | 1.0% | -0.05 | -0.10 | -3.8% | 71.1% | 2.81 | 40.9% | -13.9% | 63.0% | 0.56 |

### opposite

Blocked signals 2741. Exits: open 1, opposite_signal 130, stop 141.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 98 | 17.3% | -0.22 | -21.2% | 2.0% | -0.42 | -0.55 | -8.7% | 89.0% | 7.57 | 30.2% | -19.3% | -65.9% | 0.25 |
| 2023-now out of sample | 173 | 18.5% | 0.25 | 28.8% | 10.5% | 0.48 | 0.82 | 10.3% | 94.1% | 7.61 | 28.1% | 46.4% | 63.0% | 0.56 |

### two_close

Blocked signals 2971. Exits: open 2, two_lower_closes 40.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 31 | 0.0% | -1.24 | -32.2% | 4.3% | -0.38 | -0.51 | -12.9% | 95.2% | 21.96 | 39.6% | -27.9% | -65.9% | 0.25 |
| 2023-now out of sample | 9 | 0.0% | -1.29 | -7.5% | 15.3% | 0.26 | 0.39 | 1.2% | 100.0% | 19.43 | 55.0% | 4.8% | 63.0% | 0.56 |

### all

Blocked signals 2400. Exits: open 1, opposite_signal 41, stop 258, trail 274, two_lower_closes 39.

| Window | Closed | Win rate | Avg R | Realized | Unrealized | Sharpe | Sortino | CAGR | Exposure | Avg days | Max DD | Return | Buy & hold | BH Sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 240 | 29.6% | -0.17 | -35.6% | 0.8% | -1.10 | -1.56 | -16.5% | 64.5% | 2.32 | 40.2% | -34.7% | -65.9% | 0.25 |
| 2023-now out of sample | 372 | 28.0% | -0.02 | -9.4% | 1.0% | -0.04 | -0.08 | -3.6% | 69.7% | 2.64 | 41.9% | -13.3% | 63.0% | 0.56 |

