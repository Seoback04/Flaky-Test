# QA Workflow
This document explains the end-to-end flow from **requirement landed** to **release signed off**, and how the artifacts in this repository hang together.
## The Lifecycle
```
 Requirement
     │
     ▼
 Risk Analysis ──► risk-analysis.md
     │
     ▼
 Test Plan    ──► test-plan.md
     │
     ▼
 Scenarios    ──► test-scenarios.md       (IDs: TS-*)
     │
     ▼
 Test Cases   ──► test-cases.csv          (IDs: TC-*)
     │
     ├──► Test Data    ──► test-data.md
     └──► Traceability ──► traceability-matrix.csv
     │
     ▼
 Execution
     │
     ├──► Defects      ──► bug-report-samples.md (IDs: BUG-*)
     └──► Summary      ──► test-execution-summary.md
```
Every arrow is auditable: every test case links back to a scenario, which links back to a requirement.
## Step 1 — Requirement Ingestion
Inputs: product spec, ticket, design doc, API contract.
Output: a flat list of `REQ-<PROJECT>-NNN` items with a short description and acceptance criteria.
## Step 2 — Risk Analysis
For each requirement, assign:
- Likelihood (H/M/L).
- Impact (H/M/L).
- Risk = max(likelihood, impact) when both ≥ M, else min.
High-risk items drive **must-pass** test cases; low-risk items drive **sampled** test cases.
## Step 3 — Test Plan
Defines:
- Scope (what is / is not tested).
- Approach (functional, negative, boundary, non-functional mix).
- Environments, roles, schedule.
- Entry / exit criteria.
- Deliverables.
## Step 4 — Scenarios (`TS-*`)
A scenario is a user-meaningful workflow or behavioral area (e.g., *"classify tests after a mixed-outcome run"*). Scenarios link 1:N to test cases.
## Step 5 — Test Cases (`TC-*`)
Each case is reduced to a deterministic set of steps with an expected result. Test cases live in `test-cases.csv` with these columns:
`Test Case ID | Module | Feature | Title | Preconditions | Test Steps | Test Data | Expected Result | Actual Result | Priority | Severity | Type | Automation Candidate | Status | Notes`
## Step 6 — Test Data
Documented in `test-data.md`:
- Valid inputs (representatives of each EP class).
- Invalid inputs (malformed, empty, too large).
- Edge cases (min, max, unicode, duplicates).
- Special values (nulls, zero, negatives where meaningful).
## Step 7 — Traceability Matrix
A CSV mapping `REQ-* → TS-* → TC-* → Status`. A requirement with no test case is a coverage gap. A test case with no requirement is waste.
## Step 8 — Execution
1. Run High-risk cases first.
2. On failure: open a defect, link it in the test case's `Notes`, move on.
3. Retest fixed defects with the original steps + a regression variant.
4. Log Status (Pass / Fail / Blocked / Not Run / N/A).
## Step 9 — Defect Reporting
See `docs/bug-reporting-guidelines.md`. One bug = one defect. File in the project's `bug-report-samples.md` or in the team's issue tracker.
## Step 10 — Execution Summary
Aggregate into `test-execution-summary.md`:
- Scope tested.
- Totals: Passed / Failed / Blocked / Not Run / N/A.
- Key defects (IDs + severities).
- Top risks still open.
- **Release recommendation**: Go / Conditional Go / No-Go, with rationale.
- Known limitations (so stakeholders aren't surprised later).
## Handling Change
- **Requirement changes**: update the `REQ-*` entry → fan out updates to linked scenarios/cases (matrix shows the blast radius).
- **Spec drift during execution**: note in `test-execution-summary.md` under "Deviations."
- **Flaky test cases**: use the Flaky Test Detector; do not keep re-running until green — that's how real bugs get masked.
## Automation Handoff
Each test case has an `Automation Candidate` column (Yes / No / Later):
- **Yes** = stable expected output, worth automating now.
- **Later** = will be automated once the feature stabilizes.
- **No** = exploratory/usability in nature; manual forever.
Automated cases should reference their code location in `Notes`, so the map from `TC-*` to actual pytest/selenium/cypress code is explicit.
## Cadence
- **Per PR**: smoke regression (High-risk cases, short path).
- **Per sprint**: full regression + exploratory charters.
- **Per release**: full plan + non-functional pass + execution summary + sign-off.
## Definition of Done for a QA Pass
- All High-risk cases have a `Pass` status.
- Any `Fail` has an open bug linked.
- Traceability matrix shows 100% requirement coverage.
- `test-execution-summary.md` is committed with a clear recommendation.
- Known limitations are written in plain language, not buried in logs.
