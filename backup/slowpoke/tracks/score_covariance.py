"""Sealed evaluator. The agent never edits this file and never sees test windows.

Rolling walk-forward:
  train on TRAIN days -> estimator builds covariance -> min-variance portfolio
  -> realised volatility on the next TEST days (never used for fitting).
Score = annualised out-of-sample volatility (%) + turnover penalty. Lower is better.

Usage: python evaluator/score.py            -> prints one float
       python evaluator/score.py --verbose  -> per-window breakdown
"""
import importlib.util
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
RETURNS = ROOT / "data" / "returns.npy"
ESTIMATOR = ROOT / "problem" / "estimator.py"
SPLITS = ROOT / "evaluator" / "splits.json"

TRAIN, TEST = 250, 60
TURNOVER_PENALTY = 0.5     # score points per unit of average turnover
TIMEOUT_S = 2.0            # per estimator call
PENALTY = 1e6              # returned on any failure: crash, NaN, non-PSD, timeout
ANNUALISE = np.sqrt(252) * 100


def load_estimator():
    spec = importlib.util.spec_from_file_location("estimator", ESTIMATOR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.covariance


def min_variance_weights(cov: np.ndarray) -> np.ndarray:
    n = cov.shape[0]
    cov = cov + 1e-8 * np.eye(n)       # numerical floor only
    ones = np.ones(n)
    w = np.linalg.solve(cov, ones)
    return w / w.sum()


def splits(T: int):
    if SPLITS.exists():
        return json.loads(SPLITS.read_text())
    out, start = [], 0
    while start + TRAIN + TEST <= T:
        out.append([start, start + TRAIN, start + TRAIN + TEST])
        start += TEST
    SPLITS.write_text(json.dumps(out))
    return out


def evaluate(verbose: bool = False) -> float:
    r = np.load(RETURNS)
    try:
        estimator = load_estimator()
    except Exception as e:
        if verbose:
            print(f"estimator failed to import: {e}", file=sys.stderr)
        return PENALTY

    windows = splits(len(r))
    if not windows:
        sys.exit(f"need at least {TRAIN + TEST} days of returns, have {len(r)}")
    vols, turnovers, prev_w = [], [], None
    for a, b, c in windows:
        train, test = r[a:b], r[b:c]
        t0 = time.perf_counter()
        try:
            cov = np.asarray(estimator(train.copy()), dtype=float)
        except Exception as e:
            if verbose:
                print(f"estimator raised: {e}", file=sys.stderr)
            return PENALTY
        if time.perf_counter() - t0 > TIMEOUT_S:
            return PENALTY
        if cov.shape != (train.shape[1], train.shape[1]) or not np.all(np.isfinite(cov)):
            return PENALTY
        cov = 0.5 * (cov + cov.T)
        if np.linalg.eigvalsh(cov).min() <= 0:
            return PENALTY
        w = min_variance_weights(cov)
        if not np.all(np.isfinite(w)):
            return PENALTY
        oos = test @ w
        vols.append(oos.std(ddof=1) * ANNUALISE)
        if prev_w is not None:
            turnovers.append(np.abs(w - prev_w).sum())
        prev_w = w
        if verbose:
            print(f"window {a:4d}-{c:4d}  oos_vol={vols[-1]:6.2f}%")

    vol = float(np.mean(vols))
    turn = float(np.mean(turnovers)) if turnovers else 0.0
    score = vol + TURNOVER_PENALTY * turn
    if verbose:
        print(f"mean_oos_vol={vol:.3f}%  mean_turnover={turn:.3f}  score={score:.4f}")
    return score


if __name__ == "__main__":
    print(f"{evaluate(verbose='--verbose' in sys.argv):.6f}")
