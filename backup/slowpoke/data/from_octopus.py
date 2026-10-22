"""Pull a year of real UK half-hourly prices from the Octopus Agile tariff API
and write data/prices.npy with shape (days, 48). No API key needed.

    python data/from_octopus.py                       # last 365 days, London region (C)
    python data/from_octopus.py --days 365 --region C

Agile prices are p/kWh inc VAT, set day-ahead from wholesale, so they are the
real signal a V2G policy would trade against. Days with missing slots are dropped.
"""
import argparse
import datetime as dt
import json
import urllib.request
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
PRODUCT = "AGILE-24-10-01"


def fetch(region: str, start: dt.datetime, end: dt.datetime) -> list[dict]:
    url = (f"https://api.octopus.energy/v1/products/{PRODUCT}/electricity-tariffs/"
           f"E-1R-{PRODUCT}-{region}/standard-unit-rates/"
           f"?period_from={start:%Y-%m-%dT%H:%MZ}&period_to={end:%Y-%m-%dT%H:%MZ}&page_size=1500")
    out = []
    while url:
        with urllib.request.urlopen(url, timeout=30) as r:
            page = json.load(r)
        out.extend(page["results"])
        url = page.get("next")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=365)
    ap.add_argument("--region", default="C", help="A-P, C = London")
    args = ap.parse_args()

    end = dt.datetime.now(dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    start = end - dt.timedelta(days=args.days)
    rows = []
    cur = start
    while cur < end:                       # fetch in ~60-day chunks
        nxt = min(cur + dt.timedelta(days=60), end)
        rows.extend(fetch(args.region, cur, nxt))
        cur = nxt

    by_day = defaultdict(dict)
    for r in rows:
        t = dt.datetime.fromisoformat(r["valid_from"].replace("Z", "+00:00"))
        by_day[t.date()][t.hour * 2 + t.minute // 30] = r["value_inc_vat"]

    days = sorted(d for d, slots in by_day.items() if len(slots) == 48)
    prices = np.array([[by_day[d][s] for s in range(48)] for d in days])
    np.save(ROOT / "data" / "prices.npy", np.round(prices, 2))
    (ROOT / "data" / "prices_dates.txt").write_text("\n".join(map(str, days)))
    print(f"prices.npy shape={prices.shape}  {days[0]} to {days[-1]}  "
          f"mean={prices.mean():.1f}p  min={prices.min():.1f}p  max={prices.max():.1f}p")


if __name__ == "__main__":
    main()
