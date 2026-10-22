"""OpenEvolve driver: evolve policy.py on the TRAIN split and emit a challenger for gate.py.

Run from the repo root:
    uv run --group evolve python drivers/openevolve_driver.py [--iterations N] [--config PATH]

Reads GEMINI_API_KEY from .env (never printed). Writes runs/openevolve/<timestamp>/ with
OpenEvolve's checkpoints, best_policy.py and history.md. Promotion stays with gate.py.
"""

import argparse
import datetime as dt
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from openevolve import run_evolution  # noqa: E402
from openevolve.config import Config  # noqa: E402


def load_env(path: str = ".env") -> dict[str, str]:
    env: dict[str, str] = {}
    if not os.path.exists(path):
        return env
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env


def score_train(path):
    # Self-contained on purpose: OpenEvolve copies this function's source into a temp module,
    # so it cannot rely on module globals or imports. It runs from the repo root.
    import os
    import sys

    root = os.getcwd()
    if root not in sys.path:
        sys.path.insert(0, root)
    import evaluate  # scores a policy file on one split
    from openevolve.evaluation_result import EvaluationResult

    r = evaluate.evaluate(path, "train")
    error = r.get("error") or ""
    score = 0.0 if error else float(r["score"])
    metrics = {
        "combined_score": score,
        "pct_of_oracle": float(r.get("pct_of_oracle") or 0.0),
        "cycles": float(r.get("cycles") or 0.0),
    }
    return EvaluationResult(metrics=metrics, artifacts={"error": error})


def build_config(yaml_path: str, api_key: str) -> Config:
    cfg = Config.from_yaml(yaml_path)
    cfg.llm.api_key = api_key
    for m in cfg.llm.models + cfg.llm.evaluator_models:
        m.api_key = api_key
    cfg.prompt.system_message = open(os.path.join(ROOT, "program.md")).read()
    return cfg


def write_history(run_dir: str) -> None:
    cps = sorted(glob.glob(os.path.join(run_dir, "checkpoints", "checkpoint_*")),
                 key=lambda p: int(p.rsplit("_", 1)[-1]))
    rows = []
    if cps:
        for f in glob.glob(os.path.join(cps[-1], "programs", "*.json")):
            p = json.load(open(f))
            rows.append((p.get("iteration_found", 0), (p.get("parent_id") or "seed")[:8],
                         p.get("metrics", {}).get("combined_score", 0.0)))
    rows.sort()
    best = float("-inf")
    lines = ["| iter | parent | score | best so far |", "|---|---|---|---|"]
    for it, parent, score in rows:
        best = max(best, score)
        lines.append(f"| {it} | {parent} | {score:.2f} | {best:.2f} |")
    open(os.path.join(run_dir, "history.md"), "w").write("\n".join(lines) + "\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=50)
    ap.add_argument("--config", default=os.path.join("drivers", "openevolve.yaml"))
    args = ap.parse_args(argv)

    key = load_env().get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not key:
        print("GEMINI_API_KEY not found in .env or the environment", file=sys.stderr)
        return 1
    if not os.path.exists("policy.py"):
        print("policy.py not found; run from the repo root", file=sys.stderr)
        return 1

    cfg = build_config(args.config, key)
    run_dir = os.path.join("runs", "openevolve", dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ"))
    os.makedirs(run_dir, exist_ok=True)

    result = run_evolution(
        initial_program="policy.py",
        evaluator=score_train,
        config=cfg,
        iterations=args.iterations,
        output_dir=run_dir,
        cleanup=False,
    )
    open(os.path.join(run_dir, "best_policy.py"), "w").write(result.best_code or "")
    write_history(run_dir)
    print(run_dir)
    print(result.best_score)
    return 0


if __name__ == "__main__":
    sys.exit(main())
