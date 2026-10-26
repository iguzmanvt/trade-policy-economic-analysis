# Reviewing access and fiduciary evidence for loss and damage finance

**Independent policy analysis by Isaac Guzmán Valdivia Tovar. Prepared 26 October 2026.**

This work sample translates selected FRLD policy decisions into a compact evidence review structure. Its central recommendation is to preserve a visible chain from the applicable policy to the evidence, the unresolved issue and the person authorized to decide it.

Read the [policy note](POLICY_NOTE.md) first. The [policy register](data/policy_register.csv) contains eight status records; the [review matrix](data/review_matrix.csv) contains twelve analyst-designed checks in three modules: authority and access, funds and implementation, and financing and results. The proposed evidence requests are analytical suggestions, not additional FRLD requirements.

The review uses the Governing Instrument, selected B.8 decision excerpts and the Board's report published by UNFCCC on 19 October 2026. That report covers developments through **31 July 2026**. Publication and retrieval dates do not extend its reporting period. The [source register](sources.json) specifies document status, locators and retrieval limits.

No applicant, country, entity or funding request is assessed. All case evidence states remain `not_assessed`. The package produces no readiness score, eligibility determination, functional equivalency decision or legal opinion, and is not an official FRLD tool.

## Check the files

Python 3 standard library only, from any working directory:

```bash
python projects/06-frld-operational-review/validate.py
```

The command checks identifiers, source relationships and status labels and writes [results/validation.json](results/validation.json). These are document-integrity checks, not an automated review of substantive fiduciary evidence. See [VALIDATION.md](VALIDATION.md).
