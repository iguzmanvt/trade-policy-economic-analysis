# Data dictionary and coding contract

Unit: one selected issue, jurisdiction and NTE edition. Each row has one primary mechanism; a paragraph may discuss several concerns. Summaries are new English paraphrases.

| Field | Meaning |
|---|---|
| `record_id` | Unique stable issue identifier plus edition year |
| `edition_year` | NTE report edition; distinct from a legal measure's adoption date |
| `report_chapter` | Official country/regional chapter containing the passage |
| `jurisdiction` | Actual jurisdiction discussed; Qatar is within the Gulf Cooperation Council chapter |
| `issue_id` | Stable identifier joining repeated discussion of the same selected issue |
| `topic` | One of five mutually exclusive primary mechanism categories in `taxonomy.csv` |
| `product` | Product scope of the passage, including broader cheese/dairy inputs when explicitly connected |
| `printed_pages` | Page label printed within the report; en dash denotes inclusive range |
| `pdf_pages` | Physical PDF page number, starting at 1; en dash denotes inclusive range |
| `source_id` | Key to `sources.json` |
| `source_url` | Official report PDF URL |
| `anchor` | Short literal phrase used by the optional source check to locate the reviewed passage |
| `reported_status` | Analytical status of the passage, defined below |
| `source_instrument` | Instrument cited in the passage, or `Not separately identified in coded passage`; not independently verified law |
| `summary` | Original concise paraphrase attributed to USTR's report |
| `verification` | Page-level reading and anchor verification status |

`ongoing_concern` means the report expresses a continuing concern without a selected safeguard in the coded passage. `concern_with_market_access_assurance` retains both the concern and an assurance. `market_access_arrangement_reported` records an arrangement that mitigates the concern. `prior_user_safeguard_monitoring` records monitoring of eligibility/access under a prior-user provision. These are textual classifications, not legal adjudications or severity rankings.

There are no zero-filled country–year cells. An unlisted issue/edition is outside the released coding. All 18 records are verified positives. Repeated editions share an `issue_id`; they must not be summed as distinct measures. The taxonomy groups heterogeneous mechanisms for documentation, not for estimating a common ad valorem equivalent.
