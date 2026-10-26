# Data dictionary

The extract is an independently prepared row snapshot of official INEGI statistics. Every numeric value is in **millions of pesos at basic prices for 2018**. Reference year and base year are 2018; original workbook metadata update is **2023-08-29**. The verification on 26 October 2026 leaves this statistical vintage unchanged. No nominal time-series comparison is performed.

## Universes and dimensions

| Family | Exact official label | Meaning of row | Meaning of intermediate columns | Included coverage |
|---|---|---|---|---|
| MIP | `311513 - Elaboración de derivados y fermentos lácteos` | Uses of the class-associated product category in the symmetric product-by-product matrix | Homogeneous destination product groups, six-digit SCIAN Mexico 2018 codes | All 834 destinations per origin, six final components, controls, and the combined table's imports adjustment |
| COU | `3115 - Elaboración de productos lácteos` | Uses of a broader product category in the supply-and-use tables | User industries, SCIAN Mexico 2018 branch level | Only six final components and three controls per origin; industry-level intermediate cells were not extracted |

The class definition includes dairy derivatives and ferments as well as imitation cheese. The branch is broader. Neither universe identifies particular cheese names, firms, retail channels or the country of origin of imports. The MIP row is a product-use allocation, not the complete input-cost structure of its producing industry or of any destination group.

## Fields in `official_cells.csv`

| Field | Definition |
|---|---|
| `family` | `MIP` = symmetric product-by-product input-output matrix; `COU` = supply-and-use tables |
| `product_code` | `311513` for MIP; separate broader `3115` for COU; text identifier |
| `origin` | `D` = domestic; `M` = imported; `T` = published combined table |
| `kind` | `intermediate` = MIP destination product cell; `final` = final-account component or imports adjustment; `control` = published row total |
| `target` | Six-digit MIP destination code, a final component name, or a control name |
| `value` | Signed numeric value; published zeros are retained, not imputed from missing values |
| `file`, `sheet`, `cell` | Exact workbook basename, original sheet and coordinate |
| `label_original` | Original header retained as source metadata; final labels are English translations or analytical groups |

There are **2,557 rows**: 2,502 MIP intermediate cells (834 x 3 origins), 28 MIP components/controls and 27 COU components/controls. Of the 834 combined MIP destinations, 89 have positive values and 745 are zero. Keys are `(family, origin, kind, target)`; source locators are also unique.

## Additivity, controls and signed components

D and M are the two additive origins. T is a published combined representation and must not be added to D + M as a third flow. Controls overlap the components beneath them. The snapshot therefore is not an additive fact table without filtering `family`, `kind` and `origin`.

| Target | Meaning and treatment |
|---|---|
| `intermediate_published` | Published sum of intermediate destinations |
| `final_published` | Published final block; combined MIP includes the negative imports adjustment |
| `all_published` | Published intermediate plus published final block; not automatically gross uses in combined MIP |
| `private_consumption` | Published private final-consumption component; not a retail-sales channel |
| `government_consumption` | Government final consumption |
| `fixed_capital` | Gross fixed capital formation |
| `inventories` | Signed change in inventories; MIP total is -162.465, COU total is separately -160.904 |
| `exports` | Exports of goods and services in the row; included in the gross-use denominator |
| `discrepancy` | Published statistical discrepancy |
| `imports_net` | Negative imports-netting entry, only in the combined MIP final block; a presentation adjustment, not another use |

For MIP, gross final uses equal domestic final plus imported final uses:

`84,412.694 - (-21,761.015) = 106,173.709`.

Gross all uses equal intermediate plus gross final uses, or domestic all uses plus imported all uses: `18,072.048 + 106,173.709 = 124,245.757`. “Gross” refers to removing imports netting, not to removing negative inventories or exports. These uses are not domestic absorption.

COU uses the separate broader category and selected presentation; its controls and final components satisfy D + M = T directly. Its 17.6% intermediate-use share is not another imported-origin share.

## Exhaustive destination grouping

The rules are applied in this order and assign every MIP destination code exactly once. They are analytical aggregations, not new official institutional sectors.

| Rule on destination code | Analytical group |
|---|---|
| Starts `3115` | Dairy products |
| Starts `311` or `3121`, after excluding `3115` | Other food and beverages |
| Starts `31`, `32` or `33`, after the preceding exclusions | Other manufactures |
| Starts `722` | Food and beverage services |
| Starts `61`, `62` or `93` | Education, health and government services |
| All remaining codes | Other products and services |

## Output fields and denominators

| File / field | Definition |
|---|---|
| `origin_and_uses.csv`: `intermediate`, `final`, `all_uses` | Values for D or M; `all_uses = intermediate + final` |
| `intermediate_share_of_origin_pct` | 100 x intermediate uses of one origin / all uses of that same origin; imported row gives 34.5% |
| `origin_share_of_all_uses_pct` | 100 x all uses of one origin / both-origin gross uses; imported row gives 17.5% |
| `origin_share_of_intermediate_pct` | 100 x intermediate uses of one origin / both-origin intermediate uses; imported row gives 41.5% |
| `intermediate_destination_groups.csv`: `domestic`, `imported`, `total` | Values of the focal 311513 product used by that destination group; total = domestic + imported |
| `share_of_intermediate_pct` | 100 x group total / all MIP 311513 intermediate uses |
| `imported_share_within_group_pct` | 100 x group's imported 311513 uses / group's total 311513 uses; not imported content of all inputs used by the group |
| `final_uses.csv`: `share_of_final_pct` | 100 x signed component total / gross final uses; negative inventory change stays negative |
| `universe_comparison.csv`: `intermediate_share_pct` | 100 x intermediate / own-universe total: MIP 311513 gross uses for 14.5%; separate COU 3115 total uses for 17.6% |

All percentages are ratios of values, not physical-quantity shares. Decimal arithmetic uses the published unrounded cell strings; output tables retain unrounded ratios. Presentations round percentages to one decimal and monetary values to three decimals, except chart labels at one decimal. Displayed rounded percentages need not add exactly to 100.

## Provenance and reproduction

`workbook_provenance.json` pins six historical SHA256 values, titles, row indices, year and metadata date. `source_recovery_20261026.json` separately records their fresh official retrieval, unchanged binary identities and comparison of all selected cells. `sources.json` retains historical verification and adds the dated recovery, including the precise source links.

The analyzer validates every structural and accounting condition before writing outputs. The extractor verifies all six hashes against the unchanged registry before extraction and rejects an unexpected source version without replacing the existing snapshot. Both keep their checks active under `python -O`. Figure and note numbers are generated by `build_publication.py` from the four result CSVs.
