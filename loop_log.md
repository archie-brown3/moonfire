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
| 25 | discharge quantile 0.70 | 24.85 | no |
| 26 | lookback 2 days with current rules | 24.53 | no |
| 27 | full battery (soc>1.5) sells above median in dear third | 25.26 | no |
| 28 | profile from yesterday + same day last week | 23.34 | no |
| 29 | filter quarters (12/36) | 24.69 | no |
| 30 | filter widened (20/28) | 26.33 | yes |
| 31 | filter even split (24/24) | 25.21 | no |
| 32 | momentum: discharge only if latest >= previous | 24.13 | no |
| 33 | momentum: charge only if latest <= previous | 25.35 | no |
| 34 | smooth latest over last 2 periods | 27.54 | yes |
| 35 | smooth over 3 periods | 27.48 | no |
| 36 | negative check on raw latest price | 27.50 | no |
| 37 | charge quantile 0.25 | 26.82 | no |
| 38 | charge quantile 0.15 | 26.59 | no |
| 39 | rank now within next 12h of profile (not whole day) | 28.20 | yes |
| 40 | 8-hour horizon (HORIZON=16) for time-of-day rank | 28.39 | yes |
| 41 | 6-hour horizon (HORIZON=12) | 29.01 | yes |
| 42 | 4-hour horizon (HORIZON=8) | 27.90 | no |
| 43 | charge rank threshold 0.5 | 29.18 | yes |
| 44 | charge rank threshold 0.6 | 28.57 | no |
| 45 | discharge rank threshold 0.65 | 29.09 | no |
| 46 | discharge rank threshold 0.45 | 29.06 | no |
| 47 | profile over 3 days (+ discharge rank 0.45 carried over by a failed revert) | 29.19 | yes (marginal) |
| 48 | profile over 5 days | 29.86 | yes |
| 49 | profile over 7 days | 29.34 | no |
| 50 | discharge rank back to 0.55 (with 5-day profile) | 30.23 | yes |
| 51 | also sell in dearest expected slot ahead if above median | 28.30 | no |
| 52 | lookback 5 days (240) | 28.41 | no |
| 53 | lookback 10 days (480) | 27.31 | no |
| 54 | half-power discharge tier above 65th pct | 29.41 | no |
| 55 | half-power charge tier below 30th pct | 29.77 | no |
| 56 | margin vs expected peak ahead (max profile) | 29.71 | no |
| 57 | spread margin 25 | 27.93 | no |
| 58 | spread margin 17 | 30.05 | no |
| 59 | sit out weekends | 22.22 | no |
| 60 | smoothing weights 0.6/0.4 | 29.99 | no |
| 61 | forecast = smoothed latest + 0.5 x usual move (5-day) | 29.78 | no |
| 62 | hysteresis: continue run until median (stateful) | 30.21 | no |
| 63 | median instead of mean profile | 29.69 | no |
| 64 | horizon 7 h (14) | 30.18 | no |
| 65 | horizon 5 h (10) | 29.85 | no |
| 66 | discharge only if dearer slots ahead < soc/0.5+1 | 30.22 | no |
| 67 | same with +2 allowance | 30.06 | no |
| 68 | charge only if cheaper slots ahead < half-hours needed to fill + 1 | 30.32 | yes |
| 69 | charge slot allowance +2 | 30.30 | no |
| 70 | charge slot allowance +0 | 29.85 | no |
| 71 | horizon 8 h (16) with slot rule | 30.50 | yes |
| 72 | horizon 10 h (20) | 29.87 | no |
| 73 | SoC-aware discharge slot rule on 8h base | 30.45 | no |
| 74 | charge quantile 0.3 with slot rule | 29.87 | no |
| 75 | discharge when 0.9*latest - lo > 20 | 25.70 | no |
| 76 | discharge quantile 0.80 | 29.31 | no |
| 77 | also sell when latest >= max expected ahead | 29.47 | no |
| 78 | also charge when latest <= min expected ahead | 29.95 | no |
| 79 | lookback 6 days (288) | 30.07 | no |
| 80 | lookback 8 days (384) | 28.88 | no |
| 81 | profile over 4 days | 29.89 | no |
| 82 | profile over 6 days | 29.52 | no |
| 83 | recency-weighted 5-day profile | 30.11 | no |
| 84 | profile from same day-type (weekday/weekend) in past week | 29.64 | no |
| 85 | discharge rank 0.6 (on top of day-type profile, which commit 8f2dde6 had captured) | 29.80 | no |
| - | restore best policy from af18c94 after 8f2dde6 captured losing iter-84 variant | 30.50 | restored |
| 86 | discharge rank 0.6 | 30.36 | no |
| 87 | discharge rank 0.5 (identical to 0.55 at HORIZON 16) | 30.50 | no (no change) |
| 88 | discharge on max(smoothed, raw) price | 30.41 | no |
| 89 | charge on min(smoothed, raw) price | 30.12 | no |
| 90 | margin as hi - latest/0.9 > 20 | 30.63 | yes |
| 91 | margin 25 | 29.74 | no |
| 92 | margin 15 | 30.49 | no |
| 93 | sell threshold from last 3 days only | 28.31 | no |
| 94 | buy threshold from last 3 days only | 29.78 | no |
| 95 | horizon 9 h (18) | 30.00 | no |
| 96 | horizon 7 h (14) | 29.92 | no |
| 97 | discharge rank over 6 h ahead (charge still 8 h) | 30.82 | yes |
| 98 | discharge rank over 4 h ahead | 30.88 | yes |
| 99 | discharge rank over 3 h ahead | 30.41 | no |
| 100 | charge horizon 10 h (20) | 31.19 | yes |
| 101 | charge horizon 12 h (24) | 30.54 | no |
| 102 | charge horizon 11 h (22) | 30.79 | no |
| 103 | charge slot allowance +2 | 31.21 | yes (marginal) |
| 104 | charge slot allowance +3 | 30.95 | no |
| 105 | discharge only if dearer slots in next 4 h < soc/0.5 | 31.34 | yes |
| 106 | discharge allowance soc/0.5 + 1 | 31.21 | no |
| 107 | discharge allowance soc/0.5 - 1 | 23.97 | no |
| 108 | dearer-soon window 6 h | 31.26 | no |
| 109 | discharge quantile 0.70 | 30.61 | no |
| 110 | discharge quantile 0.78 | 30.77 | no |
| 111 | charge quantile 0.25 | 30.88 | no |
| 112 | charge quantile 0.17 | 30.07 | no |
| 113 | buy below 7-day median (slot rule + margin only) | 29.92 | no |
| 114 | 3-period smoothing on new base | 30.71 | no |
| 115 | sell ahead of expected negative prices (never fired) | 31.34 | no (no change) |
| 116 | margin vs min(hi, expected peak ahead) | 31.52 | yes |
| 117 | charge quantile 0.25 with capped margin | 31.46 | no |
| 118 | capped margin 15 | 31.73 | yes |
| 119 | capped margin 10 | 31.06 | no |
| 120 | capped margin 17 | 31.50 | no |
| 121 | cap at 4th-highest expected slot | 31.68 | no |
| 122 | margin vs expected peak alone (no hi cap) | 31.19 | no |
| 123 | profile over 7 days (new base) | 30.47 | no |
| 124 | profile over 3 days (new base) | 30.17 | no |
| 125 | also sell at expected local peak above median | 28.90 | no |
| 126 | remove negative-price rule | 31.64 | no |
| 127 | dearer_soon counted vs latest price (not profile) | 29.35 | no |
| 128 | cheaper_ahead counted vs latest price | 26.49 | no |
| 129 | also charge when expected spread > 50 | 31.72 | no |
| 130 | charge horizon 12 h (new base) | 31.19 | no |
| 131 | charge horizon 9 h (18) | 31.38 | no |
| 132 | profile days 1-5 plus 7 | 31.29 | no |
| 133 | sell threshold q70 (margin still q75) | 31.35 | no |
| 134 | sell threshold q80 (margin still q75) | 30.64 | no |
| 135 | margin cap at q85 | 31.35 | no |
| 136 | £5 tolerance on cheaper-ahead count | 29.52 | no |
| 137 | £5 tolerance on dearer-soon count | 30.87 | no |
| 138 | stricter charge count (+£5) | 29.54 | no |
| 139 | separate 2-day profile for selling | 31.07 | no |
| 140 | time-smoothed profile (±1 half-hour) | 31.34 | no |
| 141 | buy threshold = looser of week and last-day q20 | 31.84 | yes |
| 142 | sell threshold = looser of week and last-day q75 | 30.09 | no |
| 143 | day-local buy window 12 h instead of 24 h | 31.85 | yes (marginal) |
| 144 | charge quantile 0.25 | 31.92 | yes |
| 145 | charge quantile 0.30 | 31.66 | no |
| 146 | margin 20 (new base) | 32.10 | yes |
| 147 | margin 25 | 29.88 | no |
| 148 | charge quantile 0.30 (margin 20) | 31.83 | no |
| 149 | margin 18 | 32.03 | no |
| 150 | buy threshold from last 12 h only | 30.25 | no |
| 151 | local buy window 6 h | 31.91 | no |
| 152 | discharge look-ahead 5 h | 32.13 | yes (marginal) |
| 153 | discharge look-ahead 6 h | 32.03 | no |
| 154 | charge horizon 8 h (new base) | 31.51 | no |
| 155 | charge horizon 11 h (new base) | 31.75 | no |
| 156 | discharge slots soc/0.53 (efficiency-aware) | 32.13 | no (no change) |
| 157 | start trading after 5 days (shorter window while warming up) | 32.02 | no |
| 158 | charge slot count with 0.474 MWh/slot | 31.99 | no |
| 159 | sell threshold also >= last-12h q75 | 31.98 | no |
| 160 | discharge slot rule with <= | 32.03 | no |
| 161 | also sell when latest beats expected 5 h peak | 31.18 | no |
| 162 | discharge quantile 0.73 | 32.04 | no |
| 163 | discharge quantile 0.77 | 31.35 | no |
| 164 | also charge in the cheapest expected slot of the horizon | 32.28 | yes |
| 165 | charge in cheapest two expected slots | 32.05 | no |
| 166 | also sell at expected peak above q60 | 30.65 | no |
| 167 | margin cap shifted by today's deviation | 27.24 | no |
| 168 | charge quantile 0.20 (with cheapest-slot rule) | 32.31 | yes (marginal) |
| 169 | charge quantile 0.15 | 32.11 | no |
| 170 | charge only in cheapest expected slot (drop quantile) | 28.48 | no |
| 171 | profile over 4 days (new base) | 31.41 | no |
| 172 | profile over 6 days (new base) | 31.20 | no |
| 173 | sell only when both recent prices >= hi | 31.14 | no |
| 174 | cheapest-slot rule over next 4 h only | 32.06 | no |
| 175 | margin scaled with weekly spread | 31.74 | no |
| 176 | charge slot allowance +1 (new base) | 32.01 | no |
| 177 | profile with yesterday double-weighted | 31.73 | no |
| 178 | quantiles from 2-period smoothed series | 32.19 | no |
| 179 | margin 15 + 5*soc | 31.68 | no |
| 180 | margin 25 - 5*soc | 30.74 | no |
| 181 | readability refactor of charge rule (no logic change) | 32.31 | yes (refactor) |
| 182 | margin cap uses 24 h expected peak | 31.00 | no |
| 183 | margin cap uses 6 h expected peak | 32.13 | no |
| 184 | also charge on unexpected dip (latest < profile - 30) | 32.31 | no (no change) |
| 185 | same with £15 | 32.31 | no (no change) |
| 186 | half-power sell when borderline (dearer < soc/0.5+2) | 32.13 | no |
| 187 | half-power charge hedge (cheaper_ahead < room+4) | 32.01 | no |
| 188 | margin on raw latest price | 31.36 | no |
| 189 | margin on min(latest, expected now) | 28.62 | no |
| 190 | margin on max(latest, expected now) | 23.69 | no |
| 191 | local 12h buy quantile 0.3 | 32.14 | no |
| 192 | local 12h buy quantile 0.1 | 32.35 | no (+0.04 noise; adds a magic number) |
| 193 | lookback 14 days (new base) | 30.33 | no |
| 194 | lookback 5 days (new base) | 30.36 | no |
| 195 | smoothing 0.4/0.6 | 32.13 | no |
| 196 | SoC-dependent sell quantile (0.75 - 0.05*(soc-1)) | 32.13 | no |
| 197 | SoC-dependent sell quantile (0.75 + 0.05*(soc-1)) | 31.04 | no |
| 198 | charge allowance room*1.5 | 31.94 | no |
| 199 | cap expected sale price at q70 | 31.74 | no |
| 200 | MPC: 24 h DP over SoC on latest + 5-day profile | 23.29 | no |
| 201 | MPC with decaying level shift (0.8^k) | 27.48 | no |
| 202 | MPC + level shift + £5 action hurdle | 21.29 | no |
| 203 | dearer_soon vs max(expected now, latest) | 31.23 | no |
| 204 | cheaper_ahead vs min(expected now, latest) | 26.87 | no |
| 205 | discharge look-ahead 4.5 h (9) | 32.33 | yes (marginal) |
| 206 | also cheap if below every recent price at this slot | 32.33 | no (no change) |
| 207 | also sell if above every recent price at this slot | 32.31 | no |
| 208 | charge horizon 10.5 h (21) | 32.27 | no |
| 209 | margin with per-leg efficiency (0.95 each way) | 32.42 | yes |
| 210 | drop 12 h local buy threshold (cheapest-slot rule covers it) | 32.42 | yes (simplification, same score) |
| 211 | charge quantile 0.25 (simplified base) | 32.34 | no |
| 212 | charge quantile 0.15 (simplified base) | 31.83 | no |
| 213 | remove negative-price rule (simplified base) | 32.38 | no (kept: matters more in summer) |
| 214 | sell only if spread over buy threshold pays | 28.89 | no |
| 215 | trimmed-mean profile | 31.08 | no |
| 216 | margin 21 | 32.10 | no |
| 217 | margin 19 | 32.24 | no |
| 218 | discharge quantile 0.74 | 32.11 | no |
| 219 | discharge quantile 0.76 | 32.25 | no |
| 220 | median gate on cheapest-slot rule | 32.42 | no (no change) |
| 221 | latest = median of last 3 | 31.36 | no |
| 222 | skip charging when soc >= 1.95 | 32.41 | no |
| 223 | discharge slot count rounded up ((soc+0.25)/0.5) | 32.18 | no |
| 224 | charge room rounded up ((2.25-soc)/0.5) | 32.37 | no |
| 225 | full battery sells if refill cheaper within 3 h pays | 32.23 | no |
| 226 | dearer count excludes current slot | 32.42 | no (no change) |
| 227 | count cheaper slots only before expected peak | 29.45 | no |
| 228 | sell only if worth more than refilling at expected min | 29.01 | no |
| 229 | cap at second-highest expected price | 32.31 | no |
