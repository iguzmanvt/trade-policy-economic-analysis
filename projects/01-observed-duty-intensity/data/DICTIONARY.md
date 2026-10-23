# Data dictionary

`census_snapshot.csv` has 30 rows: 3 products × 5 suppliers × 2 periods. Codes are text. There are no missing input values.

| Field | Type / unit | Meaning |
|---|---|---|
| time | YYYY-MM | August endpoint of the January–August period, not one month's flow |
| basis | text | `JAN_AUG_MONTHLY_SUM`: sum of archived monthly observations |
| cty_code | four-character text | Census partner code |
| country | text | Supplier label |
| hts10 | ten-character text | Exact Harmonized Tariff Schedule statistical code |
| con_val_usd | integer, nominal U.S. dollars | Customs value of imports for consumption |
| calc_dut_usd | integer, nominal U.S. dollars | Calculated duties on the corresponding consumption imports |

Output `duty_intensity_pct` is 100 × calculated duties / import value; `gap_vs_mexico_pp` subtracts Mexico's ratio within the same product and period. `weighted_duty_intensity.csv` uses the ratio of country sums across the three products, with each country's own composition. Growth compares January–August 2026 with January–August 2025. Outputs retain unrounded decimal strings; notes round for presentation.

Zero duties are observed zeros. No zero denominator is imputed. Absent cells fail validation instead of becoming zero flows. See [methodology](../METHODOLOGY.md) for vintages and interpretation.
