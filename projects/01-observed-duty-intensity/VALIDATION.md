# Validation record

Prepared 22 October 2026. This record describes checks performed during preparation, not an independent audit of the original Census statistical release.

## Completed

- The archived source was filtered to imports for consumption, the three exact HTS10 codes, five partner codes, and January–August of each comparison year.
- Extraction returned 240 monthly observations, no duplicate monthly product–partner keys and eight months in every comparison cell.
- The included snapshot has exactly 30 unique product–partner–period combinations, complete expected coverage, matching country codes, positive import denominators and finite nonnegative numeric inputs.
- The period basis is explicitly an archived January–August monthly sum.
- The script uses decimal arithmetic and ratios of sums, with no averaging of monthly or product rates.
- A separate calculation in pandas recomputed all 30 duty-intensity ratios and the Mexico totals and growth, matching the script to floating-point tolerance. An independent review also checked all 30 gaps, ten country-period aggregates, three Mexico growth calculations and the input hash.
- Input values and labels were inspected; output tables are generated from the included data, not manually entered estimates.
- The input SHA256 in `results/results.json` and `sources.json` identifies the included snapshot.

## Not established by these checks

- A live Census refresh did not complete; current revised source values are not certified.
- The full upstream files were not rehashed in this workflow. The upstream hashes in `sources.json` were read from the archive manifest.
- The 240 monthly observations are not included, so a reader can reproduce arithmetic on the 30 aggregates but cannot reconstruct those aggregates solely from this package.
- Statistical validation does not establish legal tariff eligibility, causality, publication rights or employer approval.

The portfolio execution record adds a fresh arithmetic reproduction without changing the archived statistical input. Public diffusion approval is handled separately from statistical validation.
