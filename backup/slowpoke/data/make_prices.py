"""A year of half-hourly electricity prices (p/kWh), UK-shaped. Deterministic.

Daily shape: cheap overnight, morning bump, big evening peak 16:00-19:30.
Weekly: weekends flatter. Seasonal: winter higher. Random spikes (scarcity)
and occasional negative prices overnight (surplus wind).

Writes data/prices.npy with shape (365, 48) = days x half-hours.
To use real data instead, see data/from_csv.py.
"""
import numpy as np

SEED = 7
DAYS, SLOTS = 365, 48


def make() -> np.ndarray:
    rng = np.random.default_rng(SEED)
    t = np.arange(SLOTS) / 2.0  # hour of day
    daily = (8.0
             + 6.0 * np.exp(-((t - 8.0) ** 2) / 2.0)        # morning bump
             + 22.0 * np.exp(-((t - 17.5) ** 2) / 2.5)      # evening peak
             - 4.0 * np.exp(-((t - 3.5) ** 2) / 4.0))       # overnight trough
    out = np.empty((DAYS, SLOTS))
    for d in range(DAYS):
        season = 1.0 + 0.35 * np.cos(2 * np.pi * (d - 15) / 365)   # winter high
        weekend = 0.8 if (d % 7) in (5, 6) else 1.0
        level = rng.lognormal(0.0, 0.18)                          # day-to-day
        noise = rng.normal(0.0, 1.2, SLOTS)
        p = daily * season * level
        p[:] *= np.where((t >= 16) & (t < 20), weekend, 1.0)
        p += noise
        if rng.random() < 0.08:                                   # scarcity spike
            k = rng.integers(32, 40)
            p[k:k + 4] += rng.uniform(30, 90)
        if rng.random() < 0.10:                                   # windy night
            p[2:12] -= rng.uniform(8, 16)
        out[d] = p
    return np.round(out, 2)


if __name__ == "__main__":
    p = make()
    np.save("data/prices.npy", p)
    print(f"prices.npy shape={p.shape}  mean={p.mean():.1f}p  min={p.min():.1f}p  max={p.max():.1f}p")
