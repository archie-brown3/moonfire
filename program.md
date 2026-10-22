# program.md — instructions for the search agent

You are the research loop. Your job: make `policy.py` earn more money on the TRAIN split.

## Loop (repeat until told to stop)

1. Read `policy.py`. Only the code between `# EVOLVE-BLOCK-START` and `# EVOLVE-BLOCK-END` may change.
2. Propose ONE idea and edit the file. Ideas that tend to work: time-of-day priors (evening peak, overnight trough),
   price momentum, longer/shorter lookbacks, separate thresholds for charging vs discharging, SoC-aware hysteresis,
   weekday/weekend differences, reacting to negative prices, exploiting the 2-hour duration (don't dump all at once).
3. Run: `uv run python evaluate.py policy.py --split train`
4. Read `score` (£/MW/day). If it beats the best so far, `git commit -am "loop: <idea> score=<score>"`.
   Otherwise `git checkout policy.py` and try a different idea.
5. Append one line to `loop_log.md`: `| iter | idea | score | kept? |`.

## Rules

- Never run `evaluate.py` with `--split val` or `--split test`. Never read `data/prices.csv` directly. Never edit any file except `policy.py` and `loop_log.md`.
- `policy.py` may import only `math`. No literal dates. `decide()` must return a finite float in [-1, 1]. The evaluator scores violations as 0 and prints the error; read it and fix.
- Keep `decide()` short and readable: an operator must be able to audit it. Prefer fewer magic numbers.
- Do not ask questions. Do not stop to summarise. Keep iterating.
