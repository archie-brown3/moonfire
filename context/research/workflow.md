# Battery-optimiser strategy workflow: research notes

Collected 2026-10-22 in about 10 minutes, for the Moonfire hack. Confidence key: **[read]** means I opened the page. **[snippet]** means only a search-result snippet was seen; the page failed to load or I didn't open it. Vendor numbers are self-reported.

## 1. How optimiser firms describe their workflow

| Firm | What's public | Source |
|---|---|---|
| Tesla Autobidder | A library of algorithms for price, load and generation forecasting, dispatch optimisation and smart bidding. Methods include "classical statistics, machine learning and numerical optimization", and the algorithms "continuously improve through experiential data". Tesla describes no backtesting process. | [tesla.com/support/autobidder](https://www.tesla.com/support/energy/tesla-software/autobidder) [snippet] |
| Tesla Autobidder (job ad) | A Senior Quant/Trading Analyst role in Berlin whose duties include "simulations and backtesting to validate strategies". | [heyjobs listing](https://www.heyjobs.co/en-de/jobs/bd5b4323-df45-4806-bf65-56fea2f228f8) [snippet; the page didn't render] |
| Habitat Energy | ML and algorithmic forecasting plus optimisation, run by an in-house trading team. A role covers building "backtesting frameworks, and research environments". The platform is called PowerIQ. | [startup.jobs ML Ops](https://startup.jobs/ml-ops-engineer-habitat-energy-8021540), [NS Energy](https://www.nsenergybusiness.com/news/habitat-energy-wins-40mw-battery-storage-deal-with-arlington-energy/) [snippet] |
| Gridmatic | Backtesting is used as the sales metric: "up to 46%" revenue boost (ERCOT 2022 backtest), later "up to 32%" (2024 report). The baselines are not disclosed. | [BusinessWire 2023](https://www.businesswire.com/news/home/20231115697337/en/Gridmatic-Closes-%2450-Million-Energy-Storage-Fund-Underscoring-Importance-of-AI-to-Optimizing-Batteries) [snippet] |
| Arenko | A pure software optimiser trading the BM, frequency response and EPEX intraday. It claims "double the return of the nearest competitor" in the BM. | [Current± interview](https://current-news.co.uk/a-pure-play-software-company-arenkos-rupert-newland-on-flexibility-and-the-new-battery-markets) [snippet] |
| Enspired | "Own algorithms … fully automated intraday trading". | [Modo contact list](https://modoenergy.com/research/es/battery-energy-storage-optimizers-contact-list-gb) [snippet] |
| Kraken, Flexitricity, Modo (as an optimiser) | Nothing found in this time box. | n/a |

Peer job ads describe the same human workflow:
- **YUSO**, Quant Analyst, Flex Optimisation: "Build backtesting and parameter-optimisation pipelines, improve forecasting and ML models, support revenue simulations". [greenhouse](https://job-boards.eu.greenhouse.io/yuso/jobs/4947532101) [snippet]
- **Entrix**, Staff Quant Researcher: owns the pipeline "from signal research and backtesting through to live trading and P&L attribution". [personio](https://entrix.jobs.personio.com/job/2685705) [snippet]
- **Axpo**, battery optimisation intern: "creating a backtesting framework for assessing revenues for a given bidding strategy". [axpo](https://careers.axpo.com/jobs/6529713-intern-battery-optimisation-f-m-d) [snippet]
- **Alpiq**, Senior BESS Quant: "Model battery degradation, efficiency losses, and operational constraints". [alpiq](https://www.alpiq.com/career/open-jobs/your-application/9540) [snippet]

**Synthesis.** The human loop runs in four steps:
1. A quant forms a hypothesis about a strategy or parameter change.
2. They edit the strategy code or parameters.
3. They run an in-house backtest or revenue simulation.
4. They compare the result to the incumbent strategy and perfect foresight, then hand over to live trading and P&L attribution.

Our loop automates steps 2 and 3 plus the comparison in step 4: the "backtesting and parameter-optimisation pipeline" step.

**Update cadence.** None of the firms publish one. The only explicit recommendation found is WattClarity's: review and update arbitrage control parameters "on at least a quarterly basis" ([WattClarity 2021](https://wattclarity.com.au/articles/2021/03/spot-price-arbitrage-with-battery-storage-a-review-of-2020-performance/) [read]). Tesla only says the algorithms "continuously improve".

## 2. Open-source dispatch and backtesting tools

There is no established, widely used open-source BESS backtester with a built-in perfect-foresight benchmark. What exists is research code:
- **Weber and Lu (Energies 2024):** an open-source MILP arbitrage model with price bands that compares imperfect and perfect forecasts. [ANU](https://researchportalplus.anu.edu.au/en/publications/an-open-source-energy-arbitrage-model-involving-price-bands-for-r/) [snippet]
- **arXiv 2509.21337:** a Python backtest engine for cross-market (day-ahead plus intraday) BESS arbitrage on EPEX. It uses the ID1 index instead of the order book because of the "challenges associated with backtesting at the order book level", and includes a forecast-uncertainty sensitivity against a perfect-forecast case. [arXiv](https://arxiv.org/abs/2509.21337) [snippet]
- **pyBESS** on PyPI: "Energy Arbitrage for Battery Energy Storage Systems". Features unverified. [pypi](https://pypi.org/project/pybess/) [snippet]
- **Matsumoto lab:** a hosted battery-operation simulator with an arbitrage backtest. [link](https://www.matsumoto-lab.isc.ens.isct.ac.jp/en/battery_sim) [snippet]
- **Modo's Global Dispatch Model:** a MILP with perfect foresight used for its simulated benchmarks. It is proprietary. [Modo SPP methodology](https://modoenergy.com/benchmarks/methodology/virtual-asset/spp) [snippet]

Our perfect-foresight LP oracle plus a walk-forward evaluator is therefore a small but real gap-filler.

## 3. LLM program search or evolutionary search applied to energy and trading

- **Evolving LLM-derived control policies for residential EV charging and V2G** ([arXiv 2602.07275](https://arxiv.org/html/2602.07275v1)) [read]. This is the closest prior work.
  - An LLM is used as a mutation operator in a "prompt-evaluation-repair" loop, framed as FunSearch- and AlphaEvolve-like.
  - It evolves a Python `decide_power(...)` that returns a signed power setpoint, scored by rollouts in the EV2Gym simulator on AEMO prices.
  - The hybrid policy reaches 118% of the rule-based baseline.
  - **It has no perfect-foresight baseline and no train/test split**: it is evaluated on the same window it was iterated on, and the authors list overfitting as future work.
  - That is exactly the gap our evaluator design closes.
- **MadEvolve: Evolutionary Optimization of Trading Systems with LLMs** ([arXiv 2605.23007](https://arxiv.org/abs/2605.23007)) [read: abstract only]. It applies AlphaEvolve-style evolution to Bitcoin trading strategies and feature pipelines, compares against Claude Code as an agentic searcher, and explicitly assesses **p-hacking risk**. It cites Bailey et al. 2014 on backtest overfitting.
- **OpenEvolve and AlphaEvolve** are frameworks only ([AlphaEvolve docs](https://docs.cloud.google.cn/gemini/enterprise/docs/alphaevolve/developer-guide/overview?hl=en)). I found no published application to grid-battery dispatch with real wholesale prices and a held-out promotion gate.

## 4. How optimisers are benchmarked (metric names)

- **"Percentage of Perfect" (PoP)** = actual revenue ÷ the maximum revenue under perfect foresight, back-tested on historical prices. [Infradebt](https://www.infradebt.com.au/post/percentage-of-perfect) [read]
  - Developers typically *assume* 80–90%.
  - Observed NEM optimisers come in at **60–80%**, with wide spread between optimisers.
  - Caveats: the price-taker assumption, contract-bound assets, and limited comparability across durations, sites and availability.
- **"Adjusted capture rate"** (Modo, NEM benchmark, May 2025). [Modo methodology](https://modoenergy.com/research/en/australia-nem-battery-energy-storage-optimisation-benchmark-may-2025-methodology) [read]
  - It compares actual revenue with "adjusted potential revenue".
  - Potential is the higher of **"trading potential"** (efficiency-adjusted spreads × duration, perfect foresight, 1 cycle/day) and **FCAS potential**.
  - Potential is then adjusted for marginal loss factors, network constraints, contracts and an **availability factor**.
  - Capture can exceed 100% through co-optimisation or by cycling more than once a day.
- **Modo GB (ME BESS GB index):** in GB, Modo doesn't simulate. It measures real BMU revenues (£/MW/year) from BM acceptances, ancillary contracts and metered volumes, with 1H and 2H sub-indices. Adding imbalance cut 2024 index revenue by **£662/MW/year**. Germany, Spain and the Netherlands use simulated "virtual assets" built with the MILP. [Modo GB methodology](https://modoenergy.com/methodology/gb), [Dec 2024 release](https://modoenergy.com/research/me-bess-gb-index-battery-energy-storage-product-release-december-2024/) [snippet]
- **WattClarity** uses "discount to perfect foresight" (31.8% for one QLD battery in 2020), **average captured spread** ($90/MWh actual vs $116/MWh under perfect foresight), spread as a multiple of the regional price, a **utilisation factor** (MWh/day vs the warranty limit), and income by price band. [read]

## 5. Pitfalls practitioners cite

1. **The perfect-foresight ceiling overstates what can be achieved.** Real optimisers reach 60–80% of perfect ([Infradebt](https://www.infradebt.com.au/post/percentage-of-perfect)). A day-ahead backtest with the best forecast reached 87.4% of perfect ([Electricity Maps / re.twin](https://www.electricitymaps.com/resources/case-studies/re-twin-energy-measures-how-much-a-better-day-ahead-forecast-is-worth-to-a-battery) [snippet]). Forecast noise collapses intraday revenue from 72 to 22.6 TEUR at +100% volatility ([arXiv 2509.21337](https://arxiv.org/abs/2509.21337) [snippet]). Implication for us: report % of perfect, and never let the policy see same-period prices.
2. **Regime shifts.** Income sources swing between quarters: in one quarter about 30% came from prices above $300/MWh, and in the next over a third came from negative prices. Control parameters need re-tuning at least quarterly ([WattClarity](https://wattclarity.com.au/articles/2021/03/spot-price-arbitrage-with-battery-storage-a-review-of-2020-performance/) [read]). This supports walk-forward splits and a scheduled re-search.
3. **Degradation accounting.** Including ageing costs moved missed revenue against the theoretical maximum from 28% to 85% (DFKI) ([dfki](https://www-live.dfki.de/web/forschung/projekte-publikationen/publikation/16172) [snippet]). Warranty throughput limits are cumulative ([WattClarity](https://wattclarity.com.au/articles/2021/03/spot-price-arbitrage-with-battery-storage-a-review-of-2020-performance/)). A backtest without a throughput cost rewards over-cycling.
4. **Which price you trade.** Modo's GB index changed materially once imbalance was included (−£662/MW/yr) ([Modo, Dec 2024](https://modoenergy.com/research/me-bess-gb-index-battery-energy-storage-product-release-december-2024/)). Backtests usually use an index price, such as ID1, not achievable order-book prices ([arXiv 2509.21337](https://arxiv.org/abs/2509.21337)). Our use of the GB market index price is a simplification of the same kind and must be stated.
5. **Backtest overfitting / p-hacking from search.** MadEvolve assesses p-hacking risk and cites Bailey et al. on backtest overfitting ([arXiv 2605.23007](https://arxiv.org/abs/2605.23007)). The EV/V2G LLM-evolution paper had no held-out split ([arXiv 2602.07275](https://arxiv.org/html/2602.07275v1)). This is the core argument for our val gate and the test set we touch only once.
6. **Price-taker assumption.** Market impact is ignored, and coordinated withholding would remove the very price spikes that perfect foresight assumes ([Infradebt](https://www.infradebt.com.au/post/percentage-of-perfect)).

## Gaps

- No first-party engineering blogs from Habitat, Kraken, Flexitricity, Modo or Tesla describing their backtest infrastructure or update cadence. Job ads are the best evidence.
- Gridmatic's uplift figures have undisclosed baselines.
- Several sources are snippet-only (see the confidence tags).
