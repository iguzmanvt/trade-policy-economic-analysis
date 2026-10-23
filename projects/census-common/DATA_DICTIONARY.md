# Census dictionary and transformation contract

Contract version: `CENSUS_COMMON_INTEGRATED_R04`. Information cutoff: 22 October 2026; integration review: 23 October 2026. A new review date does not refresh a statistical vintage. All codes are text and monetary values are nominal U.S. dollars. The reporting economy is the United States.

HTS10 means the ten-digit Harmonized Tariff Schedule statistical code used for imports. HS6 means a six-digit Harmonized System group. P02A sums imports and exports independently before comparing partners; export statistical codes are Schedule B codes, not a reclassification of detailed HTS10 import lines.

## Three statistical layers

| Property | P01 — observed duties | P02A — partners | P02B — selected products |
|---|---|---|---|
| Canonical input | [Consumption snapshot](../01-observed-duty-intensity/data/census_snapshot.csv) | [Partner values](../02-trade-concentration/data/partner_values.csv) | [Monthly general imports](../02-trade-concentration/product-basket/data/general_imports_monthly.csv) |
| Grain / rows | Product–supplier–period / 30 | Partner–flow–period / 1,846 | Month–Mexico–HTS10 / 4,794 |
| Period | January–August 2025 and 2026 | January–August 2023–2026 | January–August 2025 and 2026 |
| Flow | Imports for consumption | General imports and total exports, kept separate | General imports |
| Geography | Five selected suppliers | Individual foreign partners; Canada and Mexico also reported as a combined share | Mexico only |
| Product scope | Three exact HTS10 lines | All reported products retained in each archived flow | Fixed list of 374 historical HTS10 lines grouped into 88 HS6 categories |
| Denominator | Same-product consumption customs value, or a disclosed ratio of country sums | Sum of retained individual-partner values for the same flow-period | Sum of reported values in the fixed selected basket for the same year |

Imports for consumption use customs value of merchandise cleared for consumption. General imports capture physical arrivals. Goods can enter warehouses or foreign trade zones before clearance, so the flows can differ. Total exports include domestic exports and reexports at free alongside ship (FAS) value; general imports use customs value. The flows are alternatives for different questions, not quantities to add or force into equality. [Census definitions, sections 3 and 6](https://www.census.gov/foreign-trade/guide/sec2.html).

## P01 — `01-observed-duty-intensity/data/census_snapshot.csv`

Primary key: `(time, cty_code, hts10)`. Exactly 30 rows = 2 periods × 5 suppliers × 3 products.

| Field | Type / definition |
|---|---|
| `time` | `2025-08` or `2026-08`; endpoint of a January–August sum, not August alone |
| `basis` | Exactly `JAN_AUG_MONTHLY_SUM`; not a direct official cumulative `_YR` retrieval |
| `cty_code` | Four-character Census code: `2010` Mexico, `5700` China, `5830` Taiwan, `5520` Vietnam, `5570` Malaysia |
| `country` | Label matching the country code |
| `hts10` | `8471500150`, `8471709000` or `8517620020` |
| `con_val_usd` | Archived sum of customs values of imports for consumption; positive for a calculated rate |
| `calc_dut_usd` | Archived sum of associated calculated duties |

Input SHA256: `b68c40d953e13a6a15c9babc17b76ab3a39129dcbd56a819a259b7387ac147ca`. Thirty included aggregates support arithmetic reproduction. The 240 upstream monthly observations and eight months per cell are documented antecedents: **zero original consumption-month rows are included or newly revalidated here**. No new live statistical refresh was performed.

Duty intensity is `100 × sum(calculated duties) / sum(consumption customs value)`. Gap in percentage points is a supplier's ratio minus Mexico's ratio within the same product-period. A negative gap means a lower observed ratio. Aggregate country ratios use each country's own product composition, not a fixed-weight index. Missing or zero denominators are not converted to zero rates. Source measures correspond to `CAL_DUT_MO` and `CON_VAL_MO` upstream.

## P02A — `02-trade-concentration/data/partner_values.csv`

Primary key: `(flow, period, country_code)`. See the [partner-specific dictionary](../02-trade-concentration/DICTIONARY.md) for the full output contract.

| Field | Type / definition |
|---|---|
| `flow` | `M`: general imports; `X`: total exports, domestic plus reexports |
| `period` | `YYYY-01_08`; January–August archived monthly sum |
| `country_code` | Four-character individual Census partner identifier, 1000–7999 |
| `country_name`, `iso3` | Descriptive archived partner labels; aggregation key remains the Census code |
| `value_usd` | Nonnegative integer dollars: customs import value or FAS export value |

World, regional and unallocated aggregate identifiers are excluded from the retained partner denominator. Each flow-period is calculated separately. The partner Herfindahl–Hirschman Index (HHI) is `10,000 × sum(partner_share²)` with individual partner shares on a 0–1 scale. Canada and Mexico remain individual squared terms; only their separate regional share pools the two values. Effective equal-sized partners are `10,000 / HHI`.

A present zero stays zero; blank or malformed amounts fail validation. For the **signed 2025–2026 partner change decomposition only**, an absent partner in the complete archived flow-period extract contributes an accounting value of zero. This convention depends on inherited coverage checks for that extract; it is not a newly verified observed zero or certification of a live source. It does not transfer to P02B's missing product-month rows. Each signed partner change divides by that flow's total net change, so contributions can be negative or exceed 100%.

## P02B — `02-trade-concentration/product-basket/data/general_imports_monthly.csv`

Primary key: `(period, country_code, hts10)`. The 4,794 reported rows span 16 distinct month-periods. The input is sparse, not a balanced panel.

| Field | Type / definition |
|---|---|
| `period` | Actual month, January–August 2025 or 2026 |
| `flow` | Exactly `general_imports` |
| `hts10`, `hs6` | Selected statistical line and its first six digits |
| `country_code`, `partner_iso3` | Exactly `2010` and `MEX`; the latter is an International Organization for Standardization (ISO) label |
| `general_imports_usd` | Nonnegative integer monthly customs value; missing amounts are not converted to zero |
| `source_id` | Safe archived-source identifier, with no private filesystem path |
| `statistical_basis` | Exactly `ARCHIVED_MONTHLY`; monthly sums are not direct revised `_YR` fields |

Panel SHA256: `83904e5c96b3f26c289d63e3ec649a0a996f1f1f7ca8e90a5b2755c354d052b9`. The [fixed basket](../02-trade-concentration/product-basket/data/basket_hts10.csv) has SHA256 `01c2805bd2daf50bd4b2e2181cb701b5beb912115b111946901b4a2374ca49cf`. Its 374 lines define the membership, grouped into 88 HS6 categories. Fields are `hts10`, `hs6`, `description`, `selection_scope` and `basket_version`. Inherited MAIN, COMPLEMENT and EXTENDED labels are all included; they do not establish an official industry boundary or final use.

There are 328 observed lines in 2025, 344 in 2026 and 356 in their union. Omission of a code-month record does not establish zero trade, code inactivity or complete coverage. No absent row is fabricated. All 88 selected HS6 groups have reported values in each comparison window, but the basket does not include every possible HTS10 line in those groups.

Product shares divide by the selected basket's reported value in the same year. Product HHI is `10,000 × sum(HS6_share²)` across all 88 groups formed from selected lines; it is not calculated from the figure's three leaders plus residual. It is a different dimension and denominator from P02A's partner HHI. Neither is an antitrust finding.

Dollar contributions are changes in reported sums. Net-change contributions divide by total basket change; growth contributions in percentage points divide by the 2025 basket value and multiply by 100. Signed contributions can be negative or exceed 100%. Detailed HTS10 outputs retain a blank value when an entire period is unobserved and show reported-month counts plus availability flags. An empty sum in `reported_sum_change_usd` is an accounting zero, **not measured zero activity or a valid growth rate for an absent series**. See the [local output guide](../02-trade-concentration/product-basket/DATA_DICTIONARY.md).

## Flow bridge and vintage boundaries

Run `python projects/census-common/reconcile_flows.py` from the portfolio root. The bridge reads the canonical P01 snapshot and P02B monthly panel and writes [six matched comparisons](results/flow_comparison.csv). `general_minus_consumption_usd` subtracts consumption from general imports for the same Mexico/product/January–August cell. It is not extra trade, an error to eliminate or an estimate of a warehouse balance. It does not use P02A's all-partner input.

Eight-month coverage checks in this bridge apply only to the three matched P02B general-import series. They do not newly verify P01's upstream monthly consumption observations or all P02B code-month combinations. Archive labels, recovery timestamps and official download dates remain distinct. No layer infers quantity, real growth, domestic value added or causal policy effects from nominal gross flows.
