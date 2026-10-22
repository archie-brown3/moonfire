# Pitch: autoresearch for battery dispatch

Three minutes, one speaker, one screen. Numbers in brackets get filled from `results/results.md` after `gate.py` runs.

---

## The script

**The problem (25 s)**

Britain has 8.5 gigawatts of grid batteries and needs three times that by 2030. They make money one way: buy power when it's cheap, sell it when it's dear. Every half hour, a rule decides charge, discharge or wait. Last month the average battery earned £99,000 per megawatt. The best one earned 42% more than that, and Modo Energy says the difference isn't cycling harder, it's trading smarter. Across the fleet, one percentage point of capture is worth about five and a half million pounds a year.

Today that rule is improved by humans. Habitat, Tesla, EDF: a quant has an idea, edits the rule, runs a backtest, keeps it or not. Every job ad in this industry describes that loop. Nobody has automated it.

**What we built (35 s)**

We are the optimiser firm, and this is the engine. One Python file is the dispatch rule. A sealed simulator replays it against a year of real half-hourly prices from Elexon, with efficiency losses, degradation and power limits inside the simulator so the rule can't misreport. An AI agent proposes one change, scores it, keeps it if it wins, reverts if not, and commits. It ran 249 experiments in two hours at a fifth of a second each.

The part that matters: the rule only ever sees the past. The current price is a settlement price, known after the fact. No lookahead, no literal dates, no imports except `math`, every one of those enforced by code and tested with a deliberately cheating policy.

And a new rule is promoted only if it also wins on two months the search never saw. Then it's scored once, on three further months, and we publish that number whether we like it or not.

**The result (30 s)**

Show the results table.

The seed rule earned £15 per megawatt per day on the training months. The loop took it to £32. On the held-out test window it went from £55 to £71, at 46% of perfect foresight. The industry calls that Percentage of Perfect. Optimisers quote 60 to 80, but every vendor picks its own benchmark. Ours is a five-line dynamic programme anyone can run.

Show the test week plot. This is a week it never trained on. Green is where it charged, red where it sold. It bought the overnight trough and sold the evening peak without being told either exists.

**Deployment (20 s)**

This runs as a weekly job. Refetch prices, re-run the search on a rolling window, gate on the newest month, open a pull request with the new rule and its report. The quant reviews a diff of forty lines of plain Python, shadow-runs it, switches. Different battery: change one spec file. Different market, ERCOT or Germany: change the fetcher. Different search framework, OpenEvolve, LoongFlow: call the same evaluate command. We built the contract, not the framework, because the contract is what makes it safe to deploy.

**Close (10 s)**

Every optimiser in this market sells "we trade smarter". None of them can show you a reproducible number. We can, and the loop that produced it is in the repo.

---

## Numbers to have in your head

| What | Number | Source |
|---|---|---|
| GB battery fleet | 8.5 GW / 14.4 GWh, Q3 2026 | Modo |
| 2030 need | 23 to 27 GW | NESO |
| Index revenue, Sep 2026 | £99k/MW/yr, wholesale £68k of it (record) | Modo |
| Best asset vs index | +42% | Modo, Sep 2026 |
| Value of 1 pt of capture | ~£5.5m/yr fleet-wide | README estimate |
| Industry PoP | 60 to 80%, no reproducible figure published | Modo |
| Our asset | 1 MW / 2 MWh, 90% round trip, £10/MWh degradation | battery.py |
| Data | Elexon APX, 2 Oct 2025 to 15 Oct 2026, 18,192 half-hours | fetch_prices.py |
| Splits | train 242 d, val 61 d, test 75 d, by time | battery.py |
| Evaluator speed | 0.2 s | evaluate.py |
| Experiments | 249 | loop_log.md |
| Seed vs loop, train | £15.4 vs £32 /MW/day | baselines |
| Seed vs loop, test | £55.1 vs £71 /MW/day, 46% of oracle | gate.py |

---

## Questions the judges will ask

**Isn't a one-number loop just going to overfit the backtest?**
Yes, that's the documented failure of LLM-evolved trading strategies, and it's why the loop never touches val or test. Promotion needs a val win; test is read once. The table shows the train/test gap rather than hiding it. Our next step is a paired daily test against the champion so a change has to beat noise, not just the mean.

**Why is it only 45% of perfect foresight when the industry says 75?**
Three reasons, all in the README. Our rule sees no forecast and not even the current price; the industry has day-ahead feeds. We trade one market; they stack frequency response and the Balancing Mechanism. And PoP scales with volatility, which is why we lead with £/MW/day. The point isn't the absolute number, it's that ours is reproducible and theirs isn't.

**Why not use OpenEvolve or LoongFlow?**
You can. The loop is a black box that edits one file and calls one command. We spent the three hours on the evaluator, the split and the gate, because that's what the brief asked for and that's what a deployment needs. Swapping the search framework is a driver, not a redesign.

**The loop plateaued. Why?**
The score's daily variance is wide, so late improvements are inside the noise, and the agent stayed in one family of rules. Both are fixable: paired acceptance, and forcing a structurally different proposal every few iterations. We'd rather show an honest plateau than a tuned curve.

**Who pays?**
Battery owners already pay optimisers a revenue share, a toll or a floor; Low Carbon split 95 MW across three of them and audits each. An optimiser whose rule improves every week, with a published out-of-sample score, wins that audit.

**Is this safe to run on a real asset?**
The output is a pull request, not a live change. A human reviews forty lines of Python, shadow-runs it, then switches. Degradation, warranty throughput and power limits live in the simulator, so the search can't propose something the asset can't do.

---

## On screen, in order

1. README results table (after gate.py)
2. `results/test_week.png`
3. `git log --oneline | head -20`: every commit is a kept experiment with its score
4. `policy.py`: the whole rule fits on one screen

## Who does what

Speaker: one person, no keyboard. Driver: has the four screens above in tabs, switches on cue. Third: watches the clock, holds up a hand at 2:30.
