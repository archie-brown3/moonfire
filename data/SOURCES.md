# Price data sources

What `fetch_prices.py` uses today, and other open series the same pipeline can run on. Each one is a different `fetch_*.py` writing the same `data/prices.csv` columns (`start_time, settlement_date, period, price, volume`); nothing else in the repo changes. "Verified" means the endpoint was called on 22 Oct 2026 and returned the fields described. "Untested" means documented but not called tonight.

## In use

**Elexon BMRS market index (APX), GB** · verified · half-hourly · £/MWh · no key
`https://data.elexon.co.uk/bmrs/api/v1/balancing/pricing/market-index?from=YYYY-MM-DD&to=YYYY-MM-DD`
7-day cap per request. Fields: `settlementDate, settlementPeriod, startTime, price, volume, dataProvider` (keep `APXMIDP`). This is what the loop trades.

## Same market, different price (GB)

**Elexon system (imbalance) prices** · verified · half-hourly · £/MWh · no key
`https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/YYYY-MM-DD`
One day per call. Fields include `settlementPeriod, startTime, systemSellPrice, systemBuyPrice, netImbalanceVolume`. Since Nov 2015 sell and buy are equal (single price). Use when modelling a battery that trades imbalance rather than the day-ahead index; spikier, higher ceiling, more realistic for BM-exposed assets.

**Elexon N2EX market index** · verified (same endpoint as APX) · half-hourly · £/MWh
Same URL as above, `dataProvider == "N2EXMIDP"`. Sparse volume; useful as a second exchange for robustness checks.

## Other markets (test the "change the fetcher" claim)

**Germany/Luxembourg day-ahead, Energy-Charts (Fraunhofer ISE)** · verified · 15-minute · EUR/MWh · no key
`https://api.energy-charts.info/price?bzn=DE-LU&start=YYYY-MM-DD&end=YYYY-MM-DD`
Returns `unix_seconds[]`, `price[]`, `unit`. Data credited to SMARD.de (Bundesnetzagentur). Other zones via `bzn=` (FR, NL, AT, CH, ES, IT-North, NO2, SE3 and more). 15-minute steps: aggregate to 30 or change `STEP_H` in `battery.py` to 0.25. Negative prices common on sunny weekends, which is a good stress test for the policy.

**Australia NEM, AEMO NEMWEB** · untested · 5-minute dispatch and 30-minute trading · AUD/MWh · no key
Monthly CSV archives at `https://nemweb.com.au/Reports/Archive/` (e.g. `Dispatch_SCADA`, `TradingIS_Reports`) and the aggregated `https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem/data-nem/aggregated-data` price-and-demand CSVs per region (NSW1, QLD1, SA1, TAS1, VIC1). SA1 has the most volatile prices of any major market, which is where batteries earn the most and where Tesla's Hornsdale runs.

**US ERCOT and CAISO, via gridstatus** · untested · 5-minute to hourly · USD/MWh
`pip install gridstatus`, then `gridstatus.Ercot().get_rtm_spp(...)` or `gridstatus.CAISO().get_lmp(...)`. Open-source Python wrapper around the ISOs' public portals. ERCOT real-time is the market Gridmatic quotes its 51% of theoretical figure on.

**Nord Pool and ENTSO-E Transparency** · untested · hourly / 15-minute · EUR/MWh · ENTSO-E needs a free API token
ENTSO-E `https://web-api.tp.entsoe.eu/api?documentType=A44&in_Domain=...&out_Domain=...` covers every European bidding zone from one endpoint; XML responses. Nord Pool's own API requires registration. Energy-Charts above is the no-token route to the same day-ahead numbers for most zones.

## Household tariffs (if the asset is an EV or home battery instead of a grid-scale unit)

**Octopus Agile, GB** · verified · half-hourly · p/kWh inc VAT · no key
`https://api.octopus.energy/v1/products/AGILE-24-10-01/electricity-tariffs/E-1R-AGILE-24-10-01-C/standard-unit-rates/?period_from=...&period_to=...`
Region letter A to P (C = London). Fields `valid_from, valid_to, value_inc_vat`. Derived from the day-ahead price with a cap, so the shape matches APX but the level is retail. Pair with an export tariff (Outgoing Agile) for a V2G or home-battery version of the same loop.

## Notes for whoever wires one in

- Keep `settlement_date` and `period` so `battery.SPLITS` keeps working; derive `period` from local time, 1 = 23:00 UTC previous day for GB, or redefine for the market.
- Drop partial edge days and interpolate untraded periods the way `fetch_prices.py` does, so the simulator never sees a gap.
- Re-run `baselines.py` first: the oracle per day changes a lot between markets, so compare % of perfect, not £.
