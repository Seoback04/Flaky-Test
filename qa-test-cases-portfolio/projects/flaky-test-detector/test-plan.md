# Test Plan — Flaky Test Detector
_Version_: 1.0 &nbsp;|&nbsp; _Owner_: QA Portfolio &nbsp;|&nbsp; _Target release_: 1.x
## 1. Introduction
Validate the Flaky Test Detector across its end-to-end pipeline: repeatedly execute a pytest suite, produce structured JSON reports, aggregate metrics, classify tests, detect patterns, and emit reports + charts. This plan prioritizes **analytics correctness** and **robustness under malformed or partial data**, because both directly affect release decisions downstream.
## 2. Objectives
- Prove classification logic is deterministic and matches the decision-table specification.
- Validate flakiness score, transition count, streak, and duration metric math against hand-computed expected values.
- Surface robustness gaps for malformed / missing / partial inputs.
- Ensure report and chart artifacts are produced and non-empty.
- Validate CLI argument parsing and defaults.
## 3. Scope
**In scope**
- Classifier (`stable_pass / stable_fail / flaky / infra_suspect / unknown`).
- Metrics (flakiness score, transitions, streaks, duration stddev).
- Pattern detectors.
- Parser (pytest-json-report → domain models).
- Reporter (JSON, CSV, HTML).
- Visualizer (5 matplotlib charts).
- CLI (`run`, `analyze`, `report`, `demo`).
- Partial-run / missing-report fault tolerance.
**Out of scope**
- Running the detector against thousands of tests at production scale.
- Long-lived soak testing (>24h).
- Security pen-testing (tool is local, no network surface).
## 4. Test Approach
| Dimension | Approach |
|---|---|
| Functional | Positive + negative + boundary for every classifier rule and metric. |
| Regression | High-risk cases rerun each release. |
| Robustness | Malformed JSON, partial runs, missing dirs, unicode nodeids. |
| Non-functional | Performance on 200-run × 200-test synthetic datasets. |
| Exploratory | Charter: "break the analyzer with weird pytest outputs". |
## 5. Test Design Techniques
- **Decision tables** for the classifier (every rule = 1 test case).
- **EP + BVA** for `--runs` and `--delay` arguments.
- **Negative testing** for parser input (corrupt JSON, empty array, wrong schema).
- **Error guessing**: unicode nodeids, Windows paths with spaces, concurrent writes.
## 6. Deliverables
As listed in [docs/qa-workflow.md](../../docs/qa-workflow.md).
## 7. Environments
| Env | Notes |
|---|---|
| Dev (Windows / macOS / Linux) | primary |
| CI (Linux container) | automated regression |
| Staging | N/A — tool runs locally against CI artifacts |
## 8. Schedule
| Phase | Exit |
|---|---|
| Design | scenarios + cases committed |
| Execution | High-risk cases Pass; no open S1/S2 |
| Sign-off | `test-execution-summary.md` committed |
## 9. Entry Criteria
- `pip install -r requirements.txt` succeeds.
- `pytest tests/` passes on main.
- Demo suite runs without crash.
## 10. Exit Criteria
- 100% of High-risk test cases Pass.
- 0 open S1/S2 defects.
- Report + charts produced cleanly on a 10-run demo.
## 11. Risks
See `risk-analysis.md`.
## 12. Assumptions
- Python 3.11+ available.
- Disk I/O is not constrained.
- Clock is reasonably accurate for duration metrics.
