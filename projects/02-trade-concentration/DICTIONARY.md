# Data dictionary and measurement rules

This dictionary covers the **partner view** of P02. See the [product view](product-basket/README.md) and [common dictionary](../census-common/DATA_DICTIONARY.md) for the separate product dataset and flow bridge.

## Input: `data/partner_values.csv`

| Field | Definition |
|---|---|
| `flow` | `M`: U.S. general imports; `X`: U.S. total exports, domestic plus reexports |
| `period` | `YYYY-01_08`: sum of archived January–August monthly observations |
| `country_code` | Four-digit Census partner identifier, stored as text; individual reported partner, 1000–7999 |
| `country_name` | Descriptive Census label from the archive; key is the numeric identifier |
| `iso3` | Archive partner label; descriptive, not an aggregation key |
| `value_usd` | Nonnegative integer nominal U.S. dollars; general imports at customs value or total exports at FAS value |

Unique key: `flow, period, country_code`. The universe includes all reported individual ten-digit merchandise product codes within each flow and period. It excludes world/region aggregates. No special product basket is applied. Product-level statistical special provisions are retained within the all-goods universe.

These totals come from reported product–partner entries. A partner absent from a complete flow-period extract has no recorded value in that extract; for the signed change decomposition only, its value is zero. A present zero is kept as zero. A malformed/blank numeric field raises an error; it is never replaced with zero. Archive completeness is inherited from upstream coverage checks; there is no new live source certification.

## Formulas

For each flow-period, `T = sum(value_usd)` over the individual partner rows. Partner share `s_i = value_i/T`.

- HHI = `10,000 × sum(s_i²)`. Individual partner squares are summed, including small partners; a pooled "rest of world" is never squared.
- Effective equal-sized partners = `10,000 / HHI`.
- Canada + Mexico share = `100 × (value_1220 + value_2010)/T`.
- Top-five share = sum of the five largest individual partner shares.
- Positive partners = number with a strictly positive reported total.
- Partner contribution to 2025–2026 net change = `100 × (value_2026 − value_2025)/(T_2026 − T_2025)`. Signed contributions sum to 100%; individual contributions can exceed 100% when others are negative.

All calculations use decimal arithmetic with 40-digit working precision. Output CSV decimal strings retain calculation precision; prose/figures round only for presentation. Shares are percentages; HHI is on the 0–10,000 scale. North America here means the **two foreign U.S. partners Canada and Mexico**. The United States is the reporting economy, so it is not another foreign partner in its own trade denominator.

## Outputs

`concentration_summary.csv` has one flow-period row and total value, HHI, effective partners, positive partners, Canada share, Mexico share, combined share and top-five share. `partner_shares.csv` repeats input metadata and adds each share and squared-share HHI contribution. `growth_contributions_2025_2026.csv` has one flow-partner row and both values, signed change and percentage of total net change. `validation.json` identifies the exact included input by SHA-256 and states the validation scope.
