# UI design spec: autoresearch pipeline for grid-battery dispatch

Written 2026-10-22. Style target captured from tesla.com/en_gb/support/energy/tesla-software/autobidder via Firecrawl (`scrape --format markdown,rawHtml,screenshot` and `--format branding`), plus pixel measurement of the 1920×1080 screenshot. Values marked **(captured)** come from that; **(assumed)** are inferred. We copy the look only: no Tesla name, wordmark, logo or claims anywhere in the product.

## 1. Audience and job to be done

Battery owners and route-to-market optimisers (Habitat, Arenko, Kraken Flex, EDF PowerShift and their customers such as Low Carbon and Gresham House). They already run several optimisers side by side and audit them independently; the industry metric is Percentage of Perfect (PoP), observed at 60–80%, but no vendor publishes a reproducible number and each picks its own benchmark or best backtest (products.md, workflow.md §4). The job: look at one page and decide whether the proposed dispatch rule is better than the incumbent, on evidence the search never saw, and see exactly what changed in the rule before approving the PR.

## 2. Competitive takeaways for the UI

| Competitor behaviour | What it hides | UI decision for us |
|---|---|---|
| Gridmatic: "51% of theoretical, backtest ~75%", criticised as a black box; baselines undisclosed | The denominator and the baseline | **D1.** Every score shows its oracle denominator next to it (`£/MW/day` and `% of perfect`, with the oracle £ visible). Baselines are always in the same table. |
| Modo: optimisers "pick their own benchmark or best backtest"; Modo applies a 15–25% haircut to perfect foresight | Which window the number came from | **D2.** Train, val and test are always shown side by side, with their date ranges, in that order. A test number is never shown alone. |
| Fluence: experts review results daily; "models never finished"; no backtest shown | How a change was decided | **D3.** The strategy-evolution panel shows every iteration, including rejected ones and the one honest reversal (iter 85 → restore). Kept/rejected is a visible column, not a filter default. |
| Habitat, Tesla: trading desk sets parameters; rule is private | The rule itself | **D4.** Render the evolved rule as source and as a diff against the seed. The rule is ~30 lines of plain Python; an operator can read it. |
| All vendors: single aggregate uplift claim | Variance | **D5.** Every headline £ carries its 95% CI (`ci95` from evaluate.py). Confidence intervals that overlap are not described as a win. |
| All vendors: stack ancillary, BM, intraday | Scope | **D6.** A failure-modes panel is a first-class section, not a footnote, listing single-market, zero market impact, regime shift, flat degradation, backtest overfitting. |

## 3. Page structure

Single column, Tesla-support style: white page, one 660px content column, generous vertical rhythm, one wide image per section at most. Order below is the scroll order. All data comes from files `gate.py` writes; nothing is computed in the browser except chart drawing.

Data that exists today: `loop_log.md` (86 rows), `policy.py`, `seed_policy.py`, `evaluate.py` JSON (`score, ci95, pct_of_oracle, revenue, oracle, cycles, days, error`), `battery.SPLITS` (train 2025-10-02→2026-05-31, val 2026-06-01→07-31, test 2026-08-01→10-14), `plot.py`. `results/` and `champion/` do not exist yet; `gate.py` creates `results/results.md`, `results/results.json` (per policy per split, the evaluate.py dict) and `champion/policy.py`. One addition is needed for the chart: `plot.py` (or gate.py) should also write `results/test_week.json` with `{hours, prices, seed:{soc,act}, champion:{soc,act}}`; it already computes these lists.

### 3.1 Hero
Purpose: the one-line pitch and the single most important number.
Source: README.md "One line"; `results/results.json` → `champion.test.pct_of_oracle`, `champion.test.score`, `champion.test.ci95`.
Content: H1 "Autoresearch for battery dispatch"; one sentence: "Continuously improves the dispatch rule of a grid battery on real GB prices, and promotes a new rule only when it also wins on months the search never saw." Below it the hero image: the held-out-week chart (section 3.4) rendered large, grey gradient backdrop like the reference, radius 8px. Then the pitch paragraph and an outlined button "View the champion PR" (link to the PR or `champion/policy.py`).

```
┌──────────────────────────────────────────────────────┐
│  [mark]            Pipeline  Evaluator  Results       │  nav 14px
│                                                      │
│        Autoresearch for battery dispatch             │  H1 40px
│                                                      │
│        ┌──────────────────────────────────┐          │
│        │  held-out week chart, 660×330    │          │  hero image
│        │  grey gradient bg, radius 8      │          │
│        └──────────────────────────────────┘          │
│        One-paragraph pitch, 14px grey.               │
│        ┌─────────────────┐                           │
│        │  View champion  │  outlined button          │
│        └─────────────────┘                           │
└──────────────────────────────────────────────────────┘
```

### 3.2 Headline metrics
Purpose: champion score on all three windows, side by side (D1, D2, D5).
Source: `results/results.json` → `champion.{train,val,test}.{score,ci95,pct_of_oracle,oracle,days,cycles}`; split dates from `battery.SPLITS`.
Content: three equal tiles. Each: window name and date range; `score` £/MW/day large; `ci95` small under it; `pct_of_oracle` with the oracle £/MW/day in grey ("of £X perfect"); cycles. Test tile has a thin top rule labelled "held out, read once". Below the tiles, one line: "Loop saw train only. Val decides promotion. Test is reported, never optimised."

```
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ TRAIN         │ │ VAL           │ │ TEST  held out│
│ Oct 25–May 26 │ │ Jun–Jul 26    │ │ Aug–Oct 26    │
│ £30.5 /MW/day │ │ £xx.x         │ │ £xx.x         │
│ CI 28.1–32.9  │ │ CI            │ │ CI            │
│ 61% of £49.9  │ │ xx% of £yy    │ │ xx% of £zz    │
│ 0.8 cycles/d  │ │               │ │               │
└───────────────┘ └───────────────┘ └───────────────┘
```
Phone: tiles stack vertically in the same order.

### 3.3 Strategy evolution
Purpose: show the search as it happened (D3).
Source: `loop_log.md` columns `iter, idea, score, kept?` (parsed at build time; the `-`/"restored" row included). Optionally git log subjects `loop: <idea> score=<n>` for commit hashes.
Content: a step chart of best-so-far train score vs iteration (kept iterations as dots, rejected as faint ticks), then the table beneath it. Default view: all 86 rows, kept rows in black, rejected in grey, the "restored" row flagged with a note. Table columns: iter, idea, train £/MW/day, kept. Caption: "Scores are train only. None of these numbers touched val or test."

```
  £30 ┤                              ●──●─●──●
  £25 ┤            ●───●──●──●─●──●
  £20 ┤    ●──●──●
  £15 ┼●
      └─────┬─────┬─────┬─────┬─────┬─────┬──
            10    20    30    40    50    60   86
  | iter | idea                         | train | kept |
  |  0   | seed rolling-percentile      | 15.39 | seed |
  |  3   | 7-day lookback               | 20.18 | yes  |
  |  …   |                              |       |      |
  |  85  | discharge rank 0.6 (…)       | 29.80 | no   |
  |  –   | restore best from af18c94    | 30.50 | restored |
```

### 3.4 Held-out week
Purpose: show the rule acting on data it never saw (D2).
Source: `results/test_week.json` (new, from plot.py): `prices` (£/MWh, 336 half-hours), `champion.soc`, `champion.act`, `seed.soc`, `seed.act`; week = second week of test.
Content: two stacked panels, shared x-axis in hours. Top: price line; champion charge marks (below the line) and discharge marks (above). Bottom: SoC in MWh for champion and seed. Title "Second week of the test window (Aug 2026)". Caption states the policy had the first test week as history only.

```
 £/MWh ┤      ╱╲        ╱╲▲▲          ╱╲
       ┤  ▼▼╱  ╲▲▲  ▼▼╱    ╲   ▼▼▼ ╱   ╲▲
       ┤▼╱       ╲╱         ╲╱      ╱
 SoC   ┤ ▔▔╲__╱▔▔╲___╱▔▔▔╲__╱▔▔╲_  champion (dark)
 MWh   ┤  ··╲_╱··╲__╱···╲_╱··╲_   seed (grey)
       └──────┬──────┬──────┬──────┬──────┬──
             Mon    Tue    Wed    Thu    Fri
```

### 3.5 The rule
Purpose: the artefact being approved (D4).
Source: `champion/policy.py` between `# EVOLVE-BLOCK-START/END`; `seed_policy.py` for the diff.
Content: toggle "Rule | Diff vs seed". Rule view: the block as a code listing, monospace 13px. Diff view: unified diff, additions on pale green, removals pale red, no other colour. Under it a short plain-English reading of the rule generated by hand once (three bullets: 7-day percentile thresholds; 8-hour time-of-day rank filter; charge only if the spread covers losses and there are few cheaper slots ahead).

### 3.6 Baselines
Purpose: context for the headline (D1).
Source: `results/results.md` (already a markdown table) or `results/results.json` keys `do_nothing, fixed_schedule, seed, champion` plus the oracle row.
Content: the gate.py table as-is: policy, train, val, test £/MW/day, test CI, test % of oracle, test cycles; perfect foresight as the last row at 100%. Champion row in black, others grey. Add one column "gain vs seed on test".

### 3.7 Where it can mislead
Purpose: honesty panel (D6).
Source: README.md "Where it can still mislead" (six bullets) and "Leakage and overfitting guards" table.
Content: two lists side by side at desktop, stacked on phone. Left "Guards" (no lookahead, no test peeking, no dates, only `math`, crash → 0, clipping, cycle count). Right "Limits" (regime shift, single market, zero market impact, one year of data, flat degradation, search overfits backtests). If val gain did not hold on test, the first bullet of Limits says so with the numbers.

### 3.8 Adoption
Purpose: how it runs in production.
Source: README.md "Deployment".
Content: four-step strip: fetch → search on rolling window → gate on newest month → PR. One sentence on shadow-running, one on swapping `battery.py` / `fetch_prices.py` / driver. Outlined button "Reproduce" linking to the README commands.

## 4. Visual system

Reference page is light-only; a dark variant is included because artifacts and operator screens need it.

**Type (captured).** Headings: Universal Sans Display; body: Universal Sans Text; both proprietary, so ship the stack `"Universal Sans Display", -apple-system, "Helvetica Neue", Arial, sans-serif` and the page renders in the system sans. Do not load a Google Font substitute by default; Inter is the nearest free match if the user wants one (assumed).

| Token | Value | Status |
|---|---|---|
| H1 | 40px / 1.2, weight 600, colour text-strong | captured (cap height 29px) |
| H2 | 28px / 1.2, weight 600 | captured |
| Body | 14px / 20px, weight 400, colour text | captured (branding reported 20px; measured 14px body with 20px line height) |
| Nav / button label | 14px, weight 500 | captured |
| Small / captions | 12px / 16px | assumed, matches `--tds-btn--font-size: 12px` |
| Metric number | 40px, weight 600, tabular numerals | assumed |
| Code | 13px monospace, `ui-monospace, SFMono-Regular, Menlo` | assumed |

**Colour (captured unless noted).**

| Token | Light | Dark |
|---|---|---|
| bg | #ffffff | #111111 (TDS `--tds-color-ct-bg`) |
| bg-alt (image backdrop, tiles) | #f4f4f4 (assumed) | #222222 (`spacerace-surface-alt`) |
| text-strong | #171a20 | #e8e8e8 (assumed) |
| text | #393c41 | #a2a3a5 (TDS ct-h2) |
| text-muted | #5c5e62 (input text) | #8e8e8e (TDS ct-body) |
| rule / separator | #d0d1d2 | #393c41 (TDS ct-separator) |
| hero gradient | #77808a → #bbc8d3, top-left to bottom | #222 → #111 |
| link | #008ee6 (branding) | #4da3e8 (assumed) |
| charge (buy) | #2a6a4a (assumed) | #58b58a |
| discharge (sell) | #b03a2e (assumed) | #e06c5c |
| oracle line | text-strong, dashed | same |
| diff add / remove | #e6f4ea / #fbe9e7 (assumed) | #15301f / #3a1a17 |

No other accent. Tesla's blue is used only for links.

**Spacing (captured from screenshot).** 4px base unit. Content column 660px, centred; page gutter 16px at phone width. Hero image 660×330 (2:1), radius 8px. Section gap 72px between H2 blocks (measured 100px from button bottom to next H2 top, ≈ 96px with margins); paragraph gap 16px; H1 to hero 44px; hero to body text 64px. Nav height 56px, logo mark left, four to five text links centred.

**Components.** Buttons: outlined, 2px border text-strong, radius 4px, 204×40px, label 14px weight 500, hover opacity .85; a filled variant uses #5c5e62 on white (captured secondary/primary). Tiles and tables: no cards or shadows; 1px rule separators only (TDS `--tds-border-radius--card: 0`). Tables: 14px, right-aligned numbers, header 12px uppercase muted.

**Phone.** Column 100% minus 32px gutters; metric tiles and the guards/limits lists stack; charts keep aspect ratio 2:1 and the week chart becomes horizontally scrollable at 3 days visible; the evolution table hides the "idea" column behind a tap at <400px (assumed).

## 5. Charts

| Section | Chart | Honesty rule |
|---|---|---|
| Headline metrics | Stat tiles, no chart | Oracle £ printed beside every %; CI printed under every £. |
| Strategy evolution | Step line of best-so-far train score; dots for kept, ticks for rejected | Y axis starts at the do-nothing score (0), not at the seed; oracle train £/MW/day drawn as a dashed line at the top so the gap to perfect stays visible; axis label says "train only". |
| Held-out week | Two stacked line panels, shared x; action markers on price | Whole chart is labelled as test; no train data on the same axes; seed shown in grey as the comparator; SoC axis fixed 0–2 MWh. |
| Baselines | Horizontal bars, one per policy per split, three small multiples (train, val, test) | Oracle bar at 100% in every multiple; bars share one £ scale per multiple. |

All charts: inline SVG drawn by ~100 lines of plain JS from the JSON above; no animation; colours from the tokens; axis text 12px muted; dark mode via `currentColor` and the tokens.

## 6. Implementation recommendation

**Static HTML page, `results/index.html`, written by `gate.py` at the end of a run with the JSON inlined (default).** Reason: the data already exists as files the pipeline writes, so a template substitution in gate.py is the smallest step, adds no runtime dependency, and the page is committed with each PR so the reviewer sees the exact report for that policy. The same file publishes unchanged as a claude.ai artifact (no CDN scripts needed because charts are inline SVG), which covers the demo case.

Mechanics: gate.py reads `results/results.json`, `results/test_week.json`, `loop_log.md`, `champion/policy.py`, `seed_policy.py`, embeds them in a `<script type="application/json">` block of a template kept in `results/template.html`, and writes `results/index.html`. Everything in sections 3.x reads from that block. Open the file directly; no server.

## 7. Open decisions for the user

1. **Light only, or light + dark?** The reference page is light-only; dark costs a second token set that is already drafted above. Default: ship both via `prefers-color-scheme`.
2. **Full loop log or kept-only?** 86 rows is long; it is also the honest view (D3). Default: all rows, rejected rows greyed, with a "kept only" toggle.
3. **Is the page a per-run report committed in `results/` (part of the PR), or a hosted page that always shows the current champion?** This changes where the file lives and whether a URL is needed. Default: per-run report in the PR; hosting is a copy of the same file.

Everything else above is a default.
