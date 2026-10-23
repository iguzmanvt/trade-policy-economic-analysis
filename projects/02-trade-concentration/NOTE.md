# North American exposure in the U.S. goods trade network

Isaac Guzmán Valdivia Tovar | 22 October 2026

## Question and main result

Does U.S. merchandise trade become more concentrated across foreign partners, and does greater concentration necessarily mean greater exposure to Canada and Mexico? The two measures can move differently. This example separates the country distribution of U.S. general imports and total exports from the shares specifically involving its two North American partners.

In January–August 2026, reconstructed from archived monthly observations, the import partner Herfindahl–Hirschman Index (HHI) was 703.8 and the export destination HHI was 628.8, on a 0–10,000 scale. Canada and Mexico jointly represented 28.5% of covered general imports and 30.4% of covered total exports. Export destination concentration declined from 2023, as did the combined North American export share. Imports show a different sequence: concentration fell through 2025 and then rose in 2026, while remaining below its 2023 level.

## Measurement and evidence

The universe is all reported individual ten-digit merchandise product codes, aggregated across products to individual Census country identifiers. General imports use customs value. Total exports include domestic exports plus reexports, using free alongside ship (FAS) value. Each flow has its own retained individual-partner denominator; no import/export ratio or balance is constructed. These are nominal, unadjusted goods statistics, excluding services. The archive covers all reported individual partners in its scope; a fresh reconciliation to an official world aggregate was not performed. [1–3]

HHI equals 10,000 times the sum of squared **individual partner** shares. Canada and Mexico remain separate terms. For the regional share, their values are added and divided by that same flow's all-partner total. Territories/economies are retained as individual Census partners; world and regional aggregates are excluded. Pooling the many smaller partners before squaring would artificially increase measured concentration.

| January–August | Import partner HHI | Export destination HHI | Canada + Mexico / imports | Canada + Mexico / exports |
|---|---:|---:|---:|---:|
| 2023 | 740.8 | 745.4 | 29.1% | 34.0% |
| 2024 | 723.8 | 727.1 | 28.5% | 33.5% |
| 2025 | 628.7 | 660.0 | 26.4% | 31.6% |
| 2026 | 703.8 | 628.8 | 28.5% | 30.4% |

Source: archived U.S. Census monthly statistics; author’s calculations from the included partner extract. These are sums of archived monthly observations, not direct revised cumulative `_YR` fields. The periods are seasonally comparable January–August windows.

## What changes inside the regional share?

The stable-looking import share of Canada and Mexico between 2023 and 2026 masks opposite partner movements. Mexico's share rose from 15.46% to 17.36%, while Canada's fell from 13.62% to 11.16%. Their combined share declined by 0.55 percentage points. In exports, Mexico's share was 16.22% in 2023 and 16.07% in 2026; Canada's fell from 17.83% to 14.28%. A regional total can therefore conceal a material shift in the balance between the two partners.

The 2025–2026 change provides a second view. U.S. general imports rose by 95.48 billion dollars in this archived comparison. Mexico contributed 64.87 billion dollars, or 67.9% of the net increase, while Canada contributed 10.88 billion dollars, or 11.4%. China’s decline of 35.82 billion dollars contributed −37.5%. Taiwan and Vietnam contributed 71.0% and 55.9%, respectively. These contributions legitimately add to more than 100% across selected growing partners because declines elsewhere offset some of the gross gains. They describe an accounting decomposition, not estimated trade diversion.

Total U.S. exports rose by 207.03 billion dollars. Mexico accounted for 18.1% of that increase and Canada for 3.5%. Positive trade growth with a partner does not ensure a rising share: the denominator can expand faster. This explains how North American export values can increase while the regional share falls.

## Policy relevance

Partner concentration and regional exposure answer different policy questions. HHI summarizes how unevenly a flow is distributed across counterparties. The Canada–Mexico share instead identifies the portion directly involving those two markets or suppliers. Monitoring both helps distinguish a broad redistribution across foreign partners from a shift within North America.

For country surveillance, the next step would connect the gross goods flows to domestic production, investment, employment and value added, and assess the relevant demand or supply shocks. This sample supports choosing where to investigate exposure. It does not establish the welfare benefit of diversification, the existence of a specific supply chain, tariff causality, origin compliance or transshipment. U.S.-reported shares also do not measure Mexico's or Canada's overall dependence on the United States; that requires their own all-destination/all-origin denominators.

## Reproducibility and limits

The package contains 1,846 flow–partner–period totals for four January–August windows and new standard-library Python code. It regenerates the HHI, every partner share, the signed growth decomposition and a vector figure. Key uniqueness, country-code coverage, nonnegative values, positive denominators and share/contribution sums are checked. A separate floating-point calculation checked the headline HHI and regional shares against the decimal implementation.

The partner totals were recovered from a previously executed public-statistics aggregation of 64 archived monthly product-level partitions. Only the all-goods universe is used here; prior bespoke selections, original employer code and prose are excluded. Hashes of the actual August 2026 import and export monthly source files were recomputed and matched their recorded hashes. The other upstream hashes were inherited from the source audit and were not rechecked in this continuation. The archive generation date does not establish each original download timestamp. Earlier months retain their archived vintages; no successful new live refresh or reconciliation to current revised Census totals is claimed. Full upstream product-month files are not bundled, so offline reproduction covers the supplied partner extract and subsequent arithmetic.

## Official references

[1] [U.S. Census Bureau — Description of the International Trade Statistical Program](https://www.census.gov/foreign-trade/guide/sec2.html). See general imports, export valuation, partner definitions and statistical coverage.

[2] [U.S. Census Bureau — Imports HS variable definitions](https://api.census.gov/data/timeseries/intltrade/imports/hs/variables.html). General customs value and monthly/year-to-date fields.

[3] [U.S. Census Bureau — Exports HS variable definitions](https://api.census.gov/data/timeseries/intltrade/exports/hs/variables.html). Total export values and monthly/year-to-date fields.

[4] [U.S. Census Bureau — Guide to International Trade Datasets](https://www.census.gov/foreign-trade/reference/guides/Guide_to_International_Trade_Datasets.pdf). Query syntax and detailed trade dataset use.
