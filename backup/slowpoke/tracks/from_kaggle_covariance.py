"""Build data/returns.npy from the Kaggle "S&P 500 stock data" CSV.

Dataset: kaggle.com/datasets/camnugent/sandp500  ->  all_stocks_5yr.csv
Columns: date, open, high, low, close, volume, Name

    python data/from_kaggle.py path/to/all_stocks_5yr.csv [--n 100]

Keeps the N most liquid tickers with a complete history, builds daily log
returns, and writes data/returns.npy plus data/tickers.txt. Deterministic.
"""
import argparse
import csv
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--n", type=int, default=100)
    args = ap.parse_args()

    closes, volumes = defaultdict(dict), defaultdict(float)
    with open(args.csv, newline="") as f:
        for row in csv.DictReader(f):
            try:
                c, v = float(row["close"]), float(row["volume"])
            except ValueError:
                continue
            closes[row["Name"]][row["date"]] = c
            volumes[row["Name"]] += c * v  # dollar volume as liquidity proxy

    dates = sorted(set.intersection(*(set(d) for d in closes.values())))
    full = [t for t in closes if set(dates) <= set(closes[t])]
    tickers = sorted(full, key=lambda t: -volumes[t])[: args.n]

    prices = np.array([[closes[t][d] for t in tickers] for d in dates])
    returns = np.diff(np.log(prices), axis=0)

    np.save(ROOT / "data" / "returns.npy", returns)
    (ROOT / "data" / "tickers.txt").write_text("\n".join(tickers))
    (ROOT / "evaluator" / "splits.json").unlink(missing_ok=True)  # splits depend on T
    print(f"returns.npy shape={returns.shape}  {dates[0]} to {dates[-1]}  tickers={len(tickers)}")


if __name__ == "__main__":
    main()
