# Methodology

## Population and selection

U.S. imports for consumption, three exact HTS10 products (`8471500150`, `8471709000`, `8517620020`), five origin partners (Mexico, China, Taiwan, Vietnam, Malaysia), January–August 2025 versus January–August 2026. The inherited focal selection is a bounded illustration, not a representative product sample or an identified data-center basket. No additional product or supplier is imputed.

The unchanged snapshot contains 30 aggregate rows. Its basis is `JAN_AUG_MONTHLY_SUM`: January–August totals reconstructed from archived monthly observations. `time` marks the period endpoint, not an August-only observation. The [common Census dictionary](../census-common/DATA_DICTIONARY.md) distinguishes this consumption-import sample from P02's partner and product-basket perspectives; a [local field reference](data/DICTIONARY.md) is retained for this input.

## Estimands

- Line intensity (%) = `100 × calc_dut_usd / con_val_usd` within product, origin and period.
- Gap to Mexico (percentage points) = supplier intensity minus Mexico intensity in the same product and period.
- Change in intensity (percentage points) = 2026 intensity minus 2025 intensity in the same product and origin.
- Country intensity (%) = `100 × sum(calc_dut_usd) / sum(con_val_usd)` across the three selected products. The weights differ by supplier and period.
- Retained companion import growth (%) = `100 × (value_2026 / value_2025 − 1)` for Mexico. Trade decomposition is developed separately in P02.

Decimal arithmetic precedes display rounding. A zero or missing denominator is rejected and never converted into a zero rate. Negative gaps and changes are retained. The source selection has positive denominators throughout.

## Vintages and lineage

No live download is performed. This run uses the input hash documented in `sources.json`. The archive update label is inherited metadata, not proof of an original retrieval timestamp. The earlier documentation reports 240 underlying monthly observations and eight months per aggregate. Those rows are not supplied; this run does not independently verify month coverage or regenerate the aggregate snapshot.

Archived sums are not directly downloaded revised `_YR` fields, and there is no forced reconciliation between them. Reproducing these calculations is distinct from checking the most recent Census release. Any future statistical update must create a new snapshot version and explicitly reconcile revisions across P01 and P02.

## Interpretation

The denominator is customs value of imports for consumption. General imports, export values and mirror flows are not interchangeable denominators. Country totals describe country-specific composition rather than a common fixed basket. Comparisons are descriptive; they do not identify tariffs' causal effect, legal tariff rates, final duty payments, origin eligibility, transshipment, domestic value added, final use or contributions to gross domestic product.

Calculated duties are governed by the official definitions linked in [common sources](../census-common/SOURCES.md). Original code is licensed separately from Census source statistics; no license here reclassifies third-party materials.
