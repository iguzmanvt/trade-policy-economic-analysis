# Methodology

## Question and scope

How do observed duty-to-import-value ratios differ across suppliers of three computer and network equipment lines, and what can these descriptive differences say about Mexico's trade expansion?

The selection includes three 10-digit Harmonized Tariff Schedule (HTS10) codes (8471500150, 8471709000, 8517620020), five suppliers (Mexico, China, Taiwan, Vietnam, Malaysia), and January–August in 2025 and 2026. These lines were chosen as a bounded example from existing work. They are not a representative sample of all trade, the full universe of electronics, or a direct measure of data-center demand.

## Input fields

| Field | Definition |
|---|---|
| `time` | Endpoint of the reconstructed January–August period; 2025-08 or 2026-08 |
| `basis` | `JAN_AUG_MONTHLY_SUM`, explicitly marking an archived monthly reconstruction |
| `cty_code` | Census partner code, stored as text |
| `country` | Partner label matched to the code |
| `hts10` | Exact 10-digit product code, stored as text |
| `con_val_usd` | Sum of customs value of imports for consumption, nominal U.S. dollars |
| `calc_dut_usd` | Sum of calculated duties on those imports, nominal U.S. dollars |

The original archived fields `customs_value_usd` and `calculated_duty_usd` were mapped to the two numeric fields. The aggregation included 240 monthly observations, eight per product–partner–year cell. Monthly key uniqueness and coverage were checked during extraction. The reproducible CSV contains the 30 sums, not the 240 original monthly observations.

## Calculations

For each product, supplier and period:

- Duty intensity (%) = 100 × sum of calculated duties / sum of customs value.
- Gap to Mexico (percentage points) = supplier duty intensity − Mexico duty intensity.
- Import growth (%) = 100 × (2026 value − 2025 value) / 2025 value.
- Aggregate duty intensity across the three products uses summed duties divided by summed import value. It is not the unweighted mean of product rates.

A negative gap means that the comparison supplier has a lower observed ratio than Mexico. Country aggregates reflect each supplier's product composition, so product-specific comparisons are preferable when discussing tariff differences.

## Vintages and reproducibility

The archive updated in October 2026 retains the vintages of earlier monthly observations. Revised official year-to-date values can differ from sums of previously downloaded months. This workflow does not force those vintages to agree. The source archive label and recorded upstream hashes are listed in `sources.json`; original download dates and complete upstream files were not independently revalidated in this workflow.

A live Census API request was attempted but timed out. The calculations can be reproduced offline from the included aggregate snapshot. A future update should download all comparison months using a documented common release, preserve retrieval dates and raw files, reconcile revisions, and regenerate the outputs. The script currently does not download data or independently reconstruct the 30 sums from the upstream monthly files.

## Interpretation limits

Calculated duties are a statistical measure, not a legal tariff schedule or final net cash revenue. The ratio can vary with transaction timing, composition, preferential treatment and the mix of dutiable and non-dutiable entries. It is not an estimate of USMCA utilization or legal eligibility. Antidumping/countervailing duties and subsequent administrative adjustments require separate attention under the source definitions.

Imports for consumption must not be mixed with general imports in the denominator. Trade values are gross and nominal: the data do not isolate volumes, prices, domestic value added, GDP contributions or final use. They do not prove production relocation, transshipment, origin compliance or noncompliance.

Observed trade growth and duty gaps are descriptive. A causal estimate would require policy timing, comparison groups and an identification strategy addressing demand, capacity, selection, policy endogeneity and spillovers to potential controls. The writing sample proposes that work; it does not report it as completed.

## Official references

- [Census International Trade Imports HS variables](https://api.census.gov/data/timeseries/intltrade/imports/hs/variables.html)
- [Census foreign-trade statistical definitions](https://www.census.gov/foreign-trade/guide/sec2.html)
- [Guide to International Trade Datasets](https://www.census.gov/foreign-trade/reference/guides/Guide_to_International_Trade_Datasets.pdf)
