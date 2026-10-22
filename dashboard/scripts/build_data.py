"""Build dashboard/data/dashboard.json from the repo: loop log, prices, policy replays, gate results.

    uv run python dashboard/scripts/build_data.py        (from the repo root)

Reads train only for policy replays. Val/test numbers come solely from results/results.json
written by gate.py, so the dashboard never touches held-out splits itself.
"""
import json
import os
import re
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

import baselines  # noqa: E402
import battery  # noqa: E402
import evaluate  # noqa: E402

OUT = os.path.join(ROOT, "dashboard", "data", "dashboard.json")


def loop_log():
    rows, best = [], None
    for line in open("loop_log.md"):
        m = re.match(r"\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*([\d.]+)\s*\|\s*(.*?)\s*\|", line)
        if not m:
            continue
        it, idea, score, kept = int(m[1]), m[2], float(m[3]), m[4]
        is_kept = kept.startswith("yes") or kept == "baseline"
        prev_best = best
        if best is None or (is_kept and score > best):
            best = score
        rows.append({"iter": it, "idea": idea, "score": score, "kept": is_kept, "best": best,
                     "gain": round(score - prev_best, 2) if (is_kept and prev_best is not None) else None})
    return rows


def policies():
    tmp = tempfile.mkdtemp()
    paths = {}
    for name, src in baselines.BASELINES.items():
        paths[name] = os.path.join(tmp, f"{name}.py")
        open(paths[name], "w").write(src)
    paths["seed"] = "seed_policy.py"
    paths["champion"] = "policy.py"
    return paths


def replay(path, rows):
    decide = evaluate.load_policy(path)
    return battery.simulate(decide, rows)


def week_trace(path, rows, start, n=7 * 48):
    decide = evaluate.load_policy(path)
    hist = [r["price"] for r in rows[:start]]
    soc, out = battery.CAPACITY_MWH / 2, []
    for r in rows[start:start + n]:
        p = decide(hist, soc, r["period"], r["weekday"])
        p = max(-1.0, min(1.0, float(p)))
        soc, _ = battery.step(soc, p, r["price"])
        out.append({"soc": round(soc, 3), "action": p})
        hist.append(r["price"])
    return out


def main():
    train = battery.load_prices("train")
    paths = policies()

    # per-split evaluation on TRAIN only (val/test come from the gate's results file)
    train_eval = {name: evaluate.evaluate(p, "train") for name, p in paths.items()}
    train_days = len({r["date"] for r in train})
    oracle_train = battery.oracle(train)

    # daily revenue, cumulative, champion vs seed on train
    sims = {name: replay(paths[name], train) for name in ("seed", "champion")}
    dates = sorted(sims["champion"]["daily"])
    cum = {"seed": 0.0, "champion": 0.0}
    daily = []
    for d in dates:
        row = {"date": d}
        for name in cum:
            v = sims[name]["daily"][d]
            cum[name] += v
            row[name] = round(v, 2)
            row[f"{name}_cum"] = round(cum[name], 1)
        daily.append(row)

    # daily price summary across the whole year, tagged with split
    all_rows = []
    for split in battery.SPLITS:
        for r in battery.load_prices(split):
            all_rows.append((split, r))
    by_date = {}
    for split, r in all_rows:
        d = by_date.setdefault(r["date"], {"date": r["date"], "split": split, "prices": []})
        d["prices"].append(r["price"])
    price_days = []
    for d in sorted(by_date):
        ps = by_date[d]["prices"]
        price_days.append({"date": d, "split": by_date[d]["split"], "mean": round(sum(ps) / len(ps), 1),
                           "min": round(min(ps), 1), "max": round(max(ps), 1), "spread": round(max(ps) - min(ps), 1),
                           "negative": sum(1 for p in ps if p < 0)})
    split_stats = {}
    for split in battery.SPLITS:
        rows = battery.load_prices(split)
        ps = [r["price"] for r in rows]
        ndays = len({r["date"] for r in rows})
        split_stats[split] = {"days": ndays, "periods": len(rows), "mean_price": round(sum(ps) / len(ps), 1),
                              "negative_periods": sum(1 for p in ps if p < 0),
                              "oracle_per_day": round(battery.oracle(rows) / ndays, 1),
                              "range": list(battery.SPLITS[split])}

    # one in-sample week (last full week of train) so no held-out data is shown
    start = len(train) - 7 * 48
    week_rows = train[start:start + 7 * 48]
    traces = {name: week_trace(paths[name], train, start) for name in ("seed", "champion")}
    week = []
    for i, r in enumerate(week_rows):
        week.append({"h": i / 2, "date": r["date"], "period": r["period"], "price": r["price"],
                     "champion_soc": traces["champion"][i]["soc"], "seed_soc": traces["seed"][i]["soc"],
                     "champion_action": traces["champion"][i]["action"], "seed_action": traces["seed"][i]["action"]})

    results = None
    if os.path.exists("results/results.json"):
        results = json.load(open("results/results.json"))

    # champion source, evolve block only
    src = open("policy.py").read()
    m = re.search(r"# EVOLVE-BLOCK-START\n(.*?)# EVOLVE-BLOCK-END", src, re.S)
    evolve_block = m[1].strip() if m else src

    data = {
        "generated_at": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        "spec": {"power_mw": battery.POWER_MW, "capacity_mwh": battery.CAPACITY_MWH, "efficiency": battery.EFFICIENCY,
                 "degradation_gbp_per_mwh": battery.DEGRADATION_GBP_PER_MWH, "step_h": battery.STEP_H},
        "splits": split_stats,
        "loop": loop_log(),
        "train_eval": train_eval,
        "oracle_train_per_day": round(oracle_train / train_days, 2),
        "daily": daily,
        "price_days": price_days,
        "week": week,
        "results": results,
        "evolve_block": evolve_block,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(data, open(OUT, "w"))
    print(f"wrote {OUT}: {len(data['loop'])} iters, {len(daily)} train days, {len(price_days)} price days, "
          f"results={'yes' if results else 'no'}")


if __name__ == "__main__":
    main()
