// Figures transcribed from context/research/*.md (researched 2026-10-22). `est` marks our own arithmetic.

export const revenueIndex = [
  { month: "Jan 24", gbp_k: 36, note: "low point" },
  { month: "2024", gbp_k: 50, note: "full year, est" },
  { month: "Jan 25", gbp_k: 88, note: "two-year high" },
  { month: "H1 25", gbp_k: 69, note: "excl. Capacity Market" },
  { month: "Jul 25", gbp_k: 55, note: "2025 low" },
  { month: "Oct 25", gbp_k: 77, note: "FR £30k" },
  { month: "Nov 25", gbp_k: 59, note: "FR down 22%" },
  { month: "Dec 25", gbp_k: 47, note: "down 45% y/y" },
  { month: "Aug 26", gbp_k: 57, note: "BM record low, −£17k" },
  { month: "Sep 26", gbp_k: 99, note: "wholesale record £68k" },
];

export const revenueMixSep26 = [
  { stream: "Wholesale", gbp_k: 68 },
  { stream: "Frequency response", gbp_k: 28 },
  { stream: "Capacity Market", gbp_k: 6 },
  { stream: "Reserve", gbp_k: 3 },
  { stream: "Imbalance", gbp_k: 2 },
  { stream: "Balancing Mechanism", gbp_k: -8 },
];

export const fleet = [
  { label: "2023", gw: 5, kind: "actual" },
  { label: "Q1 26", gw: 7.2, kind: "actual" },
  { label: "Q3 26", gw: 8.5, kind: "actual" },
  { label: "2029", gw: 20, kind: "projection" },
  { label: "2030 lo", gw: 23, kind: "projection" },
  { label: "2030 hi", gw: 27, kind: "projection" },
];

export const captureBenchmarks = [
  { label: "Real NEM optimisers (low)", pct: 60, source: "Infradebt" },
  { label: "Real NEM optimisers (high)", pct: 80, source: "Infradebt" },
  { label: "Modo GB calibration (low)", pct: 75, source: "Modo" },
  { label: "Modo GB calibration (high)", pct: 85, source: "Modo" },
  { label: "Naive day-ahead, DE", pct: 78.4, source: "Electricity Maps" },
  { label: "Good day-ahead forecast, DE", pct: 87.4, source: "Electricity Maps" },
  { label: "Continuous intraday", pct: 89, source: "arXiv 2501.07121" },
  { label: "Day-ahead forecast dispatch, DE", pct: 90.7, source: "Electricity Maps" },
];

export const competitors = [
  { name: "Tesla Autobidder", model: "Fixed + floating revenue share, licence after year 8", approach: "Stats + ML + numerical optimisation; human-set parameters", claim: "$330M+ trading profit (2023)", loop: "Not described" },
  { name: "Kraken Flex (Octopus)", model: "Toll, ~£57k/MW/yr (Gresham House)", approach: "AI/ML charge on surplus, discharge under stress", claim: "None found", loop: "Not described" },
  { name: "Habitat Energy", model: "Revenue share", approach: "ML forecasts + convex optimisation + trading desk; marginal degradation cost", claim: "Up to 2x revenue/MW (unverified)", loop: "Builds backtesting frameworks (job ads)" },
  { name: "Flexitricity (Drax)", model: "Revenue share, single contract", approach: "Stacks FR, wholesale, BM, reserve, DSO, CM", claim: "None found", loop: "Not described" },
  { name: "Arenko (Nimbus)", model: "Enterprise SaaS", approach: "Optimisation engine across markets", claim: "~1.2 GW managed", loop: "Not described" },
  { name: "Fluence Mosaic", model: "Bidding SaaS", approach: "ML forecasts, re-optimises every opportunity", claim: "+43.5% vs benchmark (vendor)", loop: "Daily expert review; no backtest described" },
  { name: "Gridmatic", model: "Guaranteed floor + shared upside", approach: "ML price forecasts from weather and grid", claim: "51% of potential (fleet) vs ~75% backtest", loop: "Annual backtest reports; 'black box' criticism" },
  { name: "EDF PowerShift", model: "Long-term optimisation agreements", approach: "Analytics + 24/7 trading desk", claim: "~20% of UK market (vendor)", loop: "Not described" },
  { name: "enspired", model: "Optimiser/trader", approach: "ML + reinforcement learning; cell-level health data", claim: "Cross-market 2.5x wholesale-only (sim)", loop: "'Fast adjustment'; no detail" },
];

export const pitfalls = [
  { pitfall: "Perfect foresight overstates what is achievable; real optimisers reach 60 to 80%", design: "Report % of perfect as secondary; headline is £/MW/day with bootstrap CI" },
  { pitfall: "Regime shifts between quarters; parameters need re-tuning at least quarterly", design: "Walk-forward time splits; the loop is cheap enough to re-run on a schedule" },
  { pitfall: "A backtest without a throughput cost rewards over-cycling", design: "£10/MWh degradation charged on every MWh moved; cycles reported beside revenue" },
  { pitfall: "Index prices are not achievable order-book prices", design: "Stated simplification: APX market index, price-taker assumption" },
  { pitfall: "Backtest overfitting and p-hacking from search", design: "Loop sees train only; gate promotes on val; test is read once by the gate" },
  { pitfall: "Lookahead leakage", design: "Policy receives only strictly past prices; literal dates and non-math imports score zero" },
];

export const workflowSteps = [
  { step: "1. Quant forms a hypothesis", automated: false },
  { step: "2. Edit strategy code or parameters", automated: true },
  { step: "3. Run backtest or revenue simulation", automated: true },
  { step: "4. Compare to incumbent and perfect foresight", automated: true },
  { step: "5. Hand to live trading and P&L attribution", automated: false },
];

export const judging = [
  { criterion: "Commercial value and relevance of the use case", weight: 20 },
  { criterion: "Technical design, implementation and originality", weight: 20 },
  { criterion: "Evaluation and evidence", weight: 20 },
  { criterion: "Deployment feasibility, generalisability and interoperability", weight: 20 },
  { criterion: "Ease of use and communication", weight: 20 },
];

export const pitchArithmetic = [
  { label: "GB fleet revenue today", value: "~£550m/yr", basis: "8.5 GW × ~£65k/MW/yr, est" },
  { label: "By 2029 to 2030", value: "£1.3 to 1.8bn/yr", basis: "20 to 27 GW at similar unit revenue, est" },
  { label: "One capture point, GB fleet", value: "~£5.5m/yr", basis: "est" },
  { label: "One capture point, 100 MW site", value: "£65k/yr", basis: "est" },
  { label: "Best asset vs index", value: "+30 to 45%", basis: "Modo H1 2025 and Sep 2026" },
];
