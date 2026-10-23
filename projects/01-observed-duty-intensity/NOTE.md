# Observed duty intensity and the interpretation of trade reallocation

Isaac Guzmán Valdivia Tovar | 22 October 2026

Analytical writing sample

## Main finding

U.S. imports for consumption from Mexico in three selected computer and network equipment lines rose from $53.90 billion in January–August 2025 to $113.10 billion in the corresponding 2026 period, an increase of 109.8%. Observed duty intensity in 2026 was far lower for Mexico than for China, but Taiwan, Vietnam and Malaysia also faced low ratios. The evidence supports examining supplier-specific tariff incentives; it does not establish that tariffs caused this growth in U.S. imports from Mexico.

## Scope and measurement

The comparison covers three 10-digit Harmonized Tariff Schedule (HTS10) lines and five suppliers. January–August totals are reconstructed from 240 archived monthly observations, with eight months in each product–country–year cell. Duty intensity equals 100 × calculated duties ÷ customs value of imports for consumption. It is a ratio of sums. Product labels below are shortened for readability; the exact codes define the selection. [1–3]

## 1. Observed duty intensity, January–August 2026

Percent of customs value; reconstructed from archived monthly observations.

| Product / HTS10 | Mexico | China | Taiwan | Vietnam | Malaysia |
| --- | --- | --- | --- | --- | --- |
| Processing units — 8471500150 | 0.024 | 27.125 | 0.032 | 0.109 | 0.332 |
| Storage units — 8471709000 | 0.002 | 27.670 | 0.154 | 0.007 | 1.233 |
| Switching / routing — 8517620020 | 0.112 | 26.381 | 0.020 | 0.017 | 0.011 |

Source: archived U.S. Census extracts; author’s calculations. These are observed ratios, not statutory tariff rates or final net customs revenue. [1–3]

## 2. U.S. imports for consumption from Mexico

January–August of each year; nominal U.S. dollars, billions except growth.

| Product / HTS10 | 2025 | 2026 | Change |
| --- | --- | --- | --- |
| Processing units — 8471500150 | 49.04 | 99.00 | 101.9% |
| Storage units — 8471709000 | 1.95 | 6.89 | 253.4% |
| Switching / routing — 8517620020 | 2.91 | 7.20 | 147.8% |
| Three-line total | 53.90 | 113.10 | 109.8% |

Source: same archived extracts. Totals may differ from sums of rounded entries. The three lines are a selected illustration, not a comprehensive electronics or data-center basket.

## What the comparison supports

The relevant benchmark depends on the competing supplier. In 2026, China’s observed ratios ranged from 26.381% to 27.670%, while Mexico’s ranged from 0.002% to 0.112%. The corresponding gap is large. Against Taiwan, Vietnam and Malaysia, however, Mexico’s differences were much smaller; for switching and routing equipment, Mexico’s ratio was slightly higher than all three. A claim of a broad tariff advantage would obscure these comparisons. Earlier changes may still matter: Mexico’s switching and routing ratio fell from 3.216% in 2025 to 0.112% in 2026. The comparison does not rule out effects of policy changes or expectations.

The growth is also concentrated. Processing units accounted for 84.4% of the increase in U.S. imports from Mexico within this three-line selection. Gross nominal trade values do not distinguish quantities from prices, reveal domestic value added or establish final use. Such concentration calls for examining product demand, production capacity and imported content before drawing conclusions about economy-wide growth.

## Implications for country analysis

For a country team, the immediate question is whether the trade expansion represents durable additions to productive capacity and domestic income, or a mix of higher prices, imported content and supplier substitution. Relevant follow-up indicators include investment and capacity utilization, employment, import intensity, export destination concentration and exposure to U.S. demand. These would connect a trade development to growth, external vulnerability and policy uncertainty.

Policy advice should separate facilitation measures that address demonstrated bottlenecks from incentives justified only by a temporary tariff gap. Infrastructure and customs performance warrant assessment when capacity evidence supports it. Any proposed fiscal incentive would require a separate appraisal of additional investment, budget cost, implementation capacity and spillovers; the descriptive comparison here does not establish its benefits.

## Next analytical step

An expanded study would construct a monthly product–supplier panel, date statutory tariff changes and relevant exemptions, and test whether import shares changed differentially with policy exposure. A credible design would examine pre-trends, common demand shocks, changes in product composition and policy endogeneity. Comparison suppliers can themselves respond to trade diversion, so they are not automatically valid controls. This is a proposed research agenda; no causal effect has been estimated in this sample.

## Reproducibility, vintage and sources

The accompanying repository contains 30 aggregated input rows, a standard-library Python script and unrounded results. Coverage and arithmetic were checked, including a separate recomputation. Earlier months retain their archived vintages, so these sums can differ from subsequently revised Census year-to-date fields. A fresh API verification was attempted but did not complete. Reproduction therefore applies to the included snapshot, not to the latest live release.

[[1] U.S. Census — International Trade Imports HS variable definitions](https://api.census.gov/data/timeseries/intltrade/imports/hs/variables.html)

[[2] U.S. Census — Foreign Trade statistical definitions](https://www.census.gov/foreign-trade/guide/sec2.html)

[[3] U.S. Census — Guide to International Trade Datasets](https://www.census.gov/foreign-trade/reference/guides/Guide_to_International_Trade_Datasets.pdf)
