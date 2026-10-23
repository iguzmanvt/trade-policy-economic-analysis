# Import exposure depends on which use is being measured

Isaac Guzmán Valdivia Tovar · 22 October 2026

## Finding and policy question

Imported products account for a much larger share of intermediate uses than of total uses in Mexico's dairy-derivatives category. In the 2018 symmetric input–output table, imports provide **41.5% of intermediate use**, compared with **17.5% of all gross uses**. A single aggregate import share would therefore understate the imported-origin proportion of the category's intermediate flows. These measures describe an accounting allocation, however; they do not measure the response of production or prices to a trade restriction.

The exercise asks how a narrow product category connects to domestic production and final accounts, while keeping each denominator explicit. It illustrates why a policy analyst should identify the statistical universe before interpreting import dependence or selecting an impact model.

## What is being measured

The National Institute of Statistics and Geography (INEGI) publishes a symmetric input–output matrix (MIP, its Spanish acronym) for 2018. This exercise uses the product-by-product matrix at the six-digit level of the North American Industry Classification System, Mexico 2018 (SCIAN). Category 311513 covers dairy derivatives, fermented products and substitutes; it includes substantially more than cheese. The original classification definition is located on printed page 151, PDF page 170. It does not isolate individual common cheese names.

The row records uses of products corresponding to 311513. Its 834 intermediate columns are homogeneous product groups, not a list of individual purchasing firms. The figures are monetary values at basic prices in millions of 2018 pesos. Domestic and imported identify the origin of the product. They do not identify an importing country or distinguish the United States from Europe.

For interpretation, gross uses equal domestic-origin uses plus imported-origin uses, with each split between intermediate and final uses. Ratios below are computed from the original values before rounding.

| Product origin | Intermediate uses | Final uses | All gross uses | Intermediate share of that origin |
|---|---:|---:|---:|---:|
| Domestic | 10,564.919 | 91,919.823 | 102,484.742 | 10.3% |
| Imported | 7,507.129 | 14,253.886 | 21,761.015 | 34.5% |
| Both origins | 18,072.048 | 106,173.709 | 124,245.757 | 14.5% |

Source: INEGI, MIP 2018, MIP_19 and MIP_38, `Tabulado`, row 196; author's extraction and calculations. Units: millions of pesos at 2018 basic prices.

The imported share of intermediate use is 7,507.129 / 18,072.048. The 34.5% imported-origin intermediate share in the last column answers a different question: it divides intermediate imported uses by **all imported uses**. Neither is a legal-origin or preferential-tariff-utilization measure.

## Where intermediate uses appear

A grouping of all 834 destinations places food and beverage services first, with 29.1% of intermediate use. Dairy product groups account for 24.3%, and other food and beverages for 21.0%. Together these groups represent 74.3%. Of 834 destinations, 89 have positive flows. Zero flows remain in the input snapshot, so coverage is not limited to the positive subset.

| Destination product group | Share of intermediate uses | Imported share within group |
|---|---:|---:|
| Food and beverage services | 29.1% | 36.7% |
| Dairy products | 24.3% | 47.0% |
| Other food and beverages | 21.0% | 51.3% |
| Other products and services | 14.9% | 34.6% |
| Education, health and government services | 7.1% | 32.5% |
| Other manufactures | 3.7% | 33.4% |

Source: same MIP row, intermediate cells D196:AFE196. Grouping rules are explicit in `data/DICTIONARY.md` and implemented in `analyze.py`; they are analytical categories, not official institutional sectors.

These allocations help locate links that merit closer investigation when assessing a product-specific policy. They do not establish how quickly users can substitute inputs or how a price change would transmit. Those questions require elasticities, technological assumptions and compatible price data.

## Final uses and an important reconciliation

Private consumption accounts for 103,960.152 million pesos, or 97.9% of gross final uses. Exports account for 2,376.022 million pesos, or 2.2%. Changes in inventories equal **−162.465 million pesos**, offsetting part of the other uses. Government consumption, fixed capital formation and the statistical discrepancy are zero in this row. Negative inventory changes must remain in the accounting sum; replacing them with zero would change the denominator.

MIP_10, the combined-origin table, presents imports with a negative sign in its final-demand block. Its published final total is 84,412.694, including imports of −21,761.015. Removing this netting entry reconciles gross final uses to **106,173.709**. This is a presentation bridge, not an additional demand flow. The script checks both the origin sum and this independent combined-table reconciliation.

Private consumption is the published national-accounts component. It is not a supermarket-sales statistic. The product row cannot establish retail outlet shares or the incidence across household income groups.

## A separate broader comparison

The supply-and-use tables (COU) report a **17.6%** intermediate-use share for category **3115**, covering the broader dairy category. Its intermediate uses are 44,212.476 million pesos and total uses 251,870.392. COU columns classify buyer industries, whereas this MIP exercise uses product groups. The difference from the MIP 311513 share of 14.5% is not evidence of an inconsistent revision: category breadth and matrix dimensions differ. The code retains the two universes separately.

## Implications and limits

The practical result is a reproducible exposure map with separate total-use, intermediate-use and origin denominators. Before applying an import-policy scenario, an analyst should establish which products and origins are actually affected, whether the affected users can substitute inputs, and whether the 2018 structure remains appropriate. The accounting shares alone cannot quantify output losses, welfare effects or price pass-through.

No multiplier is estimated from this row extract, and no counterfactual forecast is presented. This bounded result can support model selection and data requests without implying that the missing causal analysis has already been done.

Sources and exact workbook cells are documented in [sources.json](sources.json). The offline reproduction command is `python analyze.py`; the optional independent cell extractor requires the six original public workbooks of the recorded vintages.
