"""Champion/challenger promotion. Run after the search loop.

    uv run python gate.py policy.py

Scores challenger and current champion on VAL. Promotes the challenger to champion/policy.py only if its
val score is higher. Then scores champion, baselines and oracle on TEST once and writes results/results.md.
"""
import json
import os
import shutil
import sys

import baselines
import battery
import evaluate

CHAMPION = "champion/policy.py"
SEED = "seed_policy.py"  # frozen copy of the starting policy; never edited


def main(challenger: str) -> None:
    os.makedirs("champion", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    first = not os.path.exists(CHAMPION)
    if first:
        shutil.copy(SEED, CHAMPION)
    ch = evaluate.evaluate(challenger, "val")
    cu = evaluate.evaluate(CHAMPION, "val")
    promoted = ch["score"] > cu["score"] and not ch["error"]
    print(f"val: challenger {ch['score']} vs champion {cu['score']} -> {'PROMOTE' if promoted else 'reject'}")
    if promoted:
        shutil.copy(challenger, CHAMPION)

    # Final report: test is touched here only.
    rows = {"seed": SEED, "champion": CHAMPION}
    import tempfile
    tmp = tempfile.mkdtemp()
    for name, src in baselines.BASELINES.items():
        p = os.path.join(tmp, f"{name}.py"); open(p, "w").write(src); rows[name] = p
    lines = ["| policy | train £/MW/day | val £/MW/day | test £/MW/day | test 95% CI | test % of oracle | test cycles |", "|---|---|---|---|---|---|---|"]
    out = {}
    for name in ["do_nothing", "fixed_schedule", "seed", "champion"]:
        r = {s: evaluate.evaluate(rows[name], s) for s in battery.SPLITS}
        out[name] = r
        t = r["test"]
        lines.append(f"| {name} | {r['train']['score']} | {r['val']['score']} | {t['score']} | {t['ci95'][0]}–{t['ci95'][1]} | {t['pct_of_oracle']} | {t['cycles']} |")
    oracle = {s: round(battery.oracle(battery.load_prices(s)) / len({r['date'] for r in battery.load_prices(s)}), 1) for s in battery.SPLITS}
    lines.append(f"| perfect foresight | {oracle['train']} | {oracle['val']} | {oracle['test']} | – | 100 | – |")
    md = "\n".join(lines)
    open("results/results.md", "w").write(md + "\n")
    json.dump(out, open("results/results.json", "w"), indent=1)
    print(md)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "policy.py")
