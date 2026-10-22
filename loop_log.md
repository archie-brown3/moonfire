| iter | idea | score | kept? |
|---|---|---|---|
| 0 | seed rolling-percentile (96, 0.2/0.8) | 15.39 | baseline |
| 1 | 7-day time-of-day profile, rank top/bottom 5 slots | 9.15 | no |
| 2 | seed + forecast latest + yesterday's move | 8.02 | no |
| 3 | seed with 7-day lookback (336) | 20.18 | yes |
| 4 | 14-day lookback (672) | 19.93 | no |
| 5 | quantiles 0.25/0.75 | 14.99 | no |
| 6 | quantiles 0.15/0.85 | 19.56 | no |
| 7 | SoC-aware quantile shift (±0.1) | 14.22 | no |
| 8 | + time-of-day filter (weekly profile rank half-day) | 22.24 | yes |
| 9 | time-of-day filter tightened to thirds (16/32) | 22.59 | yes |
| 10 | quantiles 0.3/0.7 with filter | 20.03 | no |
| 11 | blend forecast 0.7 latest + 0.3 profile | 21.60 | no |
| 12 | profile over 3 days instead of 7 | 24.01 | yes |
| 13 | profile over 2 days | 24.12 | yes |
