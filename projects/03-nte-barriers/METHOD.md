# Method, coverage and exclusions

## Units and selection

This method uses National Trade Estimate (NTE) reports of the Office of the United States Trade Representative (USTR). The evidence unit is **source edition × selected issue**, with a stable issue ID, report chapter, actual jurisdiction, source file and pages. An issue ID links a policy problem; it does not prove that legal instruments or implementation are unchanged. In particular, `CHL-PRIOR-USERS` follows common-name access concerns and the later arrangement. Its 2024 record does not assert a prior-user safeguard already in force.

The fixed selection comprises eight previously public issues. This release retains their 18 original IDs, adds Chile 2024 from another official PDF variant, and reviews the remaining five cells. The grid is 8 × 3 = 24 cells. It is complete **for the declared observation grid and review protocol**, not for all cheese mentions in seven chapters. This is purposive selection to compare mechanisms, source positions and temporal interpretation. It supports no sampling-based inference about countries or prevalence.

The selected mechanisms are composition standards, conformity assessment, reported differential internal taxation, geographical indications and shelf-life regulation. They include restrictions related to inputs used in cheese production and reported access safeguards. Border tariffs, tariff-rate quotas, unrelated dairy measures and other jurisdictions are outside this fixed selection. A UAE processed-cheese measure on NTE 2026 printed p. 240 is outside the Qatar issue.

## Search and review

`data/search_terms.csv` is a new small public dictionary for this panel. Direct product terms include cheese and names such as Danbo, Havarti and mozzarella. Mechanism terms help retrieve context but do not independently establish a cheese connection. Text was searched case-insensitively with whitespace normalization, followed by reading the relevant passage and adjacent material. Contextual terms such as `grandfather` or `conformity assessment` can match unrelated information and communications technology, telecommunications or medical-device rules; those passages were excluded from the cheese issue.

Positive rows were re-read from the official PDFs. Every numerical statement used in the note has a source locator: the Dominican 18 percent refers to reported internal Tax on Transfer of Industrial Goods and Services (ITBIS) taxation, the Qatar 45 days to reported maximum white-cheese shelf life, and the Vietnam date to prior-user eligibility. None is a new estimated effect. The Chile event chronology uses additional official sources separately from the panel.

Five initially uncoded cells were resolved by reading full chapters, not by treating zero search hits as proof. The negative review scope is precisely recorded in `coverage_review.csv`: Dominican Republic 2026; Mexico 2025 and 2026; Vietnam 2024 and 2025. Their state is `SECTION_REVIEWED_NO_MENTION`, qualified to the **selected issue**. The Mexico chapters still contain cheese in the geographical-indication discussion.

| Coverage state | Meaning |
|---|---|
| `CODED_SOURCE_REVIEWED` | Selected issue positively identified and coded after source reading. |
| `SECTION_REVIEWED_NO_MENTION` | The stated section/chapter was read; no mention of the selected issue was found. No inference about the measure's legal status. |
| `SEARCH_NO_MATCH` | A search found no candidate; manual review has not established a negative result. Reserved state, not used in this completed grid. |
| `DOCUMENT_NOT_REVIEWED` | No completed content review. Reserved state, not used in this completed grid. |

An absent chapter in a particular PDF is a document-availability issue, not a reviewed non-mention. For Chile 2024 the additional official PDF supplies positive evidence, and the file distinction is retained.

## Source versions and dates

The 392-page `2024 NTE Report.pdf` is preserved for all existing 2024 records. Its Canada chapter is followed by a blank page and China; it has no Chile chapter. The 394-page `2024 NTE Report_1.pdf` supplies Chile pp. 49–50 / PDF pp. 57–58 under `NTE-2024-ALT394`. Their hashes, filenames and URLs differ. Other page positions also differ, so the files cannot share locators. We did not establish a revision date or formal supersession.

Printed and physical PDF page numbers are stored separately; PDF numbering is one-based. No fixed offset is imposed. In the baseline 2024 file, Mexico printed pp. 252–254 correspond to PDF pp. 258–260, while earlier examples use different offsets. Every page of a positive record's range has at least one explicit locator check and a printed-page check.

The coordinating reference date is 22 October 2026. Actual recovery, downloads, source review and execution occurred on 26 October 2026, America/Mexico_City. The report editions are 2024–2026. This is not a reconstruction of the exact website state on the reference date; in particular the added 2024 variant's historical availability was not dated. The original source metadata and the new verification event are distinguished in `sources.json`.

## Reproduction and what it proves

`analyze.py` regenerates results from disclosed manual coding. It checks uniqueness, edition/source consistency, valid categories and statuses, jurisdiction/chapter mappings, ranges and correspondence between positive evidence and the 24-cell coverage grid. It does not execute the earlier professional research or require personal paths.

`verify_sources.py` verifies four official source files against stored hashes and page counts, then checks printed labels and short page-specific anchors. A hash mismatch stops verification; review the changed file rather than quietly accepting it. The command does not certify all report contents or legal accuracy. Supplementary Chile materials were read through the official web sources and are not part of the four-PDF automated verification receipt.

There is no automated barrier-severity score. Duplicate control concerns edition–issue keys and source/locator/issue combinations; a shared page may legitimately contain more than one issue. Descriptive counts have this selected sample as their denominator and no economic interpretation.

## Limits

NTE is the U.S. government's account. A concern is not a World Trade Organization judgment; a committee discussion is not adjudication. A proposal is not an implemented obligation. Repetition is not proof of continuing enforcement; omission is not repeal. A changed legal citation can reflect an actual new instrument, but the NTE passage alone does not measure its incremental effects. A safeguard may be conditional and does not prove access for all users. The release makes no claims about damages, willingness to pay, tariff equivalents, welfare, causal trade effects or a complete twenty-edition corpus.
