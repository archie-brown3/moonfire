"""Score a policy file on a split. The single entry point every search-loop driver calls.

    uv run python evaluate.py policy.py --split train [--json]

Prints JSON: score (£/MW/day), pct_of_oracle, revenue, cycles, days, ci95 (bootstrap over days), error.
A policy that crashes, times out, imports anything but math, or contains a literal date scores 0.
"""
import argparse
import ast
import json
import math
import multiprocessing as mp
import random
import re
import sys

import battery

TIMEOUT_S = 30
ALLOWED_IMPORTS = {"math"}
DATE_RE = re.compile(r"\b20\d\d-\d\d-\d\d\b")


def check_source(src: str) -> None:
    if DATE_RE.search(src):
        raise ValueError("literal dates are not allowed in a policy")
    tree = ast.parse(src)
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
        for n in names:
            if n.split(".")[0] not in ALLOWED_IMPORTS:
                raise ValueError(f"import of {n!r} is not allowed; only {sorted(ALLOWED_IMPORTS)}")


def load_policy(path: str):
    src = open(path).read()
    check_source(src)
    ns = {"__name__": "policy", "__builtins__": __builtins__}
    exec(compile(src, path, "exec"), ns)
    if "decide" not in ns:
        raise ValueError("policy must define decide(past_prices, soc, period, weekday)")
    return ns["decide"]


def _run(path: str, split: str, q) -> None:
    try:
        decide = load_policy(path)
        rows = battery.load_prices(split)
        q.put(battery.simulate(decide, rows))
    except Exception as e:  # noqa: BLE001 - report everything to the loop
        q.put({"error": f"{type(e).__name__}: {e}"})


def bootstrap_ci(daily: list[float], n: int = 1000, seed: int = 0) -> tuple[float, float]:
    rng = random.Random(seed)
    means = sorted(sum(rng.choices(daily, k=len(daily))) / len(daily) for _ in range(n))
    return means[int(0.025 * n)], means[int(0.975 * n)]


def evaluate(path: str, split: str) -> dict:
    q = mp.Queue()
    proc = mp.Process(target=_run, args=(path, split, q))
    proc.start()
    proc.join(TIMEOUT_S)
    if proc.is_alive():
        proc.terminate()
        return {"score": 0.0, "error": f"timeout after {TIMEOUT_S}s"}
    res = q.get() if not q.empty() else {"error": "policy process died"}
    if "error" in res:
        return {"score": 0.0, "error": res["error"]}
    daily = list(res["daily"].values())
    days = len(daily)
    rows = battery.load_prices(split)
    opt = battery.oracle(rows)
    lo, hi = bootstrap_ci(daily)
    return {
        "score": round(res["revenue"] / days, 2),           # £/MW/day (asset is 1 MW)
        "ci95": [round(lo, 2), round(hi, 2)],
        "pct_of_oracle": round(100 * res["revenue"] / opt, 1) if opt else None,
        "revenue": round(res["revenue"], 2),
        "oracle": round(opt, 2),
        "cycles": round(res["cycles"], 1),
        "days": days,
        "error": None,
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("policy")
    ap.add_argument("--split", default="train", choices=list(battery.SPLITS))
    args = ap.parse_args()
    print(json.dumps(evaluate(args.policy, args.split)))
