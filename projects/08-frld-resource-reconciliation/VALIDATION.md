# Validation record

Reviewed and executed on 26 October 2026.

## Source and calculations

- The local official advance report matched the SHA-256 in `sources.json`. The original PDF is not included in the public module.
- Both receipt figures were inspected on the rendered source pages: PDF page 5 (printed page 3) and PDF page 15 (printed page 13). Their USD 0.20 million difference remains unresolved.
- The extract contains 18 unique metric IDs, including five explicit unavailable amounts. Missing values remain blank.
- Source units, reference dates, integer counts, finite values, evidence statuses and page-number offsets are validated.
- The request-count and funding-request-allocation identities reconcile exactly. No requirement forces receipt values to agree.
- `analyze.py` passed in normal mode and with `python -O`, from outside the project directory. The four result files were byte-identical between runs when the same optional PDF verification was supplied.

## Failure behavior

`python -m unittest discover -s tests -v` passed all 10 named tests, with each test exercising normal and optimized execution: **20 subprocess cases**. The cases cover a valid extract, duplicate IDs, a missing metric, a missing amount coded as zero, a changed reference date, inconsistent request counts, inconsistent allocations, non-finite values, incorrect units, and loss of the pipeline's reported precision.

Each invalid case returned a failure before changing pre-existing outputs. Two additional executions, normal and optimized, rejected a PDF with the wrong source hash and preserved previous output bytes. See [results/execution_checks.json](results/execution_checks.json).

`PASS` means the included extract and calculations satisfy these checks. It does not resolve the source discrepancy, establish an actual cash balance or validate the Fund's underlying financial transactions.
