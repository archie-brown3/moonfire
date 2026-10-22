"""Score the reference policies on every split and print a table.

    uv run python baselines.py [extra_policy.py ...]
"""
import sys

import battery
import evaluate

BASELINES = {
    "do_nothing": "def decide(p, soc, period, weekday):\n    return 0.0\n",
    # charge 02:00-04:00 UTC (periods 7-10), discharge 17:00-19:00 UTC (periods 37-40)
    "fixed_schedule": (
        "def decide(p, soc, period, weekday):\n"
        "    if 7 <= period <= 10: return -1.0\n"
        "    if 37 <= period <= 40: return 1.0\n"
        "    return 0.0\n"
    ),
}


def main(extra: list[str]) -> None:
    import os, tempfile
    tmp = tempfile.mkdtemp()
    paths = {}
    for name, src in BASELINES.items():
        paths[name] = os.path.join(tmp, f"{name}.py")
        open(paths[name], "w").write(src)
    paths["seed"] = "policy.py"
    for p in extra:
        paths[p] = p
    splits = list(battery.SPLITS)
    print(f"{'policy':18}" + "".join(f"{s + ' £/MW/day':>16}{s + ' %opt':>12}" for s in splits))
    for name, path in paths.items():
        cells = []
        for s in splits:
            r = evaluate.evaluate(path, s)
            cells.append(f"{r['score']:>16.1f}{(r['pct_of_oracle'] or 0):>12.1f}")
        print(f"{name:18}" + "".join(cells))
    cells = []
    for s in splits:
        rows = battery.load_prices(s)
        cells.append(f"{battery.oracle(rows) / len({r['date'] for r in rows}):>16.1f}{100.0:>12.1f}")
    print(f"{'oracle':18}" + "".join(cells))


if __name__ == "__main__":
    main(sys.argv[1:])
