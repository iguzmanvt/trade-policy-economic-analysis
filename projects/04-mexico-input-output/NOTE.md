# Import exposure depends on the use being measured

Isaac Guzmán Valdivia Tovar | P04 | Reviewed 26 October 2026 | Data: 2018

**Imported origin: 41.5% of intermediate uses; 17.5% of all gross uses.**

## Question and trade-policy relevance

How does imported-origin exposure differ between intermediate and total uses of Mexico's dairy-derivatives category, and which destination product groups account for its intermediate demand?

In the 2018 accounts, the imported-origin share of intermediate uses is 41.5%, against 17.5% for all gross uses. Food and beverage services, dairy products, and other food and beverages account for 74.3% of intermediate demand. These distinctions help identify where to investigate the consequences of a product-specific trade-policy change. They establish the allocation of recorded uses; a price or output response requires additional evidence. [1]

## A product row with explicit denominators

The National Institute of Statistics and Geography (INEGI) publishes the 2018 input-output matrix (MIP, its Spanish acronym). This exercise uses its symmetric, product-by-product table and the class associated with code 311513 in the North American Industry Classification System, Mexico 2018 (SCIAN). The official label is “Elaboración de derivados y fermentos lácteos”. It covers dairy derivatives and fermented dairy products, including cheese and imitation cheese; it does not isolate cheese names. Rows record products used; intermediate columns represent homogeneous destination product groups. Values are millions of pesos at basic prices for 2018. [1, 3]

| Product origin | Intermediate uses | Final uses | All gross uses | Intermediate / that origin |
| --- | --- | --- | --- | --- |
| Domestic | 10,564.919 | 91,919.823 | 102,484.742 | 10.3% |
| Imported | 7,507.129 | 14,253.886 | 21,761.015 | 34.5% |
| Both origins | 18,072.048 | 106,173.709 | 124,245.757 | 14.5% |

Table 1. All values except the last column are million pesos. The last column divides intermediate uses by all uses of the same row. Both origins means domestic plus imported, counted once. Source: MIP_19 and MIP_38, Tabulado, row 196; author calculations.

The 41.5% ratio is 7,507.129 / 18,072.048: imported intermediate uses divided by intermediate uses of both origins. The 17.5% ratio is 21,761.015 / 124,245.757: all imported-origin uses divided by all gross uses. In contrast, 34.5% is 7,507.129 / 21,761.015: the share of imported-origin uses that goes to intermediate demand.

Intermediate uses account for 14.5% of gross uses, while final uses account for 85.5% and have an imported-origin share of 13.4%. This composition explains the lower aggregate import share. “Gross uses” means uses before the combined table's imports-netting adjustment; it includes exports and signed inventory changes. It is not a measure of imported content in production or foreign value added.

## Where intermediate demand is concentrated

The snapshot retains all 834 intermediate destinations for each origin, including the 745 zero-flow destinations in the combined row. The 89 positive destinations are assigned once to six exhaustive analytical groups using SCIAN code prefixes. The figure separates domestic and imported values within each group. [1]

![Intermediate uses of MIP 311513 by destination product group and origin, 2018.](figures/intermediate_destination_origins.png)

Figure 1. Each bar sums domestic and imported uses of category 311513. The groups describe destination products, not individual purchasing firms or retail channels. All six groups and exact values are in results/intermediate_destination_groups.csv.

| Destination product group | Share of all intermediate uses | Imported share of 311513 uses in group |
| --- | --- | --- |
| Food and beverage services | 29.1% | 36.7% |
| Dairy products | 24.3% | 47.0% |
| Other food and beverages | 21.0% | 51.3% |

Table 2. The first percentage uses all intermediate demand of 311513 as its denominator. The second uses only the total 311513 flow into that destination group, not all inputs used by the group.

The largest destination and the highest imported share answer different screening questions. Food and beverage services has the largest flow, 5,250.707 million pesos, with 36.7% imported origin. Other food and beverages has a smaller flow but an imported share of 51.3%. These results identify different links to examine. Neither ranks vulnerability: a large flow may be readily replaceable, while a smaller specialised input may face few substitutes.

## Reconciliation and a separate comparison

Domestic plus imported values equal the combined-origin intermediate row in every destination, and destination sums equal 18,072.048 million pesos. Final components sum to 106,173.709: private consumption is 103,960.152 (97.9% of final uses), exports 2,376.022, and inventory change -162.465. Government consumption, fixed capital and the statistical discrepancy are zero. The negative inventory value remains in the final-use and gross-use totals. [1]

MIP_10 includes a negative imports entry in its final-demand block. The bridge is **84,412.694 - (-21,761.015) = 106,173.709** million pesos of gross final uses. Adding 18,072.048 of intermediate uses gives 124,245.757 of gross uses. This restores the same gross accounting presentation as the domestic-plus-imported sum; the negative imports entry is not an extra demand flow.

The supply-and-use tables (COU, their Spanish acronym) provide a separate comparison for the broader SCIAN branch 3115, “Elaboración de productos lácteos”. The row is a product category; columns identify user industries. Its 44,212.476 million pesos of intermediate uses divided by 251,870.392 of total uses gives **17.6%**. This is the intermediate-use share of another category, not another imported-origin proportion. It cannot be treated as a revision of MIP 311513's 14.5% share. [2, 3]

## The next economic question

For a specified change in market access, which affected dairy inputs could users replace, at what cost and over what period? The accounts organise that inquiry, but do not answer it. A focused follow-up would link the affected products and countries of origin of imports to the destination groups, then assemble the evidence below.

| Economic question | Additional evidence required |
| --- | --- |
| Which flows face the policy? | Tariff-line concordance to 311513; affected products, countries of origin of imports, policy provisions and dates. |
| Can users substitute? | Product specifications and quantities, domestic and imported prices, supplier switching, contracts, available capacity and substitution elasticities. |
| What are compliance costs? | Firm or product evidence on certification, testing, labelling and administration; fixed versus recurring costs and adjustment time. |
| How do prices and output respond? | The input share in each user's total costs; import, producer and consumer prices; exchange rates, margins, market structure, inventories and compatible output data. |

Updated supply-and-use or transaction evidence would also be needed to assess how far the 2018 structure remains applicable. Estimating indirect production requirements would require the relevant complete matrix and stated assumptions; identifying a causal policy effect would require a credible comparison design. The present result closes as a reproducible accounting decomposition. It identifies no firms, retail channels, named cheeses or bilateral suppliers, and estimates no substitution, compliance cost, price transmission or production effect.

Source verification. All 6 official workbooks were downloaded again on 26 October 2026; all 6 hashes match the archived files. The 2,557 selected cells agree, with 0 differences. This checks the selected extraction, not every account in the full matrices. The original 2018 reference year and 29 August 2023 workbook metadata remain unchanged. See sources.json, data/workbook_provenance.json and VALIDATION.md for exact identities and execution scope.

### Sources

[1] INEGI. MIP 2018, product-by-product, class level. MIP_19, MIP_38 and MIP_10; Tabulado row 196. [Available at: https://www.inegi.org.mx/programas/mip/2018/](https://www.inegi.org.mx/programas/mip/2018/)

[2] INEGI. COU 2018, basic-price use, branch level. COU_177, COU_184 and COU_170; Tabulado row 48. [Available at: https://www.inegi.org.mx/programas/cou/2018/](https://www.inegi.org.mx/programas/cou/2018/)

[3] INEGI. SCIAN Mexico 2018, printed pp. 150-151 (PDF pp. 169-170), categories 3115 and 311513. [Available at: https://inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/702825099695.pdf](https://inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/702825099695.pdf)
