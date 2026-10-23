# Source register and vintage policy

Statistical information cutoff: 22 October 2026, America/Mexico_City. Canonical-path integration review: 23 October 2026. This review date does not refresh the underlying statistics. The components reproduce archived inputs, not a newly certified live Census release.

| Layer / source | Role | Verification boundary and detailed register |
|---|---|---|
| P01 consumption snapshot | 30 product–supplier–period aggregate inputs | Included hash and arithmetic checked in its effective delivery. The previously documented 240 upstream monthly records are not supplied or newly revalidated. [P01 provenance and scope](../01-observed-duty-intensity/sources.json) |
| P02A archived individual-partner totals | All-goods general imports and total exports, January–August 2023–2026 | Separate 1,846-row extract and retained-partner denominators. Coverage and upstream verification limits remain those of the effective partner analysis. [Partner source register](../02-trade-concentration/sources.json) |
| P02B separately recovered monthly general-import extract and fixed research selection | 4,794 monthly records from Mexico, January–August 2025 and 2026; 374 historical ten-digit Harmonized Tariff Schedule (HTS10) lines grouped into 88 six-digit Harmonized System (HS6) categories | Included sanitized-input hashes and prior recovery provenance retained. These records do not replace or certify P01's consumption input or P02A's all-goods partner universe. [Product-basket source register](../02-trade-concentration/product-basket/sources.json) |
| [Census statistical definitions](https://www.census.gov/foreign-trade/guide/sec2.html) | Meaning of flows, customs value and calculated duties | Read in the original component preparation, especially sections 3, 6, 18 and 19. Documentation verification is distinct from checking the latest trade values. |
| [Census International Trade API User Guide](https://www.census.gov/foreign-trade/reference/guides/Guide_to_International_Trade_Datasets.pdf) | Field names and API conventions | Read in the original preparation; identifies `CAL_DUT_MO`, `CON_VAL_MO` and `_YR` variants. No fresh numerical retrieval is attributed to this integration. |
| [Imports HS API variables](https://api.census.gov/data/timeseries/intltrade/imports/hs/variables.html) | Public schema reference | The incoming common documentation recorded a timed-out direct retrieval during its preparation; no live statistical check is inferred. The retained partner and P01 registers document their own separate documentation checks. |

Calculated duties need not equal duties paid. The Census guide's treatment of reported Chapter 99 duties, antidumping and countervailing duties and possible understatement limits interpretation of P01 as a comprehensive policy-cost measure.

Each component's metadata identifies its effective input hash, archive basis and verification scope. A date in a directory name is an archive label, not proof of the original official download timestamp. Revised year-to-date values must not replace archived monthly sums without an explicit version comparison. The [shared dictionary](DATA_DICTIONARY.md) distinguishes the flows, product/partner denominators and absence conventions.

## Integration and rights

The flow bridge uses [P01's canonical consumption input](../01-observed-duty-intensity/data/census_snapshot.csv) and [P02B's canonical monthly general-import input](../02-trade-concentration/product-basket/data/general_imports_monthly.csv). It creates a six-row descriptive comparison; it neither uses nor revises the P02A partner series. The module is support, not another completed project.

The quantitative inputs are public Census statistical facts and a disclosed research selection. No client report, correspondence, API key or private path belongs in this public tree. [The common license](CODE_LICENSE.txt) applies only to its original Python code. [P02B's license](../02-trade-concentration/product-basket/LICENSE) applies only to its original code and prose; it does not relicense Census data, official descriptions or other third-party material. Neither license extends to the other portfolio components. Preserve each source's attribution and terms.
