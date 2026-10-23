# Executed validation

Prepared 22 October 2026, Mexico City time.

The public exercise was independently rebuilt from six unmodified public INEGI workbooks recovered with the prior corrected exercise. New extraction code, analysis code and English prose were written for this portfolio; no prior client report or original client script is included.

Executed:

1. `python extract_cells.py SOURCE_DIRECTORY`: extracted 2,557 cells from six original workbooks, including 834 intermediate destinations for each MIP origin. Verified row category headers, and recorded exact workbook hashes, titles and cell addresses.
2. `python analyze.py`: regenerated all four result CSVs and the validation JSON with no external dependencies. Passed unique-key, finite-value and full destination checks.
3. Summed all 834 destinations and reconciled each origin's intermediate total; verified domestic + imported = combined for every destination.
4. Reconciled final components with each origin's final total, retained negative inventory changes, and checked final + intermediate = all uses for domestic and imported origin.
5. Checked the independent MIP_10 import-netting bridge for gross final and all uses; verified origin identities in the separate COU 3115 controls.
6. Source pages, SCIAN definition and INEGI reuse terms were opened. Classification confirmed on printed page 151 / PDF page 170. Workbook header metadata verified directly. Public source metadata and Spanish labels are retained in the extract and provenance register.

Result: 124,245.757 million pesos of gross uses; 18,072.048 intermediate; 106,173.709 final; imported share of intermediate 41.5400014431%. Exact output and input hash: `results/validation.json`.

Not established: a fresh download of the binary workbooks was not completed. Original download timestamps are unavailable; hashes identify the archived workbooks actually inspected. The main source pages resolve, but their interactive table list was not text-readable in the web retrieval. The workbook titles, internal metadata, classification and arithmetic are directly verified. This workflow does not certify a newer vintage.

No causal effect, country-specific import allocation or multiplier has been inferred. The offline snapshot reproduces the delivered accounting results; re-extraction requires the same external official workbooks.
