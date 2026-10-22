# Battery dispatch optimisers: competitive scan

Researched 2026-10-22 over about 10 minutes, using web search plus a few page fetches. Most figures are vendor claims. **[unverified]** marks anything that rests on a single vendor or secondary source, or where I couldn't open the primary page. None of the vendors publishes a revenue-share %.

## Summary table

| Product | Customer | Commercial model (found) | Dispatch approach (as described) | Uplift / capture claims | Continuous improvement or backtesting |
|---|---|---|---|---|---|
| Tesla Autobidder | Utility-scale BESS owners (e.g. Neoen Hornsdale, Genex Bouldercombe) | Managed offtake with **fixed + floating revenue share** (Genex), then a **licence** after year 8. No % disclosed | Statistics + ML + numerical optimisation; price/load/generation forecasting; human-set parameters for the trading desk; maximises asset NPV including warranty costs | "$330M+ trading profit to early investors" (2023, Tesla exec) **[unverified]** | Not described |
| Kraken Flex (Octopus / Kraken) | BESS owners and funds (Gresham House, Low Carbon) | **Toll**: Octopus paid a fixed £/MW for Gresham's 568 MW over 2 years (~£57k/MW/yr per Modo). Also acts as a **dispatch/control partner** alongside other optimisers | "AI and ML" to charge on renewable surplus and discharge under grid stress | None found | Not described |
| Habitat Energy (Quinbrook) | BESS funds and developers, UK/US/AU | **Revenue share** (Low Carbon deal). No % disclosed | ML forecasts + **convex optimisation** + human trading desk; **marginal degradation cost** in each dispatch decision | Top UK optimiser per LCP Enact ranking (vendor-cited); "up to 2x revenue/MW vs competitors" **[unverified]** | Job ads mention building **backtesting frameworks** and research environments, and productionising convex models |
| Flexitricity (Drax) | BESS and flexible C&I assets | Single contract; onboarding, settlement and billing "included in our fee". Revenue share with Low Carbon | Stacks frequency response, wholesale, BM, reserve, NIV-chasing, DSO and Capacity Market | None found | Not described |
| Arenko (Nimbus) | Asset owners who trade in-house or want software (Gresham House, Ørsted, RWE, ENGIE, Vattenfall) | **Enterprise SaaS** (pricing not public) | Optimisation engine "reasons strategies" across markets and timescales; microservices | ~1.2 GW under management **[company claim]** | Not described |
| Fluence Mosaic | Utility-scale storage and renewables in NEM, CAISO, ERCOT | Software (bidding SaaS); terms not found | "Intelligent bidding": ML forecasts, **re-optimises at every opportunity**, co-optimises DA/RT and FCAS | +50% vs CAISO average (summer 2025), +$3M; 12-month +43.5% $/kW-month vs benchmark **[vendor]** | Experts review results **daily** and feed them back into the product; models are "never finished". No backtest described |
| Gridmatic | ERCOT/CAISO BESS owners | **Guaranteed floor + shared upside**; $50M fund signs multi-year offtakes | ML price forecasts from weather and grid data drive dispatch across energy and ancillary streams | ERCOT fleet earned **51% of theoretical potential** in 2022; its backtest reached **~75%** (+46%). 2023: +32% backtested. H1 2024: $113/kW-yr vs $70 market avg (+61%) **[vendor]** | Annual reports built on **backtests**; faces criticism as a "black box" |
| EDF PowerShift | UK BESS owners (Gresham House, Eelpower, Trinasolar, Ganfeng) | Optimisation agreements, often long-term; terms not found | Modelling, real-time analytics, "AI and algorithms" plus a 24/7 trading desk across ancillary, wholesale and BM | "UK's largest optimiser, ~20% of UK battery market" **[vendor]** | Not described |
| enspired | European BESS owners (12 countries; ~1 GW live) | Optimiser/trader; terms not found | In-house automated trading using **ML and reinforcement learning**; uses cell-level health data (Volytica) to stay inside warranty | Cross-market gives 2.5x wholesale-only; up to €180k/MW/yr simulated in northern Italy **[vendor simulation]** | "Fast adjustment to market changes" (in-house platform); no detail |
| Axle Energy | OEMs and suppliers with **domestic** flexibility (EVs, home batteries, heat pumps) | Platform/aggregator; terms not found | Shifts household load to cheap or low-carbon periods; DFS integration (Octopus, British Gas) | ~15k assets / 85 MW **[secondary]** | Not described. **Not a grid-scale BESS competitor** |

## Market structure (GB)

- Common GB contract types are **floors** (the optimiser tops up revenue below an agreed level in return for a higher fee), **tolls** (a fixed £/MW payment; the optimiser keeps the trading P&L) and **revenue/profit share**. Modo publishes no typical % figures. Sources: [Modo offtake Q3 2025](https://modoenergy.com/research/gb-battery-energy-storage-derisking-returns-revenues-great-britain-offtake-ldes-p462-q3-2025), [Modo on Gresham/Octopus toll](https://modoenergy.com/research/battery-tolling-announced-gresham-house-octopus-energy-june-2024).
- Owners run **several optimisers at once** and audit them independently: Low Carbon split 95 MW across Habitat, Flexitricity and EDF, with KrakenFlex as dispatch/controls partner "to carry out independent revenue and dispatch checks". Source: [newpower](https://www.newpower.info/?p=13048).
- **Benchmarking is inconsistent.** Modo notes that optimisers compare themselves to "a theoretical perfect battery, or run a back-test and pick the best result". Modo applies a **15–25% haircut** to its perfect-knowledge GB model, and an **80% calibration factor** in Germany, to match realised revenue. That implies realised capture of about **75–85% of a perfect-foresight model** (this is a Modo calibration figure, not a per-optimiser one). Sources: [Modo model calibration](https://docs.modoenergy.com/pages/jan-2026/uk-europe/gb/model-calibration), [Modo Gridmatic case study](https://modoenergy.com/customers/gridmatic).

## Per-product notes and sources

### Tesla Autobidder
- Described as a real-time trading and control platform. It runs numerical optimisation using parameters a human operator sets, and maximises NPV after counting warranty and maintenance costs. It is built from "classical statistics, machine learning and numerical optimisation", with price, load and generation forecasting, dispatch optimisation and smart bidding. Runs Hornsdale (Neoen). **The tesla.com support page returned 403 to my fetch, so this comes from search snippets of that page [partly unverified].** https://www.tesla.com/support/autobidder, https://www.tesla.com/en_GB/support/autobidder
- Genex Bouldercombe: an offtake with a **fixed component (gives lenders certainty) plus a floating revenue share**, converting to an Autobidder **licence after 8 years**. https://genexpower.com.au/genex-power-signs-offtake-agreement-with-tesla
- "$330M trading profit" claim: https://electrek.co/2023/09/15/tesla-autobidder-product-330-million-energy-investors/, https://driveteslacanada.ca/energy/teslas-autobidder-software-surpasses-330-million-in-profits-for-energy-investors/
- 2020 launch: https://electrek.co/2020/05/03/tesla-autobidder-new-product-electric-utility/

### Kraken Flex
- Gresham House toll: https://octopus.energy/press/Octopus-energy-Gresham-House/
- Low Carbon dispatch partner: https://www.newpower.info/?p=13048
- Hydro REIN partnership: https://octopus.energy/press/hydro-rein-and-krakenflex-partner-on-energy-flexibility-rollout/
- Italy co-located deal (dated Aug 2026) **[verify]**: https://www.blackridgeresearch.com/news-releases/recurrent-energy-and-octopus-energy-strike-italys-first-co-located-battery-optimization-deal-using-kraken-ai-platform
- Kraken spin-off from Octopus (~$8.65B valuation) **[secondary, unverified]**: https://www.cleanthinking.de/?p=1065029

### Habitat Energy
- Services (PowerIQ, degradation modelling): https://quinbrook.com/?p=2503
- Ben Irons on the trade-off: running for bigger spreads may give up ~10% of revenue but extend life by 50%+ **[via search snippet]**: https://theenergyst.com/?p=9408
- Williamsdale 250 MW/500 MWh "Evolve" service (AI forecasting, algorithmic trading, local team): https://reneweconomy.com.au/uk-provider-chosen-to-optimise-500mwh-canberra-battery-with-unique-revenue-sharing-deal/
- US expansion: https://energy-storage.news/quinbrooks-uk-bess-optimiser-habitat-energy-furthers-us-expansion-with-texas-deals
- ML Ops job ad (backtesting frameworks, convex optimisation): https://startup.jobs/ml-ops-engineer-habitat-energy-8021549

### Flexitricity
- Service stack: https://flexitricity.com/services/battery-energy-storage-systems
- Anesco partnership: https://flexitricity.com/resources/press-release/flexitricity-partners-anesco-dynamically-optimise-battery-assets
- Drax acquisition: https://cornwall-insight.com/projects-won/projects-won/cornwall-insight-advises-drax-on-flexitricity-purchase-as-company-continues-to-expand-its-flexibility-capability

### Arenko (Nimbus)
- https://arenko.group/optimisation
- Ørsted Carnegie Road: https://arenko.group/arenko-secures-new-contract-win-with-leading-renewable-energy-developer-orsted/
- Gresham House software deal: https://arenko.group/arenko-group-and-gresham-house-expand-relationship-with-an-asset-management-software-deal/
- Modo podcast (1.2 GW): https://arenko.group/modo-energy-podcast-how-arenko-is-building-the-digital-backbone-of-energy-storage/

### Fluence Mosaic
- Blog with the continuous re-optimisation claim, daily expert review and CAISO uplift: https://blog.fluenceenergy.com/beating-bidding-benchmark-evolving-energy-storage
- Product page: https://fluenceenergy.com/energy-bidding-software/
- 10-K (originated in the AMS acquisition; 13.7 GW in 2022): https://www.sec.gov/Archives/edgar/data/1868941/000186894122000120/flnc-20220930.htm
- Gentari NEM deployment: https://energy-storage.news/gentari-picks-fluences-optimisation-platform-for-172mw-408mwh-hybrid-solar-storage-project-in-australia

### Gridmatic
- 2022 report (51% of theoretical, backtest ~75%): https://www.businesswire.com/news/home/20230518005222/en/5454811/Gridmatic-Releases-2022-Annual-Energy-Storage-Report
- 2023 report (+32%; the article does not define what "potential" means): https://www.latitudemedia.com/news/ercots-battery-owners-lost-out-on-32-of-potential-revenue-in-2023
- 1 GWh milestone (+61% H1 2024, floor + upside): https://www.businesswire.com/news/home/20241210579395/en/Gridmatic-Surpasses-1GWh-of-Energy-Storage-Under-Management-and-Sees-Major-Growth-in-Retail-Business
- $50M fund: https://www.businesswire.com/news/home/20231115697337/en/Gridmatic-Closes-%2450-Million-Energy-Storage-Fund-Underscoring-Importance-of-AI-to-Optimizing-Batteries
- "Black box" criticism: https://energy-storage.news/gridmatic-on-black-box-ai-optimisation-criticism-results-will-speak-for-themselves-over-time

### EDF PowerShift
- https://energy-storage.news/edf-determined-to-play-major-role-in-uk-flexibility-as-it-signs-50mw-battery-optimisation-deal
- Trinasolar deal (2026): https://www.solarpowerportal.co.uk/energy-storage/edf-signs-battery-optimisation-agreement-with-trinasolar-for-179-8mwh-of-uk-bess
- Ganfeng Kintore: https://www.solarpowerportal.co.uk/energy-storage/edf-to-optimise-chinese-lithium-giant-ganfeng-s-160mwh-kintore-battery-storage-system

### enspired
- Volytica partnership: https://www.energyglobal.com/energy-storage/29012025/volytica-diagnostics-partners-with-enspired-to-strengthen-bess-trading/amp/
- Italy entry and simulation: https://www.enspired-trading.com/press-releases/enspired-enters-italy-in-partnership-with-energreen-trading
- Revenue transparency initiatives: https://www.review-energy.com/almacenamiento/leading-bess-optimizer-enspired-returns-to-intersolar-with-industry-defining-revenue-transparency-and-battery-longevity-initiatives

### Axle Energy
- https://current-news.co.uk/current±-disrupters-axle-on-unlocking-assets-via-energy-flexibility-platforms

## Implications for our platform

1. **No vendor publishes a reproducible percent-of-perfect-foresight score.** Gridmatic comes closest (51% to ~75% of "theoretical"), and Modo says the claims can't be compared because each optimiser picks its own benchmark or its best backtest. A fixed evaluator with a walk-forward split, a held-out test window and an LP-oracle denominator is the credible version of the same pitch.
2. **Owners already run several optimisers and audit them** (Low Carbon). A champion/challenger gate, with every policy change arriving as a reviewable PR, fits the way they already check optimisers against each other.
3. **Improvement today depends on humans:** daily expert review at Fluence, a trading desk at Habitat and EDF, operator-set parameters at Tesla. Habitat builds backtesting tooling, but nobody describes an automated search loop that rewrites the dispatch rule and is gated out-of-sample. That is the gap.
4. **Revenue-share and floor contracts mean the optimiser's fee grows with captured revenue.** Each point of foresight capture is the optimiser's own margin, which makes this a buyer for our tool, as well as a selling point to asset owners.
5. **Honest scope gap:** every competitor stacks ancillary services, BM, intraday and degradation-aware dispatch. We model wholesale arbitrage only, with a flat £/MWh degradation cost.
