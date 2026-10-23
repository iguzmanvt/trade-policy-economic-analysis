# Documenting non-tariff measures affecting cheese trade

**Isaac Guzmán Valdivia Tovar · Prepared 22 October 2026**

**Question.** How can a textual trade-barrier inventory distinguish mechanisms, recurring issues and market-access safeguards without turning mentions into a count of proven violations?

**Result.** This independent public sample codes **18 edition–issue observations**, representing **eight issues**, **five mechanism categories** and **seven country/regional chapters** in the **2024–2026 National Trade Estimate (NTE)** reports of the Office of the United States Trade Representative (USTR). Twelve observations report ongoing concerns; six record a market-access assurance, arrangement or prior-user safeguard. Repeated mentions are connected through stable issue identifiers. These counts describe the selected records, not global barrier prevalence.

[Read the analytical note](NOTE.md) · [Inspect the coding](data/nte_cheese_sample.csv) · [Read the dictionary](DICTIONARY.md) · [Review sources](sources.json)

## Scope and selection

The effective prior research covered editions 2007–2026 and mentions of cheese across countries and regions. This release reconstructs a **purposive recent sample** from official public PDFs, using new summaries, taxonomy and code. It does not release the earlier project corpus or claim comprehensive coverage of any edition. Selected issues demonstrate ingredient rules, conformity assessment, internal taxation, geographical indications and shelf-life regulation; repeated records support temporal comparisons. Names extend beyond any nine-name selection, including Danbo, Havarti and white cheeses.

Chapters: Canada, Chile, Dominican Republic, European Union, Gulf Cooperation Council, Mexico and Vietnam. The Qatar records identify both the regional chapter and the actual jurisdiction. Every row has printed-page and physical PDF-page references. A year absent for an issue means **not coded in this sample**, not absence of a measure.

## Reproduce offline

Python 3.11 or later; standard library only:

```bash
python analyze.py
```

The command validates the included coding and regenerates `results/topic_summary.csv`, `selected_coverage.csv`, `issue_continuity.csv`, `temporal_cases.csv` and `summary.json`. Paths resolve relative to the script, so it also runs from the portfolio root. The inputs are manual analytical coding, not automated extraction or an estimated barrier index.

Optional upstream verification requires `pypdf`:

```bash
python -m pip install -r requirements-source-verification.txt
python verify_sources.py --source-dir /path/to/nte-pdfs --download
```

The optional command downloads the three official PDFs if missing, verifies their hashes and page counts, and checks the 18 textual page anchors. For source files already available, omit `--download`. It writes `results/source_verification.json`. A changed official PDF fails explicitly; review a source revision before changing stored hashes. No key or account is required.

## Interpretation and publication

NTE reports present the U.S. government's reported concerns and policy perspective. A mention is neither a World Trade Organization finding nor an estimate of economic cost. Repeated language is not proof of continued enforcement; a changed legal citation is not proof of a new restriction. Market-access safeguards must not be coded as newly imposed barriers. No client reports, original client code, private actor records or full PDFs are included. This package is complete for its bounded sample and awaits the author's public-release approval.

[Execution and verification record](EXECUTION.md).
