# OpenEvolve Driver Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** An in-repo driver that uses OpenEvolve as a library to evolve `policy.py` on the train split and emits a best candidate for `gate.py`.

**Architecture:** One script, `drivers/openevolve_driver.py`, loads `.env`, builds an OpenEvolve `Config` from `drivers/openevolve.yaml`, wraps `evaluate.evaluate(path, "train")` as the evaluator, and calls `run_evolution`. Outputs land in a gitignored `runs/openevolve/<timestamp>/` directory. Nothing else in the pipeline changes.

**Tech Stack:** Python 3.12, uv dependency group `evolve` with `openevolve==0.4.0`, Gemini via its OpenAI-compatible endpoint.

**Spec:** `docs/superpowers/specs/2026-10-22-openevolve-driver-design.md`

## Global Constraints

- `pyproject.toml` `dependencies` stays `[]`; OpenEvolve lives only in `[dependency-groups] evolve`.
- The driver never references the `val` or `test` splits.
- `GEMINI_API_KEY` is read from `.env` and never printed or committed.
- `evaluate.py`, `battery.py`, `gate.py`, `policy.py` are not modified.
- Entry point wrapped in `if __name__ == "__main__":` (macOS spawn).

## Review Focus

- Missing `.env` or missing `GEMINI_API_KEY`: exit code 1 with a one-line message, no traceback. Test in Task 1.
- Evaluator error (crash, bad import, non-finite): `combined_score` 0 and the error text in artifacts so the model sees it. Test in Task 1.
- Candidate that edits outside the `EVOLVE-BLOCK`: OpenEvolve rejects it when `enforce_evolve_blocks` is true. Checked by config assertion in Task 1.
- Run interrupted by Ctrl-C: OpenEvolve checkpoints every 5 iterations, so partial results survive in the run directory. Covered by the smoke run in Task 2.
- `evaluate.py` with the default environment (no group): still works, proving zero runtime deps. Verified in Task 2.

---

### Task 1: Driver module with evaluator wrapper and config loading

**Files:**
- Create: `drivers/openevolve_driver.py`
- Create: `drivers/openevolve.yaml`
- Create: `drivers/__init__.py` (empty)
- Create: `tests/test_openevolve_driver.py`
- Modify: `pyproject.toml` (add dependency group)
- Modify: `.gitignore` (add `runs/`)

**Interfaces:**
- Produces: `load_env(path: str = ".env") -> dict[str, str]`; `score_train(path: str) -> EvaluationResult` (metrics `combined_score`, `pct_of_oracle`, `cycles`; artifacts `error`); `build_config(yaml_path: str, api_key: str) -> Config`; `main(argv: list[str] | None = None) -> int`.

- [ ] **Step 1: Add the dependency group and gitignore entry**

In `pyproject.toml` append:
```toml
[dependency-groups]
evolve = ["openevolve==0.4.0"]
```
Append `runs/` to `.gitignore`. Run `uv sync --group evolve` and expect `openevolve` installed.

- [ ] **Step 2: Write the failing tests**

```python
# tests/test_openevolve_driver.py
import os, textwrap, pytest
from drivers import openevolve_driver as drv

def test_load_env_parses_key(tmp_path):
    p = tmp_path / ".env"; p.write_text("GEMINI_API_KEY=abc\n# comment\n")
    assert drv.load_env(str(p)) == {"GEMINI_API_KEY": "abc"}

def test_score_train_returns_combined_score():
    r = drv.score_train("policy.py")
    assert r.metrics["combined_score"] > 0
    assert r.artifacts["error"] == ""

def test_score_train_error_scores_zero(tmp_path):
    bad = tmp_path / "bad.py"; bad.write_text("import os\ndef decide(*a): return 0.0\n")
    r = drv.score_train(str(bad))
    assert r.metrics["combined_score"] == 0
    assert r.artifacts["error"]

def test_build_config_sets_key_and_guards():
    cfg = drv.build_config("drivers/openevolve.yaml", "k")
    assert cfg.llm.api_key == "k"
    assert cfg.enforce_evolve_blocks and cfg.diff_based_evolution
    assert cfg.evaluator.timeout == 10
    assert "EVOLVE-BLOCK" in cfg.prompt.system_message

def test_main_without_key_exits_one(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert drv.main(["--iterations", "1"]) == 1
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `uv run --group evolve python -m pytest tests/test_openevolve_driver.py -v` (pytest is in OpenEvolve's dev extra; if absent, add `pytest` to the `evolve` group).
Expected: FAIL with `ModuleNotFoundError: drivers.openevolve_driver`.

- [ ] **Step 4: Write `drivers/openevolve.yaml`**

Values from the spec's Config section: `llm.api_base` `https://generativelanguage.googleapis.com/v1beta/openai/`, `primary_model gemini-2.5-pro`, `secondary_model gemini-2.5-flash`, `secondary_model_weight 0.2`, `temperature 0.7`, `timeout 120`, `retries 3`; `prompt.num_top_programs 3`, `num_diverse_programs 2`, `include_artifacts true`; `database.population_size 20`, `num_islands 2`, `archive_size 10`, `feature_dimensions [complexity, diversity]`; `evaluator.timeout 10`, `cascade_evaluation false`, `parallel_evaluations 2`; top-level `diff_based_evolution true`, `enforce_evolve_blocks true`, `max_code_length 4000`, `checkpoint_interval 5`, `log_level INFO`. Include a commented `claude_code` provider block. No `api_key` line.

- [ ] **Step 5: Implement `drivers/openevolve_driver.py`**

Functions per the Interfaces block. `load_env` parses `KEY=value` lines, ignoring blanks and `#` comments, no quotes handling. `score_train` imports `evaluate` from the repo root (add the root to `sys.path` at import time) and maps `{score, pct_of_oracle, cycles, error}` into `EvaluationResult(metrics=..., artifacts={"error": error or ""})`; when `error` is non-empty, `combined_score` is `0.0`. `build_config` uses `Config.from_yaml`, sets `cfg.llm.api_key`, and sets `cfg.prompt.system_message` to the text of `program.md`. `main` parses `--iterations` (default 50) and `--config` (default `drivers/openevolve.yaml`), returns 1 with a one-line stderr message if the key is absent, otherwise creates `runs/openevolve/<UTC %Y%m%dT%H%M%SZ>/`, calls `run_evolution(initial_program="policy.py", evaluator=score_train, config=cfg, iterations=n, output_dir=run_dir, cleanup=False)`, writes `best_policy.py` from `result.best_code`, writes `history.md` (header `| iter | parent | score | best so far |`, one row per JSON file under the last `checkpoints/checkpoint_*/programs/` sorted by `iteration_found`), prints `run_dir` and `result.best_score`, returns 0. Guard the call with `if __name__ == "__main__": sys.exit(main())`.

- [ ] **Step 6: Run tests to verify they pass**

Run: `uv run --group evolve python -m pytest tests/test_openevolve_driver.py -v`
Expected: 5 passed.

- [ ] **Step 7: Commit**

```bash
git add drivers pyproject.toml uv.lock .gitignore tests/test_openevolve_driver.py
git commit -m "feat: OpenEvolve driver for policy search (train split only)"
```

### Task 2: Smoke run and verification

**Files:**
- None created in the repo; outputs go to `runs/` (gitignored).

**Interfaces:**
- Consumes: `main` from Task 1 via `uv run --group evolve python drivers/openevolve_driver.py`.

- [ ] **Step 1: Confirm the key is present without printing it**

Run: `grep -c '^GEMINI_API_KEY=' .env`
Expected: `1`.

- [ ] **Step 2: Run three iterations**

Run: `uv run --group evolve python drivers/openevolve_driver.py --iterations 3`
Expected: last two lines are the run directory and a numeric best score; `best_policy.py` and `history.md` exist in that directory.

- [ ] **Step 3: Re-score the emitted candidate on train**

Run: `uv run python evaluate.py runs/openevolve/<dir>/best_policy.py --split train`
Expected: `score` equals the driver's printed best score to two decimals.

- [ ] **Step 4: Guard checks**

Run: `grep -n '"val"\|"test"\|--split' drivers/openevolve_driver.py`
Expected: no matches outside comments.
Run: `uv run python evaluate.py policy.py --split train`
Expected: JSON with a numeric `score`, using the default environment.

- [ ] **Step 5: Record the smoke result**

Append a "Drivers" section to `README.md`: how to run, where output goes, that `gate.py` is still the only promotion path, and the smoke-run score with its date. Commit:

```bash
git add README.md
git commit -m "docs: OpenEvolve driver usage and smoke run"
```
