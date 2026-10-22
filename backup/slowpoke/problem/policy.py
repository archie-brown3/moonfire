"""THE ONLY FILE THE AGENT MAY EDIT.

Contract:
    decide(prices_ahead, soc, slot, weekday) -> kW

prices_ahead : np.ndarray, the next 48 half-hourly prices in p/kWh (index 0 = now)
soc          : state of charge in kWh, 0 <= soc <= CAPACITY (60)
slot         : half-hour slot of the day, 0..47 (slot 34 = 17:00)
weekday      : True Mon-Fri, False Sat-Sun

Return power in kW for the next half hour:
    > 0  charge from the grid (buy),  <= MAX_KW
    < 0  discharge to the grid (sell), >= -MAX_KW
    0    idle
The simulator clips to the battery's limits. numpy only, no state between calls,
no file or network access, must return in well under 1 ms.

Constants you may read: CAPACITY=60 kWh, MAX_KW=7, MIN_MORNING_SOC=48 kWh (80%)
required at slot 14 (07:00) on weekdays, car away slots 16..35 on weekdays.
"""
import numpy as np

CAPACITY = 60.0
MAX_KW = 7.0
MIN_MORNING_SOC = 48.0


def decide(prices_ahead: np.ndarray, soc: float, slot: int, weekday: bool) -> float:
    # Baseline: dumb overnight charging. Charge if below the morning target
    # and it's night time. Never discharges. This is what most EV owners do.
    if soc < MIN_MORNING_SOC and (slot < 14 or slot >= 44):
        return MAX_KW
    return 0.0
