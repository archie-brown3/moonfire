# Moonfire: autoresearch for battery dispatch

Entry for the Moonfire Ventures Hack (Cambridge Compute Co. · AIDDA). Brief: [context/moonfire-ventures-hack.md](context/moonfire-ventures-hack.md).

**One line:** an autoresearch pipeline that continuously improves the dispatch rule of a grid battery on real GB electricity prices, and promotes a new rule only when it also wins on months the search never saw.

## The use case

Grid batteries earn money by buying power when it is cheap and selling it when it is dear. Every half hour the dispatch rule decides: charge, discharge, or wait, knowing only past prices. The quality of that rule is the whole business.

We are the **optimiser firm** in this scenario: the company that runs dispatch for battery owners under a revenue share, the way Tesla Autobidder, Octopus Kraken Flex, Habitat Energy and Flexitricity do in GB. An optimiser's margin is the gap between what its rule captures and what a rival's would. GB has several GW of batteries, each MW earning tens of thousands of pounds a year; a few percentage points more captured value across a fleet is direct margin, and it is also the number optimisers compete on when pitching asset owners.

Today that rule is improved by analysts: tweak, backtest, compare, repeat. This pipeline runs that loop continuously, with the held-out discipline an analyst is supposed to keep and often skips under time pressure.

## The pipeline

```
fetch_prices.py ──> data/prices.csv ──> split by time (train / val / test)
                                               │
        search loop (pluggable) edits policy.py │
                 │  calls                       ▼
                 └──────────> evaluate.py ──> JSON {score, ci95, pct_of_oracle, cycles, error}
                                               │
                           gate.py: beats champion on val?  ──yes──> champion/policy.py + results/
```

| File | Role |
|---|---|
| `fetch_prices.py` | Half-hourly APX market index prices from Elexon's open BMRS API. No key. Drops partial edge days, interpolates untraded periods. |
| `battery.py` | Asset spec (1 MW / 2 MWh, 90% round trip, £10/MWh degradation), simulator, time splits, exact perfect-foresight oracle. **The loop cannot edit this.** |
| `policy.py` | `decide(past_prices, soc, period, weekday) -> MW`. **The only file the loop edits.** |
| `evaluate.py` | Scores a policy file on a split in a guarded subprocess. The single command every loop driver calls. 0.2 s per run. |
| `baselines.py` | Do-nothing, fixed time-of-day schedule, seed rule, oracle, on every split. |
| `gate.py` | Champion/challenger promotion on val; scores test once; writes `results/`. |
| `program.md` | Instructions for the search agent. |
| `seed_policy.py` | Frozen copy of the starting rule, for the report. |

Zero dependencies beyond Python 3.12. `uv sync && uv run python baselines.py` reproduces the table below.

### The search loop is a black box

The loop only needs to do two things: edit `policy.py`, and run `uv run python evaluate.py policy.py --split train`. In this run it is a Claude Code agent following `program.md` (Karpathy-style: propose, score, keep if better, commit). OpenEvolve, LoongFlow or any other framework drops in by writing a driver that calls the same command. Everything judges should care about (task contract, evaluator, split, gate) is independent of that choice.

## The evaluator

**Headline:** net revenue in £/MW/day over the window, with a 95% bootstrap confidence interval over days.
**Secondary:** % of the perfect-foresight optimum.

- **The ceiling is exact.** With 1 MW and half-hour steps, stored energy moves in 0.5 MWh units, so a five-state dynamic programme over the window gives the best any policy could do knowing every future price. It runs in a millisecond.
- **Why £/MW/day leads.** "% of perfect foresight" scales with volatility, not skill: a calm month has a tiny denominator and bad trades can push it negative. The later windows here were two to three times more volatile than train, so both numbers are shown.
- **Costs are inside the simulator**, not the policy: efficiency losses, degradation per MWh moved, power and charge limits. The policy returns a request; the simulator clips it and does the accounting. It cannot misreport.

### Leakage and overfitting guards (each verified with a deliberately bad policy)

| Guard | Mechanism |
|---|---|
| No lookahead | Policy is called step by step with `prices[:t]`. The current period's price is a settlement price, known only after the fact. |
| No test peeking | Split by time. The loop runs only `--split train`. `gate.py` reads val for promotion and test exactly once. |
| No hard-coded calendars | Literal dates rejected by regex before the policy is loaded. |
| No smuggled data | AST check: only `math` may be imported. |
| Crash, NaN, hang | Score 0, error text returned to the loop. 30 s subprocess timeout. |
| Over-rating | Simulator clips to 1 MW and SoC limits. |
| Thrashing | Cycle count reported; degradation cost already penalises it. |

### Where it can still mislead

- **Regime shift.** Train is Oct 2025–May 2026; test is Aug–Oct 2026. Gas, wind and interconnector conditions differ. A train gain that fails on test is reported, not hidden.
- **Single market.** The model trades the realised market index only. Real operators also run day-ahead, frequency response and the Balancing Mechanism, and use forecast feeds. Absolute £ here is a floor, not a forecast.
- **Market impact** is assumed zero at 1 MW.
- **One year of data** is one price regime.

## Results

_Filled in by `gate.py` at the end of the run; see `results/results.md`._

RESULTS_TABLE

## Deployment

A weekly scheduled job runs the whole cycle: refetch prices, re-run the search on a rolling window, gate on the newest month, and open a pull request containing the new `policy.py` and its report. The quant team reviews the diff (the rule is a few dozen lines of plain Python with no dependencies, which is how dispatch rules are written anyway), shadow-runs the challenger beside live dispatch, then switches.

- **Different asset:** change the spec in `battery.py`.
- **Different market** (ERCOT, NEM, Germany): change `fetch_prices.py`.
- **Different search framework:** write a driver that calls `evaluate.py`.
- **Cost:** evaluation is 0.2 s; the LLM is the only expense, and it is bounded by iteration count.

## Reproduce

```
uv sync
uv run python fetch_prices.py 2025-10-01 2026-10-15
uv run python baselines.py
# run your search loop of choice against policy.py, then
uv run python gate.py policy.py
```
