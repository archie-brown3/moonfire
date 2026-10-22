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
| 14 | profile over 1 day | 18.49 | no |
| 15 | lookback 4 days (192) with filter | 23.19 | no |
| 16 | lookback 10 days (480) with filter | 22.47 | no |
| 17 | always charge on negative latest price | 25.12 | yes |
| 18 | spike override: discharge above 98th pct any time | 24.29 | no |
| 19 | charge only if 0.9*hi - latest > 20 (spread covers losses) | 25.93 | yes |
| 20 | spread margin 30 | 24.47 | no |
| 21 | spread margin 15 | 25.54 | no |
| 22 | charge quantile 0.3 with margin | 25.12 | no |
| 23 | discharge quantile 0.85 | 23.39 | no |
| 24 | discharge quantile 0.75 | 26.03 | yes |
