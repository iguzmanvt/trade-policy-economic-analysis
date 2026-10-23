# P02B data and output guide

This directory is the product-basket subanalysis of P02. The authoritative field definitions, formulas, vintage treatment and absence conventions are in the [shared Census dictionary](../../census-common/DATA_DICTIONARY.md). The [partner analysis dictionary](../DICTIONARY.md) describes a different input and denominator.

## Inputs

| File | Grain and scope | Important fields |
|---|---|---|
| `data/general_imports_monthly.csv` | 4,794 reported month–Mexico–HTS10 records; January–August 2025 and 2026; general imports | `period`, `flow`, `hts10`, `hs6`, `country_code`, `partner_iso3`, `general_imports_usd`, `source_id`, `statistical_basis` |
| `data/basket_hts10.csv` | Fixed membership of 374 historical HTS10 lines grouped into 88 HS6 categories | `hts10`, `hs6`, `description`, `selection_scope`, `basket_version` |

HTS10 means the ten-digit Harmonized Tariff Schedule statistical code; HS6 means the six-digit Harmonized System group. Codes remain text and dollar amounts are nominal U.S. dollars. The statistical input is a sparse archived extract, not a completed code-month panel. An absent record is not a measured zero. Source and sanitized-input hashes are in [sources.json](sources.json).

## Outputs

| Output | Meaning / denominator |
|---|---|
| `results/concentration.csv` | HHI = 10,000 × sum of squared shares of 88 HS6 groups formed from the selected HTS10 lines; each year's reported basket total is the denominator |
| `results/composition_hs6.csv` | Group values, changes, shares and contributions within that selected basket |
| `results/contributions.csv` | Three leading lines and the residual of reported basket values; net-change shares divide by total basket change, while growth contributions divide by its 2025 value |
| `results/reported_hts10_sums.csv` | Available period sums, reported-month counts and availability flags; entire-period absence stays blank |
| `results/monthly_totals.csv` | Sums of reported basket values for the 16 actual month periods |
| `results/summary.json`, `results/checks.json` | Full-precision summary and executed checks |

`reported_sum_change_usd` subtracts the sums of records present in each period. The empty sum used in that accounting difference is zero; it does not turn an absent series into observed zero trade or justify calculating its growth rate. Signed contributions can be negative or exceed 100% when declines offset gains.

The file `figures/contributions.svg` displays three leaders plus a residual. HHI is calculated from all 88 selected HS6 groups, not from those four displayed bars. P02B is not an estimate of all trade, every code inside the 88 headings, final use or a causal tariff effect.
