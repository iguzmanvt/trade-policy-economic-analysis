# Observed duties across suppliers of three equipment lines

Isaac Guzmán Valdivia Tovar · 22 October 2026

This project measures observed calculated-duty intensity within the same Harmonized Tariff Schedule 10-digit (HTS10) product code across Mexico, China, Taiwan, Vietnam and Malaysia. It is a descriptive portfolio sample using U.S. imports for consumption in January–August 2025 and 2026.

[Read the analytical note](NOTE.md) · [Method and limitations](METHODOLOGY.md) · [Validation record](VALIDATION.md)

## Result

China's 2026 observed ratios exceeded Mexico's by **26.269–27.668 percentage points** across the three lines. Gaps against Taiwan, Vietnam and Malaysia were much smaller and sometimes negative: Mexico's switching and routing ratio was **0.092–0.102 points higher** than theirs. Supplier-specific comparisons matter; this exercise does not identify a causal tariff effect.

![Observed duty intensity gaps relative to Mexico, 2026](figures/gaps_vs_mexico_2026.svg)

## Reproduce

Requires Python 3.11 or later, standard library only. No credentials, network access or additional packages are required.

```bash
python analyze.py
```

The script validates and reads the bundled **30 aggregate rows**, regenerates five CSV/JSON result files and an SVG chart. It can run from any working directory. To write alternative outputs:

```bash
python analyze.py --input data/census_snapshot.csv --output results
```

The figure is written to `figures/` next to the output directory. Numeric outputs retain Decimal precision; presentation rounding does not affect calculations. Zero or missing denominators raise an error rather than producing a zero rate. A common dictionary and source definitions are maintained at [Census data dictionary](../census-common/DATA_DICTIONARY.md) and [Census sources](../census-common/SOURCES.md).

## Data and outputs

| File | Contents |
| --- | --- |
| `data/census_snapshot.csv` | Unchanged 30-row archived aggregate snapshot |
| `analyze.py` | Validation, duty ratios, gaps, changes, legacy trade totals and chart |
| `results/duty_intensity_by_line.csv` | All 30 country–product–period ratios and gaps to Mexico |
| `results/duty_intensity_changes.csv` | 15 changes from 2025 to 2026 in percentage points |
| `results/weighted_duty_intensity.csv` | Ten country–period ratios of sums across three products |
| `results/mexico_import_growth.csv` | Retained companion trade-value results; composition analysis is in P02 |
| `results/results.json` | Full-precision results, input hash and explicitly scoped checks |
| `figures/gaps_vs_mexico_2026.svg` | Dependency-free chart with separate, labeled comparison scales |
| `sources.json` | Snapshot identity, source links and verification scope |
| `data/DICTIONARY.md` | Retained local field reference and link to the common dictionary |
| `EXECUTION.md` | Canonical integration checks and separately labeled historical execution |
| `CODE_LICENSE.txt` | License scoped to original code; source-data terms remain separate |

## Coverage and vintage

**January–August totals reconstructed from archived monthly observations.** This is the input's statistical basis, not a new reconstruction performed here. Earlier work reported 240 monthly observations; those records are not included and were not revalidated in this run. The executable reproduction starts from 30 aggregates. This project does not download official cumulative `_YR` fields or certify the latest revised Census release. Original download timestamps are not established by the archive's update label.

Exact product codes: `8471500150`, `8471709000`, `8517620020`. The sample is selected and bounded; it does not cover all electronics or identify data-center use. Values are gross and nominal. Calculated duties are neither legal tariff rates nor final net customs receipts.

This is the published project's canonical directory. The analytical presentation, temporal changes and figure have been integrated under the author's existing public-dissemination authorization. The input vintage and central results are unchanged; private application and coordination packages remain separate.
