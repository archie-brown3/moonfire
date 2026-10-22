"""Battery spec, simulator, and perfect-foresight oracle. The search loop never edits this file.

Units: power in MW, energy in MWh, price in £/MWh, one step = one half-hour settlement period.
"""
import csv
import math
from datetime import datetime

# Asset spec
POWER_MW = 1.0
CAPACITY_MWH = 2.0
EFFICIENCY = 0.90          # round trip; applied as sqrt each way
DEGRADATION_GBP_PER_MWH = 10.0  # cost per MWh of throughput (charge + discharge)
STEP_H = 0.5
STEP_MWH = POWER_MW * STEP_H    # max energy moved per step at full power
ETA = math.sqrt(EFFICIENCY)

SPLITS = {  # settlement_date ranges, inclusive; split by time, never within a window
    "train": ("2025-10-02", "2026-05-31"),
    "val": ("2026-06-01", "2026-07-31"),
    "test": ("2026-08-01", "2026-10-14"),
}


def load_prices(split: str, path: str = "data/prices.csv") -> list[dict]:
    lo, hi = SPLITS[split]
    out = []
    with open(path) as f:
        for r in csv.DictReader(f):
            if lo <= r["settlement_date"] <= hi:
                t = datetime.fromisoformat(r["start_time"].replace("Z", "+00:00"))
                out.append({"price": float(r["price"]), "period": int(r["period"]),
                            "weekday": t.weekday(), "date": r["settlement_date"]})
    return out


def step(soc: float, power: float, price: float) -> tuple[float, float]:
    """Apply one half-hour action. power>0 discharges, <0 charges. Returns (new_soc, cash).

    The simulator owns all constraints: it clips to the power rating and to what the SoC allows.
    """
    power = max(-POWER_MW, min(POWER_MW, power))
    if power > 0:  # discharge: energy leaving the cell is limited by soc; grid gets eta * that
        e = min(power * STEP_H, soc)
        soc -= e
        cash = e * ETA * price - e * DEGRADATION_GBP_PER_MWH
    elif power < 0:  # charge: energy drawn from grid; cell stores eta * that
        e = min(-power * STEP_H, (CAPACITY_MWH - soc) / ETA)
        soc += e * ETA
        cash = -e * price - e * DEGRADATION_GBP_PER_MWH
    else:
        cash = 0.0
    return soc, cash


def simulate(decide, rows: list[dict], soc0: float = CAPACITY_MWH / 2) -> dict:
    """Replay `rows` calling decide(past_prices, soc, period, weekday) each step.

    The policy only ever sees prices strictly before the current step: the current period's
    price is a settlement price, known only after the fact.
    """
    prices = [r["price"] for r in rows]
    soc, cash, throughput = soc0, 0.0, 0.0
    daily = {}
    for t, r in enumerate(rows):
        p = decide(prices[:t], soc, r["period"], r["weekday"])
        if not isinstance(p, (int, float)) or not math.isfinite(p):
            raise ValueError(f"policy returned non-finite power {p!r} at step {t}")
        new_soc, c = step(soc, float(p), r["price"])
        throughput += abs(new_soc - soc)
        soc, cash = new_soc, cash + c
        daily[r["date"]] = daily.get(r["date"], 0.0) + c
    return {"revenue": cash, "cycles": throughput / (2 * CAPACITY_MWH), "daily": daily, "final_soc": soc}


def oracle(rows: list[dict], soc0: float = CAPACITY_MWH / 2) -> float:
    """Perfect-foresight optimum by exact DP over SoC on a 0.5 MWh grid.

    With 1 MW and 0.5 h steps the only non-dominated actions move exactly STEP_MWH of cell
    energy (or nothing), so the SoC stays on the grid and the DP is exact for this spec.
    """
    n_states = int(round(CAPACITY_MWH / STEP_MWH)) + 1
    best = [0.0] * n_states  # value-to-go from each state at the end: nothing
    for r in reversed(rows):
        price = r["price"]
        nxt = best[:]
        for s in range(n_states):
            v = best[s]  # idle
            if s > 0:  # discharge one grid step
                v = max(v, STEP_MWH * ETA * price - STEP_MWH * DEGRADATION_GBP_PER_MWH + best[s - 1])
            if s < n_states - 1:  # charge one grid step (draw STEP_MWH/ETA from grid)
                v = max(v, -(STEP_MWH / ETA) * price - (STEP_MWH / ETA) * DEGRADATION_GBP_PER_MWH + best[s + 1])
            nxt[s] = v
        best = nxt
    return best[int(round(soc0 / STEP_MWH))]
