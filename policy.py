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
DISCHARGE_PCT = 0.75   # discharge when above this quantile
HORIZON = 20           # half-hours ahead (10 h) the charging decision looks

def decide(past_prices, soc, period, weekday):
    if len(past_prices) < LOOKBACK:
        return 0.0
    window = sorted(past_prices[-LOOKBACK:])
    latest = (past_prices[-1] + past_prices[-2]) / 2  # smooth out single-period noise
    # buy threshold: the looser of the week's and the last 12 hours' CHARGE_PCT quantile
    lo = max(window[int(CHARGE_PCT * (LOOKBACK - 1))], sorted(past_prices[-24:])[int(CHARGE_PCT * 23)])
    hi = window[int(DISCHARGE_PCT * (LOOKBACK - 1))]
    # time-of-day filter: expected price for each of the next HORIZON half-hours = mean of the same half-hour over
    # the past 5 days
    n = len(past_prices)
    profile = [sum(past_prices[n - 48 * d + k] for d in range(1, 6)) / 5 for k in range(HORIZON)]
    if latest < 0:  # paid to take power: always charge
        return -1.0
    cheaper_ahead = sum(p < profile[0] for p in profile)
    room = (2 - soc) / 0.5  # half-hours of charging needed to fill
    cheap = latest <= lo or cheaper_ahead == 0  # cheap now, or the cheapest slot expected in the horizon
    pays = min(hi, max(profile)) * 0.95 - latest / 0.95 > 20  # sale vs cost per stored MWh (0.95 = sqrt(0.9) each way) covers wear
    if cheap and pays and cheaper_ahead < room + 2:  # not enough cheaper slots ahead to fill up later
        return -1.0
    dearer_soon = sum(p > profile[0] for p in profile[:9])  # selling only looks 4.5 h ahead
    if latest >= hi and dearer_soon < soc / 0.5:  # fewer dearer slots coming than we need to empty
        return 1.0
    return 0.0
# EVOLVE-BLOCK-END
