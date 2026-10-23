# Data dictionary

`official_cells.csv` is an independently extracted statistical snapshot. **Every value is in millions of pesos at 2018 basic prices.** Reference year is 2018; original workbook metadata update is 2023-08-29. No nominal time-series comparison is performed.

| Field | Definition |
|---|---|
| `family` | MIP = symmetric product-by-product input–output matrix; COU = supply-and-use tables |
| `product_code` | 311513 (MIP), or broader 3115 (COU); text identifier |
| `origin` | D = domestic; M = imported; T = published combined table |
| `kind` | `intermediate` = destination product cell; `final` = account component; `control` = published row total |
| `target` | Six-digit destination product code, component label, or named control |
| `value` | Signed numeric value; zeros are published zeros, never imputed missing values |
| `file`, `sheet`, `cell` | Exact workbook and original cell locator |
| `label_original` | Original header retained as source metadata; result labels are English translations or analytical groups |

There are 834 intermediate cells for each MIP origin, including zeros. The three origins form overlapping representations: **D + M = T**, so do not sum all three. `control` totals likewise overlap underlying components. The raw snapshot is not a long-form additive fact table without filtering `kind` and `origin`.

For combined MIP final demand, `imports_net` is a negative balancing import entry. Gross final uses sum D and M, and equal the T published final total less `imports_net`. COU totals in this selected vintage use a different presentation and broader product category; they remain separate.

## Exhaustive destination grouping

Rules are applied in this order; every code receives exactly one group.

| Rule on destination code | Analytical group |
|---|---|
| Starts 3115 | Dairy products |
| Starts 311 or 3121, after excluding 3115 | Other food and beverages |
| Starts 31, 32 or 33, after the preceding exclusions | Other manufactures |
| Starts 722 | Food and beverage services |
| Starts 61, 62 or 93 | Education, health and government services |
| All remaining codes | Other products and services |

The mapping describes homogeneous product groups in the MIP. It is not an institutional-sector classification, purchasing-establishment register or retail-channel mapping.

## Output denominators

`origin_and_uses.csv`: intermediate share of origin = intermediate / (intermediate + final) of that origin; origin share of all uses = origin all uses / both-origin gross uses; origin share of intermediate = origin intermediate / both-origin intermediate.

`intermediate_destination_groups.csv`: distribution = group's total / all intermediate uses; imported share within group = group's imported / group's total.

`final_uses.csv`: each total / gross final uses, keeping signed inventory changes.

`universe_comparison.csv`: MIP and COU each use their own intermediate / gross total. Results are Decimal strings and are unrounded for downstream presentation.
