# Slowpoke

An autoresearch loop that teaches an electric car to make money from the grid.

One Python function decides, every half hour, whether the car's battery buys from the grid, sells to it, or sits still. A sealed simulator runs it through a year of half-hourly prices with real constraints and returns the annual profit. An AI agent proposes one change at a time, keeps what makes money, reverts what doesn't, and logs everything. Nobody writes the trading rule.

```
problem/policy.py      ──►   evaluator/score.py    ──►   database/
(the ONE file the agent      (sealed: one-year V2G        (archive of every candidate,
 may edit)                    simulation, returns          results.tsv, parent selection)
         ▲                    -profit in £)                        │
         └──────────────────── loop/run.py ◄───────────────────────┘
                 propose one change · score · commit or revert · log
```

Karpathy-style loop (one editable file, locked evaluator, commit or revert). AlphaEvolve shape (program, evaluator, program database). ADRS argument: a cheap deterministic evaluator (0.15 s for a year) is why the loop works.

## The problem

Vehicle-to-grid. A 60 kWh EV, 7 kW charger both ways, plugged in at home. Prices are known 48 half-hours ahead and are UK-shaped: cheap overnight, sometimes negative on windy nights, big evening peak, winter premium, occasional scarcity spikes.

Constraints the simulator enforces and the agent cannot change:
- 90% round-trip efficiency, 3p/kWh battery wear, export pays 85% of import
- Weekdays the car leaves 08:00, returns 18:00, uses 12 kWh; not callable while away
- Weekdays it must be at 80% by 07:00 or a £40 penalty applies
- Weekends it's home all day

## The guard against cheating

- The agent can only write `problem/policy.py`.
- `evaluator/score.py` is never shown to it. Any crash, NaN, or slow call returns a hard penalty. "Always sell" scores -£10,439.
- Every experiment is archived and logged, kept or reverted. Kept experiments are git commits, so `git log` is the lab notebook.

## Run it

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...
python data/make_prices.py              # a year of synthetic half-hourly prices
python evaluator/score.py --verbose     # baseline breakdown
python loop/run.py --iterations 40      # the research loop
python -m http.server 8000              # dashboard at localhost:8000/dashboard/
```

## Results

| | annual result | kept? |
|---|---|---|
| baseline: dumb overnight charging | -£371 | |
| buy only in the cheapest slots before 07:00 | -£186 | yes |
| always sell (cheat attempt) | -£10,439 | no |
| add evening discharge above the 90th percentile | -£120 | yes |
| *loop run* | *fill in* | |

## Applied use

Octopus Energy, OVO, any V2G tariff provider, or a fleet operator with a thousand vans on driveways overnight. Point the loop at real tariff data, let it run, ship the policy. The same loop with a different `score.py` is a home battery, a heat pump schedule, or a grid-scale storage asset.

`tracks/` holds the earlier covariance-estimator version of the same architecture.
