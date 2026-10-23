# P02B — Product concentration in a fixed U.S. import basket from Mexico

This is the product-basket perspective of [P02 — trade concentration](../README.md). The complementary [partner perspective](../NOTE.md) covers all goods across individual foreign partners. These are two subanalyses of one project, with different dimensions and denominators; their Herfindahl–Hirschman indices must not be joined into one series.

**Question.** Which products account for the change in U.S. general imports from Mexico within a fixed research basket, and how concentrated are those values?

**Result.** January–August reported values rise from **93.602 billion dollars in 2025 to 153.705 billion dollars in 2026**. Three selected tariff lines account for **99.64% of the 60.103 billion dollar increase**. The product Herfindahl–Hirschman Index (HHI), on a 0–10,000 scale after aggregating selected lines into 88 six-digit groups, rises from **2,853.09 to 4,289.04**. These results describe a selected gross trade flow, not economy-wide growth or a causal tariff effect.

![Absolute contributions to the change](figures/contributions.svg)

## Scope and selection

- Reporter: United States; partner: Mexico (Census country code `2010`).
- Flow: **general imports**, which differs from the imports-for-consumption measure used by P01.
- Selection: the explicitly published, frozen author-defined list in `data/basket_hts10.csv`: **374 historical Harmonized Tariff Schedule ten-digit (HTS10) codes**, grouped into **88 Harmonized System six-digit (HS6) categories**. This does not assert coverage of every tariff line within those 88 categories.
- The research basket includes computing, communications, storage, electrical, cooling and ancillary goods with multiple potential uses. It is a retrospective research selection, not a representative statistical sample or a verified data-center end-use classification. No causal interpretation relies on the selection process.
- Periods: January–August of 2025 and 2026. Monetary amounts: nominal U.S. dollars. We sum reported monthly values, retaining their archived vintages.
- Recovered input: **4,794 monthly observations**, covering all 16 month-periods. There are 328 observed HTS10 lines in 2025, 344 in 2026 and 356 across both windows. The 88 selected HS6 groups have reported values in both windows.
- Newly introduced codes outside the frozen list are excluded. Old selected codes remain eligible when reported. Absence of a record is retained as absence; it is not converted into a measured zero or evidence that a product ceased to exist.

## Reproduce

Python 3.9 or later; **standard library only**. From this directory:

```sh
python analyze.py
```

The script reads only bundled data, checks hashes, scope, keys and coverage, and regenerates all CSV/JSON results plus `figures/contributions.svg`. It makes no network requests. Values are computed with integer dollars and high-precision decimal ratios. The recovery archive was read on October 22, 2026 (Mexico City date). This run does not establish the source's original download date or the latest official revision.

## Files

| File | Purpose |
| --- | --- |
| `NOTE.md` | Original English analytical note, interpretation and limits |
| `DATA_DICTIONARY.md` | Local field/output guide and link to the shared contract |
| `analyze.py` | Executed reproducible computation and figure generation |
| `data/general_imports_monthly.csv` | Sanitized monthly panel; no private source paths |
| `data/basket_hts10.csv` | Exact frozen membership list and original product descriptions |
| `sources.json` | Archive and derived-input hashes, coverage and retrieval scope |
| `results/contributions.csv` | Three leading lines and residual; absolute and relative contributions |
| `results/composition_hs6.csv` | Composition of selected lines after grouping at HS6 |
| `results/concentration.csv` | Product HHI and effective number of equal-sized groups |
| `results/reported_hts10_sums.csv` | Reported sums and number of reported months by line and year |
| `results/monthly_totals.csv` | Comparable-window monthly totals |
| `results/summary.json`, `results/checks.json` | Unrounded results and checks actually executed |
| `figures/contributions.svg` | Reproducible, self-contained vector figure |

The common definitions and cross-project statistical boundary are in [the shared Census dictionary](../../census-common/DATA_DICTIONARY.md) and [source notes](../../census-common/SOURCES.md). The [P01 consumption sample](../../01-observed-duty-intensity/README.md) and this product-basket general-import sample must not be added together or substituted for each other. The [flow bridge](../../census-common/results/flow_comparison.csv) matches only the three shared lines and comparison periods; it does not merge the universes.

## Measurement and rights

These are **January–August totals reconstructed from archived monthly observations**, not a new download of official cumulative `_YR` fields. Current reproduction verifies this archived panel and arithmetic; it does not certify the latest official release or revalidate P01's 240 original monthly consumption records.

The data originate from the U.S. Census Bureau's International Trade statistics. Official definitions and retrieval documentation: [HS imports variables](https://api.census.gov/data/timeseries/intltrade/imports/hs/variables.html), [statistical definitions](https://www.census.gov/foreign-trade/guide/sec2.html), [dataset guide](https://www.census.gov/foreign-trade/reference/guides/Guide_to_International_Trade_Datasets.pdf). Source data and official descriptions retain their original terms; the license below applies only to original code and prose.

Copyright 2026 Isaac Guzmán Valdivia Tovar. Original code and prose are provided under the MIT License; see `LICENSE`. No blanket relicensing of Census materials is intended.
