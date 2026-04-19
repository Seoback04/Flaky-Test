# Test Scenarios — Flaky Test Detector
Scenarios group related test cases around a user-meaningful behavior. Each scenario links to one or more requirements and fans out to concrete test cases in `test-cases.csv`.
## TS-FLAKY-001 — Stable Pass Classification
Verify that tests passing in every executed run are classified as `stable_pass` and excluded from worst-offender lists.
_Requirements_: REQ-FLAKY-001
_Test cases_: TC-FLAKY-001
## TS-FLAKY-002 — Stable Fail Classification (Non-Infra)
Verify that tests failing in every executed run with non-infra error messages are classified as `stable_fail`.
_Requirements_: REQ-FLAKY-002
_Test cases_: TC-FLAKY-002
## TS-FLAKY-003 — Flaky Classification
Verify that tests with mixed pass/fail outcomes (non-infra dominated) are classified as `flaky`.
_Requirements_: REQ-FLAKY-003
_Test cases_: TC-FLAKY-003, TC-FLAKY-004
## TS-FLAKY-004 — Infra-Suspect Classification
Verify that failures whose messages match infra keywords (timeout, connection error, 503, webdriver, etc.) are classified as `infra_suspect`, whether all-failing or mixed.
_Requirements_: REQ-FLAKY-004
_Test cases_: TC-FLAKY-005, TC-FLAKY-006
## TS-FLAKY-005 — Flakiness Score Computation
Verify `min(pass,fail)/executed` for representative and boundary inputs.
_Requirements_: REQ-FLAKY-005
_Test cases_: TC-FLAKY-007, TC-FLAKY-008, TC-FLAKY-009
## TS-FLAKY-006 — Transition Count Logic
Verify transitions count only pass↔fail state changes and ignore skipped runs.
_Requirements_: REQ-FLAKY-006
_Test cases_: TC-FLAKY-010, TC-FLAKY-011
## TS-FLAKY-007 — Duration Variance Metric
Verify average and stddev of per-run durations; zero-stddev case; high-variance case flagged.
_Requirements_: REQ-FLAKY-007
_Test cases_: TC-FLAKY-012, TC-FLAKY-013
## TS-FLAKY-008 — Report Generation
Verify summary.json, test_metrics.csv, top_flaky.csv, raw_history.csv, and report.html are produced with the expected schema.
_Requirements_: REQ-FLAKY-008
_Test cases_: TC-FLAKY-014, TC-FLAKY-015
## TS-FLAKY-009 — Chart Generation
Verify all 5 PNGs are produced and non-zero-sized when data exists; placeholder chart when data is empty.
_Requirements_: REQ-FLAKY-009
_Test cases_: TC-FLAKY-016, TC-FLAKY-017
## TS-FLAKY-010 — Malformed Input Handling
Verify parser raises `ParserError` for corrupt JSON, missing files, and non-dict payloads without crashing the CLI.
_Requirements_: REQ-FLAKY-010
_Test cases_: TC-FLAKY-018, TC-FLAKY-019
## TS-FLAKY-011 — Partial Run Failure Handling
Verify the runner continues after individual run failures, logs the error, and analyzer works on the subset that succeeded.
_Requirements_: REQ-FLAKY-011
_Test cases_: TC-FLAKY-020
## TS-FLAKY-012 — CLI Argument Validation
Verify that out-of-range or malformed CLI arguments are rejected with a clear error.
_Requirements_: REQ-FLAKY-012
_Test cases_: TC-FLAKY-021, TC-FLAKY-022
## TS-FLAKY-013 — Output File / Directory Creation
Verify that running on a fresh checkout creates `outputs/raw/`, `outputs/summary/`, `outputs/charts/`.
_Requirements_: REQ-FLAKY-013
_Test cases_: TC-FLAKY-023
