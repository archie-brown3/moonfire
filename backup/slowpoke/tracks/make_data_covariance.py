"""Synthetic returns with a known factor structure and a planted regime shift.

Deterministic. Run once; the evaluator reads data/returns.npy.
"""
import numpy as np

SEED = 42
N_ASSETS = 100
N_FACTORS = 4
T = 2000
SHIFT_AT = T // 2


def make() -> np.ndarray:
    rng = np.random.default_rng(SEED)
    loadings = rng.normal(0.0, 1.0, (N_ASSETS, N_FACTORS))
    factor_vol = np.array([0.012, 0.008, 0.006, 0.004])
    factors = rng.normal(0.0, 1.0, (T, N_FACTORS)) * factor_vol
    factors[SHIFT_AT:] *= 2.0  # regime shift: factor risk doubles
    idio = rng.normal(0.0, 0.02, (T, N_ASSETS))
    return factors @ loadings.T + idio


if __name__ == "__main__":
    r = make()
    np.save("data/returns.npy", r)
    print(f"returns.npy  shape={r.shape}  shift_at={SHIFT_AT}")
