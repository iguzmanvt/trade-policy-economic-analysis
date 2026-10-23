# Observed duty intensity and the interpretation of trade reallocation

**Isaac Guzmán Valdivia Tovar · Analytical sample · 22 October 2026**

This bounded analytical example compares U.S. imports for consumption in three 10-digit Harmonized Tariff Schedule (HTS10) lines from Mexico, China, Taiwan, Vietnam and Malaysia. It is intended as an analytical writing sample. It is not an IMF publication, and no affiliation or endorsement is implied.

[Read the analytical note](NOTE.md).

## Main finding

In the archived snapshot, U.S. imports for consumption from Mexico in the selected lines increased from **$53.90 billion** in January–August 2025 to **$113.10 billion** in the same months of 2026 (**109.8%**). Mexico's observed duty intensity in 2026 was far below China's, while the other selected Asian suppliers also had low ratios. These comparisons motivate a research question; they do not estimate a causal tariff effect.

## Reproduce

Requires Python 3.11 or later. No additional packages, credentials or network connection are required.

```bash
python analyze.py
```

The script reproduces the tables from the bundled 30-row snapshot. The snapshot was reconstructed upstream from archived monthly observations. By default the script reads `data/census_snapshot.csv` and overwrites the reproducible result files in `results/`. It can also run from a different working directory or accept explicit paths:

```bash
python analyze.py --input data/census_snapshot.csv --output results
```

The script uses decimal arithmetic. Output decimals are unrounded strings; tables in the writing sample round only for presentation.

## Contents

| File | Purpose |
|---|---|
| `data/census_snapshot.csv` | 30 aggregate product–country–period observations |
| `analyze.py` | Coverage checks, calculated-duty ratios, gaps and import growth |
| `results/duty_intensity_by_line.csv` | Product and supplier comparisons in both periods |
| `results/mexico_import_growth.csv` | U.S. import values from Mexico and changes by product |
| `results/weighted_duty_intensity.csv` | Country ratios across the three lines, using sums |
| `results/results.json` | Full precision calculations and validation flags |
| `METHODOLOGY.md` | Definitions, vintage treatment and inference limits |
| `data/DICTIONARY.md` | Standalone input/output dictionary |
| `EXECUTION.md` | Portfolio continuation execution record |
| `sources.json` | Official reference links and provenance of the archived snapshot |
| `VALIDATION.md` | Completed checks and limits of verification |
| `NOTE.md` | Full analytical note readable on GitHub |

## Data basis

The input is a **January–August sum of archived monthly observations**, reconstructed separately for 2025 and 2026. It is not a direct download of Census's revised cumulative `_YR` variables. Earlier months retain their archived vintages. A fresh API check was attempted during preparation but did not complete; this package reproduces the included snapshot, not the latest live release.

Duty intensity is `100 × calculated duties / customs value of imports for consumption`. It is not a simple average of monthly rates. Country totals also use the ratio of sums. Output CSVs include the period basis; `2026-08` is the endpoint of January–August, not a single month.

The three lines are 8471500150, 8471709000 and 8517620020. The shortened product labels are descriptive; these exact codes define the selection. This is not a comprehensive electronics or data-center basket, and the data do not identify final use.

## Provenance and reuse

The analytical note and script were prepared independently for this portfolio. Only a bounded extract of public statistics is included; employer reports and original client-project code are excluded. See the portfolio rights notice for source-specific conditions.

The archived input and analytical results are preserved from the completed sample. This edition removes the redundant Word copy and adds a dictionary and execution record; it does not restart the tariff extraction.
