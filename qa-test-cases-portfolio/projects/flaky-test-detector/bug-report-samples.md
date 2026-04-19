# Bug Report Samples — Flaky Test Detector
Three representative defect reports demonstrating severity/priority discipline and reproducible steps.
---
## BUG-FLAKY-001 — [Classifier] Mixed outcomes with all-infra failures misclassified as `flaky`
| Field | Value |
|---|---|
| **Bug ID** | BUG-FLAKY-001 |
| **Reported on** | 2026-03-11 |
| **Build / Version** | 1.0.0 / pre-release |
| **Environment** | Windows 11 / Python 3.13 / fresh venv |
| **Severity** | S2 |
| **Priority** | P1 |
| **Frequency** | Always |
| **Status** | Verified (fixed) |
| **Linked Test Case** | TC-FLAKY-006 |
| **Linked Requirement** | REQ-FLAKY-004 |
### Preconditions
- Detector installed; demo suite available.
### Steps to Reproduce
1. Produce 10 synthetic runs where 6 pass and 4 fail with the message `"Request timed out after 30s"`.
2. Invoke `analyze(suite_runs)`.
3. Inspect the category for that test.
### Expected Result
Category is `infra_suspect` (all failures match infra keyword `timeout`, ratio = 1.0 ≥ 0.5 threshold).
### Actual Result
Category is `flaky`. Rationale cites mixed outcomes but does not reference infra keywords.
### Impact
Release decisions based on the category column would wrongly treat an environmental flake as product flakiness, sending engineers to debug phantom regressions.
### Root Cause Hypothesis
`classify_one` evaluated the `infra_dominated` branch only for all-fail cases; the mixed-outcome branch did not re-check infra dominance.
### Notes
- Unit test added: `tests/test_classifier.py::test_flaky_dominated_by_infra_is_infra_suspect`.
- Regression fence in place.
---
## BUG-FLAKY-002 — [Parser] Corrupt JSON crashes entire `analyze` command instead of skipping the broken file
| Field | Value |
|---|---|
| **Bug ID** | BUG-FLAKY-002 |
| **Reported on** | 2026-03-12 |
| **Build / Version** | 1.0.0 |
| **Environment** | Linux / Python 3.11 |
| **Severity** | S2 |
| **Priority** | P2 |
| **Frequency** | Always |
| **Status** | Fixed |
| **Linked Test Case** | TC-FLAKY-018 |
| **Linked Requirement** | REQ-FLAKY-010 |
### Preconditions
- `outputs/raw/` contains 10 valid `run_*.json` files and one corrupt file `run_006.json` with content `{not json`.
### Steps to Reproduce
1. Run `python main.py analyze --input outputs/raw`.
### Expected Result
CLI logs a warning for `run_006.json`, skips it, and continues; produces analysis based on the remaining 9 runs.
### Actual Result
CLI aborts with an unhandled `ParserError` and exit code 1; no report is produced.
### Impact
A single bad file in a large CI archive discards all analysis output, forcing a manual cleanup pass before retry.
### Root Cause Hypothesis
`cli._load_suite_runs_from_raw` does catch parser errors, but the underlying exception bubbled up earlier through an `Exception` propagation that wasn't caught.
### Notes
- Fixed by wrapping the parse call in a broad `except Exception`, logging, and continuing.
- Added test coverage in `test_parser.py::test_parse_invalid_json_raises`.
---
## BUG-FLAKY-003 — [Visualizer] `heatmap.png` not produced when a test appears in only a subset of runs
| Field | Value |
|---|---|
| **Bug ID** | BUG-FLAKY-003 |
| **Reported on** | 2026-03-15 |
| **Build / Version** | 1.0.0 |
| **Environment** | macOS 14 / Python 3.12 |
| **Severity** | S3 |
| **Priority** | P3 |
| **Frequency** | Intermittent (≈20%) |
| **Status** | Triaged |
| **Linked Test Case** | TC-FLAKY-016 |
| **Linked Requirement** | REQ-FLAKY-009 |
### Preconditions
- Run the detector against a suite where a test is filtered out mid-session by a dynamic `-k` selector on alternating runs.
### Steps to Reproduce
1. `python main.py run --tests demo --runs 10 -k "not browser"` (simulating intermittent presence).
2. Open `outputs/charts/heatmap.png`.
### Expected Result
Heatmap renders all tests × 10 runs, with missing cells shown in neutral color.
### Actual Result
Heatmap renders with uneven rows and a logged `IndexError: list index out of range` from `chart_heatmap`.
### Impact
Users lose the visual instability map when test membership is not stable across runs (a realistic CI scenario).
### Root Cause Hypothesis
`chart_heatmap` assumes every nodeid appears in every run; missing entries are not defaulted to a neutral value.
### Notes
- Proposed fix: treat missing (nodeid, run_index) as `Outcome.SKIPPED` → matrix value 0.
- Will add regression test using sparse synthetic data.
