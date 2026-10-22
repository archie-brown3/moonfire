# OpenEvolve driver for the policy search

Date: 2026-10-22. Branch: `feature/openevolve-driver`.

## Goal

Replace the Claude Code session that follows `program.md` with an in-repo evolutionary driver that uses OpenEvolve as a library to search for a better `policy.py`. The evaluator, the split rules and `gate.py` do not change. The driver only ever scores on the train split.

## Non-goals

- Changing `evaluate.py`, `battery.py`, `gate.py` or the task contract.
- Promotion. The driver emits a best candidate; `gate.py` remains the only path to `champion/`.
- A scheduled job. That stays in the README's adoption story.

## Files

| File | Role |
|---|---|
| `drivers/openevolve_driver.py` | The driver. About 60 lines. |
| `drivers/openevolve.yaml` | OpenEvolve config: LLM, prompt, database, evaluator settings. |
| `pyproject.toml` | Adds `[dependency-groups] evolve = ["openevolve==0.4.0"]`. `dependencies` stays empty. |
| `.gitignore` | Adds `runs/`. |
| `runs/openevolve/<UTC timestamp>/` | Per-run output: OpenEvolve checkpoints and logs, `best_policy.py`, `history.md`. Gitignored. |

## Driver behaviour

Invocation: `uv run --group evolve python drivers/openevolve_driver.py [--iterations N] [--config PATH]`. Defaults: 50 iterations, `drivers/openevolve.yaml`.

1. Load `.env` from the repo root (plain `KEY=value` lines, no dependency) and read `GEMINI_API_KEY`. Fail with a clear message if missing. Never print it.
2. Build the OpenEvolve `Config` from the yaml, then set `llm.api_key` from the env var and `prompt.system_message` to the contents of `program.md`.
3. Call `run_evolution(initial_program="policy.py", evaluator=score_train, config=config, iterations=N, output_dir=run_dir, cleanup=False)`.
4. `score_train(path)` calls `evaluate.evaluate(path, "train")` and returns `{"combined_score": score, "pct_of_oracle": ..., "cycles": ..., "error": error or ""}`. When the evaluator reports an error, `combined_score` is 0 and `error` carries the text so the next prompt shows it. The function never references any split other than train.
5. After the run, write `best_policy.py` (the result's best code) and `history.md` (one row per evaluated program: iteration, parent, score, kept, drawn from the result's database or checkpoint) into the run directory. Print the run directory and the best train score as the last line.
6. Wrap the entry point in `if __name__ == "__main__":` because macOS multiprocessing uses spawn.

## Config (yaml)

- `llm`: `api_base: https://generativelanguage.googleapis.com/v1beta/openai/`, `primary_model: gemini-2.5-pro`, `secondary_model: gemini-2.5-flash` with a small weight, `temperature: 0.7`, `timeout: 120`, `retries: 3`. `api_key` is not in the file. A commented block shows the `claude_code` provider as an alternative.
- `prompt`: `num_top_programs: 3`, `num_diverse_programs: 2`, `include_artifacts: true` so errors reach the model.
- `database`: `population_size: 20`, `num_islands: 2`, `archive_size: 10`, `feature_dimensions: ["complexity", "diversity"]` (OpenEvolve's built-in dimensions; no custom feature code).
- `evaluator`: `timeout: 10`, `cascade_evaluation: false`, `parallel_evaluations: 2`.
- `diff_based_evolution: true`, `allow_full_rewrites: false`, `max_code_length: 4000`. Edits stay inside the existing `EVOLVE-BLOCK` markers.

## Guards and errors

- `evaluate.py` already enforces the import allow-list, no literal dates, finite output, the 10 s timeout and score 0 on failure. The driver relies on it and adds nothing.
- A missing key, missing `policy.py`, or an OpenEvolve import failure exits non-zero with a one-line reason.
- Model or network failures inside a generation are handled by OpenEvolve's retries; the iteration is skipped, the run continues.

## Testing

1. Unit-free smoke test: `--iterations 3` from the worktree. Expect a run directory with `best_policy.py` and `history.md`.
2. Re-score `best_policy.py` with `uv run python evaluate.py runs/.../best_policy.py --split train` and check the score matches the driver's reported best.
3. `grep -n "val\|test" drivers/openevolve_driver.py` returns only the words inside comments or none.
4. `uv run python evaluate.py policy.py --split train` still works with the default (no group) environment, proving the pipeline stays dependency-free.

## Open defaults

- Primary model `gemini-2.5-pro`. Switch to Flash in the yaml if speed matters more than quality.
- 50 iterations per run. Scale once a smoke run shows the per-iteration time.
