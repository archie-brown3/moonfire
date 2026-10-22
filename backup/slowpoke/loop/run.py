"""The research loop. Karpathy-style: one editable file (problem/policy.py), sealed evaluator,
commit if better, revert if not, log everything.

    python loop/run.py --iterations 40
    python loop/run.py --iterations 40 --explore 0.2   # 20% of the time branch off a top-5 parent

Each iteration:
  1. select a parent from the archive (best, or occasionally a random top-5 one)
  2. ask the model for ONE change to policy.py, given parent source + experiment log
  3. write the candidate, run evaluator/score.py, read one number
  4. archive the candidate; commit if it beat the best, otherwise restore the best
  5. append a row to database/results.tsv
"""
import argparse
import json
import os
import random
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import anthropic

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "problem" / "policy.py"
ARCHIVE = ROOT / "database" / "archive"
RESULTS = ROOT / "database" / "results.tsv"
PROMPT = (ROOT / "loop" / "prompts" / "hypothesiser.md").read_text()
MODEL = os.environ.get("SLOWPOKE_MODEL", "claude-sonnet-4-5")
HEADER = "n\tparent\tscore\tbest\tkept\thypothesis\n"

client = anthropic.Anthropic()


def score() -> float:
    out = subprocess.run([sys.executable, str(ROOT / "evaluator" / "score.py")],
                         capture_output=True, text=True, timeout=120)
    try:
        return float(out.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return 1e6


def read_log() -> list[dict]:
    if not RESULTS.exists():
        return []
    rows = []
    for line in RESULTS.read_text().splitlines()[1:]:
        n, parent, s, best, kept, hyp = line.split("\t")
        rows.append(dict(n=int(n), parent=int(parent), score=float(s),
                         best=float(best), kept=kept == "1", hypothesis=hyp))
    return rows


def append_row(n, parent, s, best, kept, hyp):
    if not RESULTS.exists():
        RESULTS.write_text(HEADER)
    hyp = hyp.replace("\t", " ").replace("\n", " ")
    with RESULTS.open("a") as f:
        f.write(f"{n}\t{parent}\t{s:.6f}\t{best:.6f}\t{int(kept)}\t{hyp}\n")


def select_parent(log, explore: float) -> int:
    """Return archive id of the parent. 0 is the baseline."""
    scored = [(r["score"], r["n"]) for r in log if r["score"] < 1e5]
    scored.append((log[0]["best"] if log else float("inf"), 0))
    scored.sort()
    if random.random() < explore and len(scored) > 1:
        return random.choice(scored[:5])[1]
    return scored[0][1]


def propose(parent_src: str, log: list[dict]) -> tuple[str, str]:
    history = "\n".join(
        f"#{r['n']} score={r['score']:.4f} {'KEPT' if r['kept'] else 'reverted'}: {r['hypothesis']}"
        for r in log[-25:]) or "(no experiments yet)"
    user = f"CURRENT BEST policy.py:\n```python\n{parent_src}\n```\n\nEXPERIMENT LOG:\n{history}\n\nPropose the next experiment. JSON only."
    msg = client.messages.create(model=MODEL, max_tokens=4000, temperature=0.7,
                                 system=PROMPT, messages=[{"role": "user", "content": user}])
    text = msg.content[0].text
    m = re.search(r"\{.*\}", text, re.S)
    data = json.loads(m.group(0))
    return data["hypothesis"].strip(), data["source"]


def git(*args):
    subprocess.run(["git", *args], cwd=ROOT, capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=30)
    ap.add_argument("--explore", type=float, default=0.15)
    args = ap.parse_args()

    ARCHIVE.mkdir(parents=True, exist_ok=True)
    log = read_log()
    if not (ARCHIVE / "0.py").exists():
        shutil.copy(TARGET, ARCHIVE / "0.py")
    best_src = TARGET.read_text()
    best = min([r["best"] for r in log], default=None)
    if best is None:
        best = score()
        print(f"baseline score {best:.4f}")
        append_row(0, 0, best, best, True, "baseline: dumb overnight charging")
        log = read_log()

    for _ in range(args.iterations):
        n = log[-1]["n"] + 1
        parent = select_parent(log, args.explore)
        parent_src = (ARCHIVE / f"{parent}.py").read_text()
        t0 = time.time()
        try:
            hyp, src = propose(parent_src, log)
        except Exception as e:
            print(f"#{n} proposal failed: {e}")
            continue
        TARGET.write_text(src)
        (ARCHIVE / f"{n}.py").write_text(src)
        s = score()
        kept = s < best
        if kept:
            best, best_src = s, src
            git("add", "-A")
            git("commit", "-q", "-m", f"exp {n}: {hyp} (score {s:.4f})")
        else:
            TARGET.write_text(best_src)
        append_row(n, parent, s, best, kept, hyp)
        log = read_log()
        tag = "KEPT   " if kept else "revert "
        print(f"#{n:3d} {tag} {s:9.4f}  best {best:.4f}  parent {parent:3d}  {time.time()-t0:4.0f}s  {hyp}")


if __name__ == "__main__":
    main()
