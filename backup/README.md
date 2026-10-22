# Backup: alternative pipeline built in parallel (Ekjot, 22 Oct 2026)

Not part of the submission. Kept on the `backup-ekjot` branch in case anything on `main` breaks.

`slowpoke/` is a second autoresearch pipeline with the same shape as the main repo
(one editable file, sealed evaluator, archive, commit-or-revert loop, live dashboard):

- `problem/policy.py` + `evaluator/score.py`: EV vehicle-to-grid battery, 60 kWh, year of half-hourly prices,
  morning-charge constraint, wear cost, export haircut. Score = negative annual profit in pounds.
- `loop/run.py`: Claude-driven propose / score / archive / commit-or-revert loop with parent selection.
- `dashboard/index.html`: live chart of results.tsv, kept vs reverted.
- `data/make_prices.py`: synthetic UK-shaped prices. `data/from_octopus.py`: real Octopus Agile prices.
- `tracks/`: the earlier covariance-estimator version (portfolio risk) of the same architecture.

Tested end to end with mocked proposals; the live Claude call needs ANTHROPIC_API_KEY.
