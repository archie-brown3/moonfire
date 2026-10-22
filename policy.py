"""Dispatch policy. THIS IS THE ONLY FILE THE SEARCH LOOP EDITS.

decide(past_prices, soc, period, weekday) -> power in MW, in [-1, 1].
  past_prices: list of £/MWh for every half-hour before now (oldest first); the current price is unknown.
  soc:         current stored energy in MWh, 0..2
  period:      settlement period of the day, 1..48 (1 = 23:00 UTC previous day)
  weekday:     0 = Monday .. 6 = Sunday
Positive power discharges (sells), negative charges (buys). The simulator clips to physical limits.
Only the `math` module may be imported.
"""
import math

# EVOLVE-BLOCK-START
LOOKBACK = 336         # half-hours of history to rank the latest price against (7 days)
CHARGE_PCT = 0.20      # charge when the latest price is below this quantile of the lookback
DISCHARGE_PCT = 0.80   # discharge when above this quantile


def decide(past_prices, soc, period, weekday):
    if len(past_prices) < LOOKBACK:
        return 0.0
    window = sorted(past_prices[-LOOKBACK:])
    latest = past_prices[-1]
    lo = window[int(CHARGE_PCT * (LOOKBACK - 1))]
    hi = window[int(DISCHARGE_PCT * (LOOKBACK - 1))]
    if latest <= lo:
        return -1.0
    if latest >= hi:
        return 1.0
    return 0.0
# EVOLVE-BLOCK-END
