"""The search trajectory: every experiment in loop_log.md, kept vs rejected, best-so-far, and the oracle ceiling.
Writes results/loop.png. Reads nothing but loop_log.md and the train oracle.

    uv run --with matplotlib python plot_loop.py
"""
import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import battery

rows = []
for line in open("loop_log.md"):
    m = re.match(r"\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*([-\d.]+)\s*\|\s*(.*?)\s*\|", line)
    if m:
        rows.append((int(m[1]), m[2], float(m[3]), m[4].lower().startswith(("yes", "baseline"))))

train = battery.load_prices("train")
oracle = battery.oracle(train) / len({r["date"] for r in train})

iters = [r[0] for r in rows]
best, run = [], float("-inf")
for _, _, s, kept in rows:
    if kept:
        run = max(run, s)
    best.append(run)

fig, ax = plt.subplots(figsize=(11, 5.2))
ax.axhline(oracle, color="#999", lw=1, ls="--")
ax.text(iters[-1], oracle, f"  perfect foresight £{oracle:.0f}", va="center", fontsize=9, color="#777")
ax.step(iters, best, where="post", color="#0b6e4f", lw=2.2, label="best kept rule")
kept = [(i, s) for i, _, s, k in rows if k]
rej = [(i, s) for i, _, s, k in rows if not k]
ax.scatter([i for i, _ in rej], [s for _, s in rej], s=18, color="#c33", alpha=.55, label="rejected")
ax.scatter([i for i, _ in kept], [s for _, s in kept], s=34, color="#0b6e4f", zorder=3, label="kept")
ax.annotate(f"seed £{rows[0][2]:.1f}", (rows[0][0], rows[0][2]), xytext=(6, -14), textcoords="offset points", fontsize=9)
ax.annotate(f"£{best[-1]:.1f}", (iters[-1], best[-1]), xytext=(-40, 8), textcoords="offset points", fontsize=10, fontweight="bold", color="#0b6e4f")
ax.set_xlabel("experiment"); ax.set_ylabel("train revenue, £/MW/day")
ax.set_title(f"Autoresearch trajectory: {len(rows)-1} experiments, {len(kept)-1} kept, train split")
ax.set_ylim(bottom=0); ax.legend(loc="lower right", fontsize=9); ax.grid(alpha=.25)
fig.tight_layout()
os.makedirs("results", exist_ok=True)
fig.savefig("results/loop.png", dpi=130)
print(f"wrote results/loop.png  ({len(rows)-1} experiments, best £{best[-1]:.2f}, oracle £{oracle:.1f})")
