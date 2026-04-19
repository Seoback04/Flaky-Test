# Test Strategy
## Purpose
This document defines the shared test strategy used across every project in this portfolio. It is intentionally pragmatic: enough structure to be professional, not so much ceremony that documentation rots.
## Objectives
1. Establish confidence that each feature behaves as specified on happy paths.
2. Prove that negative, boundary, and error paths are handled safely.
3. Make coverage auditable via traceability (requirement → scenario → case).
4. Produce defensible release recommendations based on executed evidence.
5. Surface non-functional risks (performance, reliability, observability, security) explicitly.
## Scope
In scope:
- Functional testing (UI, CLI, API, analytics).
- Negative and error-path testing.
- Boundary and edge-case testing.
- Regression testing of previously released features.
- Selected non-functional testing (performance, reliability, robustness, usability, security).
- Exploratory testing under charter-based sessions.
Out of scope:
- Load testing at internet-scale (noted under *Limitations* per project).
- Full penetration testing (only surface-level security considerations).
- Localization testing (projects are English-only here).
## Test Levels
| Level | Responsibility | Artifacts |
|---|---|---|
| Unit | Developer-authored; enforced at PR review | N/A here |
| Integration | Shared between dev + QA | scenarios, traceability |
| System | QA-owned | test plans, cases, execution reports |
| Acceptance | Stakeholder + QA | execution summary, release recommendation |
## Test Types Covered
- **Functional** — feature behaves as spec'd on positive paths.
- **Negative** — invalid inputs, malformed payloads, missing auth, offline state.
- **Boundary** — min/max values, empty collections, max-length strings, zero-byte files.
- **Regression** — existing features still work after changes.
- **Exploratory** — charter-driven, time-boxed, session-noted.
- **Non-functional** — performance, reliability, robustness, observability, usability, security.
## Prioritization Model (Risk-Based)
Each feature is assigned a **risk level** = `likelihood × impact`.
| Risk | Definition | Execution policy |
|---|---|---|
| High | User-visible, blocking, or data-integrity-related | Every release, blocking for Go |
| Medium | Noticeable but recoverable | Every release, non-blocking for Go |
| Low | Cosmetic / rarely hit | Sampled across releases |
Test cases inherit the risk of their feature and are scheduled accordingly.
## Severity vs Priority
- **Severity** — how bad is this defect from a product/user standpoint? (S1 critical → S4 cosmetic)
- **Priority** — how soon must we fix it? (P1 now → P4 whenever)
These are **independent** axes. A typo in the marketing homepage can be S4/P1. A rare data-loss bug can be S1/P3 if the repro is non-trivial.
## Entry / Exit Criteria
**Entry (can QA begin?)**
- Build deployed to a reachable environment.
- Smoke tests pass locally.
- Requirements/spec frozen for the scope under test.
- Test environment + test data ready.
**Exit (can we call it done?)**
- All High-risk test cases executed; 0 open S1/S2 defects.
- ≥ 95% of Medium-risk cases executed; no open S2 defects.
- Execution summary + release recommendation produced.
- Known limitations explicitly documented.
## Environments
- **Dev** — developer machines; used for sanity and exploratory.
- **CI** — ephemeral containers; used for automated regression.
- **Staging** — production-parity; used for full system + non-functional passes.
- **Prod** — post-release smoke only.
## Tooling
- Manual test management: markdown + CSV in this repository (versioned with git).
- Execution tracking: `Status` column per test case (Not Run / Pass / Fail / Blocked / N/A).
- Bug tracking: templated markdown files in `bug-report-samples.md` (would be Jira/Linear in a team setting).
- Reporting: `test-execution-summary.md` per project.
## Roles
| Role | Responsibility |
|---|---|
| QA owner | Test plan, test cases, traceability, execution summary |
| Developer | Unit coverage, bug triage, fixes |
| Tech lead | Risk sign-off, release recommendation approval |
| PM | Accept known limitations, sign off go/no-go |
## Deliverables (Per Project)
- `test-plan.md`
- `test-scenarios.md`
- `test-cases.csv`
- `traceability-matrix.csv`
- `bug-report-samples.md`
- `test-execution-summary.md`
- `risk-analysis.md`
- `test-data.md`
- `non-functional-tests.md`
## Success Metrics
- **Coverage**: % of requirements linked to at least one test case (target: 100%).
- **Execution rate**: % of planned cases executed per release.
- **Escaped defect rate**: defects found post-release vs pre-release.
- **Defect leakage per severity**: number of S1/S2 that escaped.
- **Re-open rate**: % of defects re-opened after "fixed".
