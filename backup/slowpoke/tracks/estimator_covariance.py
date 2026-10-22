"""THE ONLY FILE THE AGENT MAY EDIT.

Contract: covariance(returns) -> (N, N) symmetric positive-definite matrix.
returns is a (T, N) array of daily returns for the training window only.
numpy only. No file or network access. Must run in under 2 seconds.
"""
import numpy as np


def covariance(returns: np.ndarray) -> np.ndarray:
    return np.cov(returns, rowvar=False)
