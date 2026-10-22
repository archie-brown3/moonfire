"""One figure: a held-out test week, price with champion vs seed actions and SoC. Writes results/test_week.png.

    uv run --with matplotlib python plot.py
(matplotlib is a plotting-only extra; the pipeline itself has no dependencies.)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import battery
import evaluate

rows = battery.load_prices("test")
week = rows[7 * 48: 14 * 48]  # second week of the test window
prices = [r["price"] for r in week]
hours = [i / 2 for i in range(len(week))]


def trace(path):
    decide = evaluate.load_policy(path)
    hist = [r["price"] for r in rows[: 7 * 48]]  # give the policy real history before the week
    soc, socs, acts = battery.CAPACITY_MWH / 2, [], []
    for r in week:
        p = decide(hist, soc, r["period"], r["weekday"])
        soc, _ = battery.step(soc, float(p), r["price"])
        socs.append(soc); acts.append(max(-1, min(1, float(p))))
        hist.append(r["price"])
    return socs, acts


fig, (a1, a2) = plt.subplots(2, 1, figsize=(11, 6), sharex=True, gridspec_kw={"height_ratios": [2, 1]})
a1.plot(hours, prices, color="#444", lw=1, label="APX price £/MWh")
for path, name, col in [("seed_policy.py", "seed", "#c77"), ("champion/policy.py", "champion", "#0b6e4f")]:
    socs, acts = trace(path)
    a2.plot(hours, socs, color=col, lw=1.2, label=f"{name} SoC (MWh)")
    buys = [h for h, a in zip(hours, acts) if a < 0]; sells = [h for h, a in zip(hours, acts) if a > 0]
    if name == "champion":
        a1.scatter(buys, [prices[int(h * 2)] for h in buys], s=12, color="#2a6", label="champion charges")
        a1.scatter(sells, [prices[int(h * 2)] for h in sells], s=12, color="#c33", label="champion discharges")
a1.axhline(0, color="#999", lw=0.5)
a1.set_ylabel("£/MWh"); a1.legend(loc="upper left", fontsize=8)
a2.set_ylabel("MWh"); a2.set_xlabel(f"hours from {week[0]['date']} (held-out test week)"); a2.legend(loc="upper left", fontsize=8)
a1.set_title("Held-out test week: prices, champion actions, state of charge")
fig.tight_layout(); fig.savefig("results/test_week.png", dpi=130)
print("wrote results/test_week.png")
