# Execution and validation record

Prepared 22 October 2026 (Mexico City). Scope: the public partner extract and newly written portfolio analysis.

## Executed

```bash
python projects/02-trade-concentration/analyze.py
```

Run from the portfolio root, with Python 3.11 or later. Result: **Validated 1,846 partner–flow–period rows; reproduced eight concentration summaries.** No external packages or network access are used by this command.

- Recovered and inspected the effective prior HHI country-components file, its audit and upstream extraction definitions. Selected only the all-goods January–August country totals, excluding prior bespoke baskets. Wrote new Python code and English prose.
- Normalized integer dollar strings from archived numeric totals without changing their values. The amounts are below the exact-integer range of the upstream binary representation; the new analysis uses decimal arithmetic.
- Checked all 1,846 unique input keys; all eight expected flow–period groups; codes, periods, finite nonnegative integer values and positive denominators. HHI uses separate individual partners; shares and signed growth contributions sum to 100% within numerical tolerance.
- Regenerated the result CSVs, validation JSON and SVG. The exact input hash is in `results/validation.json` and `sources.json`.
- Independently calculated all eight HHI and Canada/Mexico shares with a separate floating-point sum to check the decimal implementation. A separate reviewer then used exact rational arithmetic (`fractions.Fraction`) on all 1,846 input rows to verify every total, HHI, regional share and partner growth contribution in both flows; all passed, and the exact signed contributions sum to 100% per flow.
- Recomputed SHA-256 for the actual archived August 2026 general-import and total-export monthly source files; both matched the pre-existing audit hashes. No private source paths or prior client scripts are included in the public project.
- Converted the SVG to PNG with Inkscape for visual inspection. Titles, series, labels, endpoint values, axes and source note were visible without clipping. The PNG is temporary QA material and is not part of the project. Inkscape is not needed for reproduction or GitHub display of the SVG.

## Limits

The 64 upstream product-month partitions and their original download timestamps were not freshly downloaded or comprehensively revalidated. Aside from the two hashes described above, upstream hashes and coverage checks are retained provenance from the prior effective extraction. The code reproduces **downstream measures from the included partner extract**, not the upstream product-month extraction. A fresh Census request and reconciliation to current revised world/cumulative totals were not performed. The archive's vintage limitations remain beside the results. Publication approval is tracked at the portfolio level.
