# Project brief: battery-dispatch autoresearch

*Status as of 18:55 BST, 22 Oct 2026. Deadline 19:30. Companion to the hack brief in `moonfire-ventures-hack.md` and the working rules in `../README.md` and `../program.md`.*

## What we are building

An autoresearch pipeline that continuously improves the dispatch rule of a grid battery on real GB half-hourly electricity prices. An LLM search loop rewrites one Python rule; an evaluator replays it against a year of prices; a gate promotes a new rule only if it also wins on months the loop never saw.

**Scenario:** we are the optimiser firm, building an Autobidder-style dispatch platform (peers: Tesla Autobidder, Octopus Kraken Flex, Habitat Energy, Flexitricity). Our margin is the gap between what our rule captures and what a rival's would. The autoresearch loop is the engine that keeps that rule improving.

**Not in scope:** building an evolutionary framework. The loop is a pluggable black box; our work is the task contract, evaluator, data split, promotion gate and adoption story.

## Decisions made, in order

| Time | Decision | Why |
|---|---|---|
| 17:55 | Framework-agnostic: evaluate.py is the one command any loop calls | Brief rewards evaluator and deployment design, not the loop itself |
| 18:00 | Problem: grid battery trading, over cache eviction, M5 inventory, LLM scheduling, fab dispatch | Open data with no auth; exact optimum ceiling; crisp no-lookahead story; commercial pitch judges already believe |
| 18:12 | Three-agent debate (two advocates, one neutral auditor) confirmed battery over M5 | M5's ceiling depends on an invented cost model; battery's is a textbook DP |
| 18:12 | Headline metric: £/MW/day with bootstrap CI; % of perfect foresight secondary | % scales with volatility, not skill, and can go negative |
| 18:20 | Data: Elexon BMRS market index, APX provider only, 2 Oct 2025 to 14 Oct 2026 | Verified free and fast; 7-day paging; DST days kept; 12 untraded periods interpolated |
| 18:25 | Oracle is an exact 5-state dynamic programme, no scipy | 1 MW, 0.5 h steps, 2 MWh means SoC moves on a 0.5 MWh grid; zero dependencies |
| 18:25 | Splits by time: train Oct–May (242 d), val Jun–Jul (61 d), test Aug–Oct (75 d) | Walk-forward mirrors deployment; loop sees train only; test read once |
| 18:29 | Guards: lagged prices only, math-only imports, no literal dates, crash/NaN/timeout score 0, simulator clips power | Each verified with a deliberately bad policy |
| 18:43 | Search loop = a Claude Code agent in a Herdr tab following program.md | No API key or install; shows the loop is swappable; time |
| 18:43 | Research agents run as Claude Opus 5.5 (high effort) in their own Herdr tabs, not in-process subagents | User preference; auto-approve flags for agy were blocked by the permission classifier |
| 18:45 | No separate spec or plan documents; AGENTS.md is the spec | Deadline |

## Current state

Done and committed: data fetcher, simulator, oracle, evaluator, baselines, gate, program.md, frozen seed policy, README draft (results placeholder).

Baselines (£/MW/day, % of oracle): seed 15.4 / 24% train, 46.9 / 41% val, 55.1 / 36% test. Fixed schedule 11.1 / 17% train. Oracle 64.9, 115.2, 152.5.

Search loop finished. `research-products`, `research-market`, `research-workflow` tabs writing reports to the scratchpad.

Done by 19:35: loop stopped at 249 experiments (39 kept, plateau at £32.42 train). gate.py promoted the champion on val (£61.62 vs £46.90) and scored test once: £70.64/MW/day vs seed £55.11, 46.3% of perfect foresight. Results, charts, dashboard data, pitch and deck filled from those outputs.

## Agent orientation

If you are an agent joining this repo:

- Read `../README.md` for the pipeline and evaluator rules and `../program.md` for the loop's rules, then this file for why.
- The only file the search loop may edit is `policy.py`; `program.md` is its instruction set.
- `battery.py` is the authority on physics and money. Do not move constraints into the policy.
- Never run `evaluate.py --split val` or `--split test` from a search loop. `gate.py` is the only reader of those splits.
- Reproduce everything with `uv sync && uv run python baselines.py`. No other dependencies exist, and none should be added without a reason that survives the README's "zero dependencies" claim.
- Report numbers honestly: a val gain that fails on test goes in the table as is.
