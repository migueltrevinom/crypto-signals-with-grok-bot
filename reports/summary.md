# time@mode paper backtest

No parameter optimization. Fees are 0.1% taker per side. Slippage is 5 bps.
Starting equity is 10,000 USDT per pair. One position at a time.
R is net PnL divided by the 1% risk budget. Buy-and-hold is the daily close change.
In-sample is 2017-2022 and out-of-sample is 2023 onward. The same rules run on both.

## binance BTCUSDT

History 2017-08-17 to 2026-11-19. Signals 4281.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 17 | 5.9% | 5.92 | 5.92 | 6.27 | 15.8% | 83.3% | 287.6% |
| 2023-now out of sample | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 281.3% |
| 2018 bear | 3 | 0.0% | -1.05 | -1.05 | 0.00 | 3.0% | -3.0% | -72.3% |
| 2019 recovery | 1 | 0.0% | -1.05 | -1.05 | 0.00 | 1.0% | -1.0% | 134.8% |
| 2020 crash | 9 | 11.1% | 12.12 | 12.12 | 12.97 | 7.6% | 91.4% | 3.0% |
| 2020-21 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 570.3% |
| 2022 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -64.1% |
| 2023 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 154.7% |
| 2024 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 119.5% |
| 2025-2026 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -32.6% |

## binance ETHUSDT

History 2017-08-17 to 2026-11-19. Signals 4141.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 13 | 7.7% | 7.18 | 7.18 | 8.02 | 11.6% | 81.7% | 297.3% |
| 2023-now out of sample | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 48.6% |
| 2018 bear | 1 | 0.0% | -0.70 | -0.70 | 0.00 | 0.7% | -0.7% | -81.2% |
| 2019 recovery | 8 | 0.0% | -1.06 | -1.06 | 0.00 | 7.9% | -7.9% | 72.5% |
| 2020 crash | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -0.9% |
| 2020-21 bull | 1 | 100.0% | 105.64 | 105.64 | inf | 0.0% | 93.3% | 2056.7% |
| 2022 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -67.4% |
| 2023 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 91.6% |
| 2024 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 47.3% |
| 2025-2026 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -46.8% |

## binance SOLUSDT

History 2020-08-11 to 2026-11-19. Signals 2962.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 3 | 33.3% | 86.62 | 86.62 | 125.39 | 2.0% | 254.5% | 200.1% |
| 2023-now out of sample | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 638.6% |
| 2018 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2019 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2020 crash | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2020-21 bull | 3 | 33.3% | 86.62 | 86.62 | 125.39 | 2.0% | 254.5% | 6087.4% |
| 2022 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -94.2% |
| 2023 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 922.1% |
| 2024 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 88.1% |
| 2025-2026 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -61.1% |

## binance ARBUSDT

History 2023-03-23 to 2026-11-19. Signals 1706.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2023-now out of sample | 25 | 4.0% | -0.75 | -0.75 | 0.20 | 21.7% | -17.3% | -90.4% |
| 2018 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2019 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2020 crash | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2020-21 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2022 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2023 recovery | 11 | 0.0% | -1.05 | -1.05 | 0.00 | 10.9% | -10.9% | 12.0% |
| 2024 bull | 9 | 0.0% | -0.99 | -0.99 | 0.00 | 7.6% | -7.6% | -53.0% |
| 2025-2026 | 5 | 20.0% | 0.33 | 0.33 | 1.38 | 3.2% | 1.2% | -82.4% |

## binance BNBUSDT

History 2017-11-06 to 2026-11-19. Signals 4236.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 2 | 50.0% | 1289.38 | 1289.38 | 6267.24 | 0.4% | 2568.2% | 15546.1% |
| 2023-now out of sample | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 136.6% |
| 2018 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -30.9% |
| 2019 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 210.6% |
| 2020 crash | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -9.7% |
| 2020-21 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 3577.0% |
| 2022 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -51.9% |
| 2023 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 28.7% |
| 2024 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 126.2% |
| 2025-2026 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -17.0% |

## binance XRPUSDT

History 2018-05-04 to 2026-11-19. Signals 3779.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 35 | 0.0% | -1.06 | -1.06 | 0.00 | 31.1% | -31.1% | -61.2% |
| 2023-now out of sample | 7 | 14.3% | 0.71 | 0.71 | 1.74 | 4.2% | 3.1% | 185.5% |
| 2018 bear | 13 | 0.0% | -1.06 | -1.06 | 0.00 | 12.9% | -12.9% | -59.0% |
| 2019 recovery | 3 | 0.0% | -1.08 | -1.08 | 0.00 | 2.8% | -2.8% | -32.1% |
| 2020 crash | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -1.1% |
| 2020-21 bull | 10 | 0.0% | -1.05 | -1.05 | 0.00 | 8.4% | -8.4% | 368.3% |
| 2022 bear | 9 | 0.0% | -1.07 | -1.07 | 0.00 | 7.0% | -7.0% | -58.4% |
| 2023 recovery | 7 | 14.3% | 0.71 | 0.71 | 1.74 | 4.2% | 3.1% | 83.2% |
| 2024 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 234.4% |
| 2025-2026 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -53.6% |

## binance ADAUSDT

History 2018-04-17 to 2026-11-19. Signals 4163.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 6 | 0.0% | -0.95 | -0.95 | 0.00 | 5.6% | -5.6% | 1.3% |
| 2023-now out of sample | 25 | 4.0% | -0.56 | -0.56 | 0.38 | 20.9% | -13.0% | -38.4% |
| 2018 bear | 2 | 0.0% | -0.79 | -0.79 | 0.00 | 1.6% | -1.6% | -82.4% |
| 2019 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 20.5% |
| 2020 crash | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 9.3% |
| 2020-21 bull | 3 | 0.0% | -1.04 | -1.04 | 0.00 | 3.0% | -3.0% | 3269.1% |
| 2022 bear | 1 | 0.0% | -1.02 | -1.02 | 0.00 | 1.0% | -1.0% | -81.2% |
| 2023 recovery | 9 | 0.0% | -1.03 | -1.03 | 0.00 | 8.4% | -8.4% | 144.5% |
| 2024 bull | 14 | 0.0% | -1.07 | -1.07 | 0.00 | 12.0% | -12.0% | 45.0% |
| 2025-2026 | 2 | 50.0% | 5.05 | 5.05 | 16.26 | 0.5% | 7.4% | -82.1% |

## binance DOGEUSDT

History 2019-07-05 to 2026-11-19. Signals 3367.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 23 | 4.3% | 13.19 | 13.19 | 12.84 | 20.2% | 239.7% | 1667.4% |
| 2023-now out of sample | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -16.3% |
| 2018 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2019 recovery | 13 | 0.0% | -0.96 | -0.96 | 0.00 | 11.7% | -11.7% | -41.0% |
| 2020 crash | 3 | 0.0% | -1.08 | -1.08 | 0.00 | 2.8% | -2.8% | 12.5% |
| 2020-21 bull | 7 | 14.3% | 45.59 | 45.59 | 45.96 | 5.7% | 254.3% | 8736.8% |
| 2022 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -59.8% |
| 2023 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 28.1% |
| 2024 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 250.6% |
| 2025-2026 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -81.4% |

## binance AVAXUSDT

History 2020-09-22 to 2026-11-19. Signals 2929.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 6 | 16.7% | 0.76 | 0.76 | 1.80 | 5.2% | 4.1% | 104.4% |
| 2023-now out of sample | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -35.5% |
| 2018 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2019 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2020 crash | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2020-21 bull | 6 | 16.7% | 0.76 | 0.76 | 1.80 | 5.2% | 4.1% | 2163.3% |
| 2022 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -90.1% |
| 2023 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 260.8% |
| 2024 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -6.7% |
| 2025-2026 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -80.3% |

## binance LINKUSDT

History 2019-01-16 to 2026-11-19. Signals 3835.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 15 | 6.7% | 4.34 | 4.34 | 4.98 | 13.8% | 55.0% | 1018.5% |
| 2023-now out of sample | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 62.9% |
| 2018 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2019 recovery | 9 | 0.0% | -1.07 | -1.07 | 0.00 | 9.2% | -9.2% | 750.0% |
| 2020 crash | 6 | 16.7% | 12.45 | 12.45 | 14.85 | 4.6% | 64.2% | -4.2% |
| 2020-21 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 574.9% |
| 2022 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -71.9% |
| 2023 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 172.1% |
| 2024 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 37.7% |
| 2025-2026 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -54.6% |

## kucoin BTCUSDT

History 2017-10-19 to 2026-11-19. Signals 4264.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 49 | 2.0% | 6.09 | 6.09 | 5.16 | 40.4% | 168.1% | 223.2% |
| 2023-now out of sample | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 281.3% |
| 2018 bear | 10 | 0.0% | -1.04 | -1.04 | 0.00 | 9.8% | -9.8% | -70.6% |
| 2019 recovery | 26 | 0.0% | -1.08 | -1.08 | 0.00 | 21.8% | -21.8% | 135.0% |
| 2020 crash | 2 | 0.0% | -1.06 | -1.06 | 0.00 | 1.4% | -1.4% | 2.9% |
| 2020-21 bull | 10 | 10.0% | 34.01 | 34.01 | 32.95 | 6.3% | 202.2% | 569.9% |
| 2022 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -64.1% |
| 2023 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 154.8% |
| 2024 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 119.5% |
| 2025-2026 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -32.6% |

## kucoin ETHUSDT

History 2017-10-19 to 2026-11-19. Signals 4147.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 22 | 4.5% | 1.73 | 1.73 | 2.41 | 20.0% | 28.2% | 306.8% |
| 2023-now out of sample | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 48.6% |
| 2018 bear | 11 | 0.0% | -1.08 | -1.08 | 0.00 | 11.1% | -11.1% | -80.9% |
| 2019 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 72.7% |
| 2020 crash | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -0.9% |
| 2020-21 bull | 10 | 10.0% | 5.09 | 5.09 | 6.17 | 7.8% | 40.4% | 2055.7% |
| 2022 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -67.4% |
| 2023 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 91.6% |
| 2024 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 47.3% |
| 2025-2026 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -46.8% |

## kucoin SOLUSDT

History 2021-08-04 to 2026-11-19. Signals 2393.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 10 | 0.0% | -1.03 | -1.03 | 0.00 | 9.8% | -9.8% | -72.3% |
| 2023-now out of sample | 17 | 5.9% | -0.87 | -0.87 | 0.13 | 14.3% | -12.5% | 638.2% |
| 2018 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2019 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2020 crash | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2020-21 bull | 1 | 0.0% | -1.08 | -1.08 | 0.00 | 1.1% | -1.1% | 470.0% |
| 2022 bear | 9 | 0.0% | -1.02 | -1.02 | 0.00 | 8.7% | -8.7% | -94.2% |
| 2023 recovery | 1 | 0.0% | -1.02 | -1.02 | 0.00 | 0.9% | -0.9% | 921.2% |
| 2024 bull | 8 | 0.0% | -1.07 | -1.07 | 0.00 | 7.4% | -7.4% | 88.1% |
| 2025-2026 | 8 | 12.5% | -0.65 | -0.65 | 0.31 | 6.0% | -4.2% | -61.1% |

## kucoin ARBUSDT

History 2023-03-23 to 2026-11-19. Signals 1725.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2023-now out of sample | 35 | 2.9% | -0.59 | -0.59 | 0.33 | 29.1% | -19.6% | -90.3% |
| 2018 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2019 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2020 crash | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2020-21 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2022 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2023 recovery | 18 | 0.0% | -1.05 | -1.05 | 0.00 | 17.3% | -17.3% | 12.3% |
| 2024 bull | 12 | 0.0% | -0.95 | -0.95 | 0.00 | 9.0% | -9.0% | -53.0% |
| 2025-2026 | 5 | 20.0% | 1.90 | 1.90 | 3.39 | 2.8% | 6.7% | -82.4% |

## kucoin BNBUSDT

History 2019-06-19 to 2026-11-19. Signals 3486.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 15 | 6.7% | 31.98 | 31.98 | 31.72 | 13.5% | 414.1% | 599.9% |
| 2023-now out of sample | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 136.6% |
| 2018 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2019 recovery | 1 | 0.0% | -1.07 | -1.07 | 0.00 | 1.1% | -1.1% | -45.8% |
| 2020 crash | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -9.9% |
| 2020-21 bull | 14 | 7.1% | 34.34 | 34.34 | 34.47 | 12.4% | 415.1% | 3566.5% |
| 2022 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -51.9% |
| 2023 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 28.7% |
| 2024 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 126.1% |
| 2025-2026 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -17.0% |

## kucoin XRPUSDT

History 2018-12-04 to 2026-11-19. Signals 3448.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 43 | 2.3% | 0.01 | 0.01 | 0.80 | 35.1% | -7.0% | -3.0% |
| 2023-now out of sample | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 185.5% |
| 2018 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 5.3% |
| 2019 recovery | 26 | 0.0% | -1.04 | -1.04 | 0.00 | 23.9% | -23.9% | -34.4% |
| 2020 crash | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -1.0% |
| 2020-21 bull | 17 | 5.9% | 1.61 | 1.61 | 2.50 | 11.2% | 16.9% | 368.4% |
| 2022 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -58.4% |
| 2023 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 83.1% |
| 2024 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 234.4% |
| 2025-2026 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -53.6% |

## kucoin ADAUSDT

History 2019-07-04 to 2026-11-19. Signals 3495.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 31 | 3.2% | -0.70 | -0.70 | 0.24 | 25.9% | -19.8% | 211.1% |
| 2023-now out of sample | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -38.4% |
| 2018 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2019 recovery | 30 | 0.0% | -0.99 | -0.99 | 0.00 | 25.9% | -25.9% | -38.2% |
| 2020 crash | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 8.8% |
| 2020-21 bull | 1 | 100.0% | 8.22 | 8.22 | inf | 0.0% | 6.1% | 3265.7% |
| 2022 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -81.2% |
| 2023 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 144.5% |
| 2024 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 44.9% |
| 2025-2026 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | -82.1% |

## kucoin DOGEUSDT

History 2021-02-09 to 2026-11-19. Signals 2594.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 16 | 0.0% | -1.07 | -1.07 | 0.00 | 15.8% | -15.8% | -2.3% |
| 2023-now out of sample | 22 | 4.5% | -0.93 | -0.93 | 0.06 | 16.7% | -15.6% | -16.3% |
| 2018 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2019 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2020 crash | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2020-21 bull | 3 | 0.0% | -1.05 | -1.05 | 0.00 | 3.1% | -3.1% | 207.1% |
| 2022 bear | 13 | 0.0% | -1.07 | -1.07 | 0.00 | 12.6% | -12.6% | -59.8% |
| 2023 recovery | 21 | 0.0% | -1.05 | -1.05 | 0.00 | 16.7% | -16.7% | 28.2% |
| 2024 bull | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 250.6% |
| 2025-2026 | 1 | 100.0% | 1.55 | 1.55 | inf | 0.0% | 1.0% | -81.4% |

## kucoin AVAXUSDT

History 2021-03-05 to 2026-11-19. Signals 2667.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 17 | 0.0% | -1.02 | -1.02 | 0.00 | 15.9% | -15.9% | -55.4% |
| 2023-now out of sample | 19 | 5.3% | -0.44 | -0.44 | 0.50 | 14.5% | -7.3% | -35.5% |
| 2018 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2019 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2020 crash | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2020-21 bull | 10 | 0.0% | -1.00 | -1.00 | 0.00 | 9.5% | -9.5% | 394.4% |
| 2022 bear | 7 | 0.0% | -1.05 | -1.05 | 0.00 | 6.4% | -6.4% | -90.1% |
| 2023 recovery | 3 | 0.0% | -0.95 | -0.95 | 0.00 | 2.4% | -2.4% | 260.7% |
| 2024 bull | 11 | 0.0% | -1.08 | -1.08 | 0.00 | 9.2% | -9.2% | -6.7% |
| 2025-2026 | 5 | 20.0% | 1.24 | 1.24 | 2.42 | 3.0% | 4.2% | -80.3% |

## kucoin LINKUSDT

History 2020-08-20 to 2026-11-19. Signals 3013.

| Window | Trades | Win rate | Avg R | Expectancy | Profit factor | Max DD | Strategy | Buy & hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2017-2022 in sample | 23 | 0.0% | -1.05 | -1.05 | 0.00 | 21.5% | -21.5% | -65.9% |
| 2023-now out of sample | 19 | 5.3% | -0.63 | -0.63 | 0.32 | 13.5% | -9.1% | 63.0% |
| 2018 bear | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2019 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2020 crash | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2020-21 bull | 17 | 0.0% | -1.05 | -1.05 | 0.00 | 16.4% | -16.4% | 55.4% |
| 2022 bear | 2 | 0.0% | -1.04 | -1.04 | 0.00 | 1.7% | -1.7% | -71.9% |
| 2023 recovery | 0 | n/a | n/a | n/a | n/a | n/a | n/a | 172.1% |
| 2024 bull | 7 | 0.0% | -1.09 | -1.09 | 0.00 | 5.8% | -5.8% | 37.7% |
| 2025-2026 | 12 | 8.3% | -0.37 | -0.37 | 0.57 | 7.7% | -3.3% | -54.6% |

