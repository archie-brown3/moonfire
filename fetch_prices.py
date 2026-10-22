"""Fetch half-hourly GB market index prices (APX, £/MWh) from Elexon's open BMRS API.

Writes data/prices.csv with columns: start_time, settlement_date, period, price, volume.
No auth needed. The API caps a request at 7 days, so we page through the range.
"""
import csv
import json
import sys
import urllib.request
from datetime import date, timedelta

URL = "https://data.elexon.co.uk/bmrs/api/v1/balancing/pricing/market-index?from={}&to={}"
PROVIDER = "APXMIDP"  # one series only; N2EXMIDP is a second exchange with sparse volume


def fetch(start: date, end: date) -> list[dict]:
    rows = {}
    day = start
    while day < end:
        chunk_end = min(day + timedelta(days=7), end)
        with urllib.request.urlopen(URL.format(day, chunk_end), timeout=30) as r:
            data = json.load(r)["data"]
        for rec in data:
            if rec["dataProvider"] != PROVIDER:
                continue
            key = (rec["settlementDate"], rec["settlementPeriod"])
            rows[key] = rec  # dedupe overlapping chunk boundaries
        print(f"{day} -> {chunk_end}: {len(data)} rows", file=sys.stderr)
        day = chunk_end
    return [rows[k] for k in sorted(rows)]


def clean(rows: list[dict]) -> list[dict]:
    """Drop partial first/last settlement days; interpolate untraded (zero-volume) periods."""
    first, last = rows[0]["settlementDate"], rows[-1]["settlementDate"]
    rows = [r for r in rows if r["settlementDate"] not in (first, last)]
    untraded = [i for i, r in enumerate(rows) if r["volume"] == 0]
    for i in untraded:
        lo = next(j for j in range(i, -1, -1) if rows[j]["volume"] > 0)
        hi = next(j for j in range(i, len(rows)) if rows[j]["volume"] > 0)
        w = (i - lo) / (hi - lo)
        rows[i]["price"] = round(rows[lo]["price"] * (1 - w) + rows[hi]["price"] * w, 2)
    print(f"interpolated {len(untraded)} untraded periods", file=sys.stderr)
    return rows


def main(start: str, end: str, out: str = "data/prices.csv") -> None:
    rows = clean(fetch(date.fromisoformat(start), date.fromisoformat(end)))
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["start_time", "settlement_date", "period", "price", "volume"])
        for r in rows:
            w.writerow([r["startTime"], r["settlementDate"], r["settlementPeriod"], r["price"], r["volume"]])
    print(f"wrote {len(rows)} rows to {out}", file=sys.stderr)


if __name__ == "__main__":
    main(*sys.argv[1:])
