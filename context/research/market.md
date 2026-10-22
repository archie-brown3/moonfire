# Market numbers: GB battery dispatch optimisation

Research date: 2026-10-22. Most figures come from Modo Energy's free article summaries; the full articles are paywalled.
**[est]** marks our own arithmetic or inference. Anything not found is marked as a gap.

## 1. GB installed BESS capacity and pipeline

| Figure | Value | Source (date) |
|---|---|---|
| Fleet, end Q3 2026 | **~8.5 GW / 14.4 GWh** | [Modo Q3 2026 buildout](https://modoenergy.com/research/en/gb-bess-buildout-q3-2026-great-britain-battery-energy-storage-record-quarter-coalburn) (Oct 2026) |
| Added in Q3 2026 | 917 MW / 1,844 MWh, a record quarter; largest site Coalburn 1 at 500 MW | same |
| Fleet, Q1 2026 | 7.2 GW / 11.8 GWh | [Modo Q1 2026 buildout](https://modoenergy.com/research/gb-bess-buildout-q1-2026-great-britain-battery-energy-storage-connections-reform) |
| Modo 2029 projection | 20 GW with connection delays (22.8 GW without); connections pipeline about 30 GW | same |
| NESO Clean Power 2030 need | **23–27 GW by 2030**, up from ~5 GW in 2023; needs 2.6–3.2 GW of new build a year | [ESS News](https://www.ess-news.com/?p=3053), [Current News](https://current-news.co.uk/neso-storage-necessary-uks-herculean-effort-meet-clean-power-2030-goals) (Nov 2024) |
| NESO connections reform | 7.6 GW of BESS given pre-2030 connection dates | [Energy Global](https://www.energyglobal.com/energy-storage/16042025/neso-reforms-to-see-76-gw-of-bess-given-pre-2030-connection-dates/amp/) (Apr 2025) |

## 2. GB BESS revenue (£/MW/year, Modo ME BESS GB index)

| Period | Total | Split / notes | Source |
|---|---|---|---|
| Jan 2024 | £36k | low point | [Modo Jan 2025 roundup](https://modoenergy.com/research/gb-research-roundup-january-2025-battery-energy-storage-great-britain-revenues-markets-wholesale-capacity-market-balancing-mechanism) |
| 2024 full year | ~£50k **[est]** | back-calculated from "2025 YTD (to May) £75k = 50% above 2024"; a Modo Q3 2025 piece says ~£51k | [Modo May 2025](https://modoenergy.com/research/me-bess-gb-battery-energy-storage-revenues-may-2025-balancing-mechanism), [Modo Q3 2025 derisking](https://modoenergy.com/research/gb-battery-energy-storage-derisking-returns-revenues-great-britain-offtake-ldes-p462-q3-2025) |
| Jan 2025 | £88k | two-year high; wholesale +£11.6k | Jan 2025 roundup |
| H1 2025 | **£69k** (excl. Capacity Market) | top systems above **£100k** | [Modo H1 2025](https://modoenergy.com/research/en/gb-bess-revenues-battery-energy-storage-balancing-mechanism-wholesale-h1-2025-tclc) |
| Jul 2025 | £55k | 2025 low point before December | [Modo Nov 2025](https://modoenergy.com/research/en/me-bess-gb-battery-energy-storage-revenues-november-2025-balancing-mechanism-gas-wind) |
| Oct 2025 | £77k | FR £30k; wholesale −12% m/m; BM flat | [Modo Oct 2025](https://modoenergy.com/research/battery-energy-storage-revenues-gb-october-2025-record-balancing-mechanism-dispatch-rates) |
| Nov 2025 | £59k | FR £23k (−22%); wholesale and BM lowest since Feb 2024 | Modo Nov 2025 |
| Dec 2025 | £47k | −45% y/y against £86k in Dec 2024; FR −£8.6k and BM −£3.2k m/m | [Modo Dec 2025](https://modoenergy.com/research/me-bess-gb-battery-energy-storage-revenues-december-2025-low-demand-christmas) |
| 2025 full year | **not found**; monthly range £47k–£88k, likely ~£65k **[est]** | | |
| Aug 2026 | £57k | wholesale £44k (highest since Sep 2021); BM **−£17k** (record low) | [Modo Aug 2026](https://modoenergy.com/research/en/gb-bess-revenues-august-2026-balancing-mechanism-offer-dispatch-rate-skips) |
| **Sep 2026** | **£99k** | **wholesale £68k (index record)**, FR £28k, BM −£8k, imbalance £2k, reserve £3k, CM £6k; 2-hour index £104k; top-10 assets at least ~£136k; best (Hyde) £148k excl. CM | [Modo Sep 2026](https://modoenergy.com/research/en/gb-bess-revenues-september-2026-wholesale-record-gas-wind-spreads) |

A negative BM figure means batteries charge on BM bids and then sell the energy in wholesale, so revenue booked as "wholesale" partly depends on BM positioning.

**LCP Delta and Cornwall Insight:** I found no free figures in the time available (gap).

## 3. Optimiser fee / revenue share

- **I found no published percentage.** The contract structures are documented:
  - Fees "can be based on a percentage of gross or net revenues"; [Modo, Choosing an optimiser pt 2](https://modoenergy.com/research/choosing-optimiser-part-two-tendering-questions) (Aug 2021).
  - Revenue-share deals are in use, for example Low Carbon's 95 MW with Habitat, Flexitricity and EDF; [Energy-Storage.news](https://energy-storage.news/uks-low-carbon-signs-revenue-share-deals-with-optimisers-for-95w-of-bess) (Jan 2024).
  - Under a **toll**, the optimiser earns nothing from the contract itself and profits only from trading above the toll level. Gresham House and Octopus agreed a 568 MW, 2-year toll at about **£57k/MW/yr** (Modo estimate); [Modo](https://modoenergy.com/research/battery-tolling-announced-gresham-house-octopus-energy-june-2024) (Jun 2024).
  - **Floors:** Gresham House has EDF floors running more than 10 years, and contracted revenue rose to £23.8m from £11.5m; [QuotedData](https://quoteddata.com/2026/04/gresham-house-energy-storage-excited-as-trial-points-to-significant-rise-in-alternative-revenues/) (Apr 2026).
  - Tesla Autobidder at Bouldercombe uses a fixed payment plus a floating revenue share, with a minimum revenue guarantee for 8 years; the percentage is undisclosed. [Genex](https://genexpower.com.au/genex-power-signs-offtake-agreement-with-tesla)
- Industry folklore puts revenue shares at **~5–15%**. **[est, unsourced; do not cite as fact]**

## 4. Capture rate and the spread between optimisers

- **GB, H1 2025:** top systems earned **>£100k against a £69k average**, which Modo headlines as "30%+ higher"; the stated figures imply ~45% **[est]**. Modo attributes the gap mainly to trading strategy: the top batteries "aren't cycling harder – they're trading smarter". Jamesfield 2 cycled 15% less than the lowest earner. [Modo H1 2025](https://modoenergy.com/research/en/gb-bess-revenues-battery-energy-storage-balancing-mechanism-wholesale-h1-2025-tclc)
- **GB, Sep 2026:** best asset £148k against the £104k 2-hour index, **+42%** **[est from stated figures]**. [Modo Sep 2026](https://modoenergy.com/research/en/gb-bess-revenues-september-2026-wholesale-record-gas-wind-spreads)
- **GB, 2021:** Reserve from Storage trial optimisers beat the fleet average by 55%. Modo cautions that much of the variation is outside the optimiser's control (availability, market timing, network charges). [Modo 2021](https://modoenergy.com/research/choosing-optimiser-part-two-tendering-questions)
- **NEM, Q2 2025:** capture rates "varied highly, even for similar batteries". Outages cost the worst-hit assets more than half of their potential revenue, and location (MLFs and constraints) cost up to 20%. Modo also finds that merchant or revenue-share contracts outperform fixed-revenue contracts. The numbers are paywalled. [Modo NEM Q2 2025](https://modoenergy.com/research/australia-nem-battery-energy-storage-optimisers-revenues-q2-2025-adjusted-capture-rate)
- **Percent of perfect foresight (Germany; no GB figure found):**
  - Day-ahead forecast-driven dispatch captured **90.7%** of the maximum; [Electricity Maps](https://www.electricitymaps.com/resources/publications/bess-forecast-accuracy-day-ahead-revenue-capture).
  - Re-Twin backtest on Jan–Mar 2026: **87.4%** with a good forecast against **78.4%** with a previous-day naive baseline, a **9-point gap from forecast and policy quality alone**; [Electricity Maps case study](https://www.electricitymaps.com/resources/case-studies/re-twin-energy-measures-how-much-a-better-day-ahead-forecast-is-worth-to-a-battery).
  - Continuous intraday: ~89% of perfect foresight (~11% below); [arXiv 2501.07121](https://arxiv.org/abs/2501.07121v2).
- Arenko claims its batteries earned 8% more than the closest competing optimiser (vendor claim); [Modern Power Systems](https://www.modernpowersystems.com:443/features/featurearenkos-optimal-performance-10696371).

## 5. Revenue mix: wholesale vs frequency response since 2023

- **Dec 2022:** wholesale overtook Dynamic Containment for the first time, 38% against 28% of fleet revenue, as frequency response saturated. [Modo Q4 2022](https://modoenergy.com/research/battery-energy-storage-key-trends-q4-2022)
- **2023:** "frequency response services saturated"; the revenue stack shifted to wholesale and the BM. [Modo 2024 review](https://modoenergy.com/research/gb-battery-energy-storage-markets-2024-year-in-review-great-britain-wholesale-balancing-mechanism-frequency-response-reserve)
- **2024:** monthly FR fell as low as £5–8k against wholesale at £13–15k (Mar and May 2024). [Modo Mar 2024](https://modoenergy.com/research/gb-benchmark-index-battery-energy-storage-march-2024-revenue)
- **Late 2025:** FR rebounded to £23–30k and drove most of the swings.
- **Sep 2026:** wholesale was **£68k of £99k, about 69%** **[est from the stated split]**, against FR at £28k (~28%). Wholesale plus BM net (£60k) is ~61%. That is the highest wholesale share on record.
- **Takeaway:** energy trading (wholesale + BM) is now the largest and most optimiser-sensitive part of GB BESS revenue. Frequency response is a commoditised, saturating floor.

## 6. ERCOT and NEM headlines

- **ERCOT:** 2025 was about **$29–30/kW-yr** (Modo Nowcast), against **$56/kW in 2024** and **$193/kW in 2023**. The fall came from mild weather plus ancillary-service saturation and compressed arbitrage spreads. RTC+B went live on 5 Dec 2025. [Modo ERCOT 2025](https://modoenergy.com/research/why-were-ercot-battery-revenues-so-low-in-2025-weather-energy-arbitrage-builodout), [Modo Nov 2025](https://modoenergy.com/research/ercot-battery-revenue-benchmark-november-2025-battery-energy-storage-bess-capture-rates)
- **NEM:** monthly fleet averages ran from A$62k (Dec 2025, lowest since Mar 2024) to A$94k/MW/yr (May 2025). The trailing 12-month average was **A$135–141k/MW/yr** (Oct–Nov 2025 reports). Energy trading is the largest stream. [Modo NEM Oct 2025](https://modoenergy.com/research/australia-nem-battery-energy-storage-revenues-benchmark-october-2025-queensland-fcas-volatility), [Modo NEM Dec 2025](https://modoenergy.com/research/australia-nem-battery-energy-storage-revenues-december-2025-price-volatility)

## Pitch arithmetic [all est]

- GB fleet revenue ≈ 8.5 GW × ~£65k ≈ **~£550m/yr**. That is likely to keep rising toward 20–27 GW by 2029–30, so **~£1.3–1.8bn/yr** at similar unit revenue.
- Each **1 percentage point** of capture on today's fleet is worth ~£5.5m/yr. For a single 100 MW site at £65k/MW/yr, 1% is **£65k/yr**.
- The gap between the best GB asset and the index average is **30–45%**, so dispatch-policy quality is worth tens of £k per MW per year.

## Gaps
- No GB percent-of-perfect-foresight figure, and no median-optimiser figure.
- No published optimiser fee percentage.
- No LCP Delta or Cornwall Insight numbers.
- No official 2025 full-year GB average.
