# Validation record

Analytical validation initially executed 22 October 2026, America/Mexico_City. The canonical integration was reproduced on 23 October 2026. This record covers the delivered aggregate snapshot and derived results, rather than an independent audit of the original Census statistical release.

## Checks executed for this version

- Ran `python analyze.py` successfully on the bundled data. The 30 keys are unique and exhaust three products × five origin partners × two periods. Codes and names match, all numeric values are finite and nonnegative, import-value denominators are positive, and every row explicitly uses `JAN_AUG_MONTHLY_SUM`.
- Recomputed all 30 duty ratios and all 30 gaps using Python `Fraction` arithmetic independently of the script's `Decimal` calculation. Differences after float conversion were below `1e-12` percentage points.
- Independently summed duties and values for all ten country–period groups and checked their ratios of sums. Integer totals matched exactly; rates agreed within `1e-12` percentage points.
- Compared core results against the supplied predecessor: all 30 rates and gaps, ten country totals, three Mexico import changes, and the Mexico grand totals and growth were unchanged. The three retained CSV result files are byte-for-byte identical to their predecessors.
- Verified the input SHA256: `b68c40d953e13a6a15c9babc17b76ab3a39129dcbd56a819a259b7387ac147ca`.
- Checked that zero, missing and nonfinite denominator values in temporary modified inputs are rejected rather than converted into zero rates.
- Parsed the generated SVG as XML, rendered it to a temporary PNG and inspected the chart at its intended 1200 × 700 reading size. Titles, separate scales, signed values, code labels and source note are legible and unclipped. The PNG is an internal preview; the delivered SVG is the reproducible figure.

## Inherited evidence kept separate

Previous preparation reported 240 monthly observations, no duplicate monthly keys and eight months per aggregate. Those observations are not included in this project. Their coverage and source concordance were **not newly checked in this run**. The archive update label is not treated as an independently verified original download timestamp.

## Not established

- No fresh statistical API extraction, current revised Census cumulative `_YR` comparison, or new reconstruction of the 30 aggregate values from monthly records was performed.
- Upstream full-source hashes were not recomputed. Only the included snapshot identity was verified.
- Numerical reproduction does not establish legal tariff rates, final net receipts, tariff eligibility, causal effects, origin compliance, transshipment or final use.
- This analytical validation does not certify a GitHub publication. Publication identity is recorded separately by the portfolio coordinator; the existing published project and author dissemination authorization are retained.

## Canonical integration check — 23 October 2026

The enhanced script ran successfully from the canonical project directory. The input hash remained unchanged, the three previously published CSV tables were reproduced byte for byte, and every previously reported core value in `results.json` was retained. The integration adds 15 temporal rate changes, the source-return figure, and more explicit validation-scope fields. The prior source basenames, column mapping, product/partner codes and two inherited upstream hashes remain in the merged source register. No original monthly consumption rows were included or revalidated, and no statistical refresh was performed.
