"""Sealed evaluator. The agent never edits this file.

Simulates one year of an EV battery doing vehicle-to-grid arbitrage under the
agent's policy. Score = NEGATIVE annual profit in pounds (lower is better, so
the loop's "minimise" convention holds). Verbose mode prints the breakdown.

Physics and rules the agent cannot change:
  battery 60 kWh, charger 7 kW both ways, 90% round-trip efficiency (sqrt each way)
  battery wear: 3p per kWh moved (either direction)
  export price = 85% of import price (typical V2G tariff haircut)
  weekdays: car leaves at 08:00 (slot 16), back 18:00 (slot 36), uses 12 kWh driving
  weekdays: must be >= 48 kWh at 07:00 (slot 14), else 40 pound penalty per shortfall day
  weekends: car at home all day, no driving

Usage: python evaluator/score.py            -> prints one float
       python evaluator/score.py --verbose  -> breakdown
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
PRICES = ROOT / "data" / "prices.npy"
POLICY = ROOT / "problem" / "policy.py"

CAPACITY = 60.0
MAX_KW = 7.0
HALF_HOUR = 0.5
EFF = np.sqrt(0.90)
WEAR_P_PER_KWH = 3.0
EXPORT_FACTOR = 0.85
LEAVE, RETURN = 16, 36
DRIVE_KWH = 12.0
MORNING_SLOT, MIN_MORNING_SOC = 14, 48.0
SHORTFALL_PENALTY_GBP = 40.0
TIMEOUT_S = 20.0           # whole year; ~17.5k calls
PENALTY = 1e6


def load_policy():
    spec = importlib.util.spec_from_file_location("policy", POLICY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.decide


def simulate(decide, prices: np.ndarray, verbose: bool = False) -> float:
    days, slots = prices.shape
    flat = prices.reshape(-1)
    flat = np.concatenate([flat, flat[:48]])  # wrap so day 365 sees a day ahead
    soc = 30.0
    cost_p = revenue_p = wear_p = 0.0
    shortfall_days = 0
    kwh_in = kwh_out = 0.0
    t0 = time.perf_counter()

    for d in range(days):
        weekday = (d % 7) < 5
        for s in range(slots):
            i = d * slots + s
            price = flat[i]
            if weekday and s == MORNING_SLOT and soc < MIN_MORNING_SOC - 1e-6:
                shortfall_days += 1
            if weekday and s == LEAVE:
                soc = max(0.0, soc - DRIVE_KWH)
            if weekday and LEAVE <= s < RETURN:
                continue  # car is away, cannot charge or discharge
            try:
                kw = float(decide(flat[i:i + 48].copy(), soc, s, weekday))
            except Exception as e:
                if verbose:
                    print(f"policy raised: {e}", file=sys.stderr)
                return PENALTY
            if not np.isfinite(kw):
                return PENALTY
            kw = float(np.clip(kw, -MAX_KW, MAX_KW))
            if kw > 0:
                grid_kwh = min(kw * HALF_HOUR, (CAPACITY - soc) / EFF)
                soc += grid_kwh * EFF
                cost_p += grid_kwh * price
                wear_p += grid_kwh * WEAR_P_PER_KWH
                kwh_in += grid_kwh
            elif kw < 0:
                batt_kwh = min(-kw * HALF_HOUR, soc)
                soc -= batt_kwh
                grid_kwh = batt_kwh * EFF
                revenue_p += grid_kwh * price * EXPORT_FACTOR
                wear_p += batt_kwh * WEAR_P_PER_KWH
                kwh_out += grid_kwh
        if time.perf_counter() - t0 > TIMEOUT_S:
            return PENALTY

    profit_gbp = (revenue_p - cost_p - wear_p) / 100.0 - shortfall_days * SHORTFALL_PENALTY_GBP
    if verbose:
        print(f"bought  {kwh_in:8.0f} kWh  cost     £{cost_p/100:8.0f}")
        print(f"sold    {kwh_out:8.0f} kWh  revenue  £{revenue_p/100:8.0f}")
        print(f"wear                     £{wear_p/100:8.0f}")
        print(f"shortfall days {shortfall_days:3d}   penalty  £{shortfall_days*SHORTFALL_PENALTY_GBP:8.0f}")
        print(f"ANNUAL PROFIT            £{profit_gbp:8.0f}   (score = {-profit_gbp:.2f})")
    return -profit_gbp


def evaluate(verbose: bool = False) -> float:
    prices = np.load(PRICES)
    try:
        decide = load_policy()
    except Exception as e:
        if verbose:
            print(f"policy failed to import: {e}", file=sys.stderr)
        return PENALTY
    return simulate(decide, prices, verbose)


if __name__ == "__main__":
    print(f"{evaluate(verbose='--verbose' in sys.argv):.4f}")
