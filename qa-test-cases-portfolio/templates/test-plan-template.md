# Test Plan — <Project Name>
_Version_: 1.0 &nbsp;|&nbsp; _Owner_: <QA owner> &nbsp;|&nbsp; _Last updated_: YYYY-MM-DD
## 1. Introduction
One paragraph: what is this project, what is being validated in this plan, and why now.
## 2. Objectives
- Prove <feature area A> meets acceptance criteria.
- Validate negative and boundary behavior for <feature area B>.
- Surface non-functional risks: <list>.
- Produce a release recommendation with supporting evidence.
## 3. Scope
**In scope**
- <functional area 1>
- <functional area 2>
- <selected non-functional axes>
**Out of scope**
- <items deferred>
- <items owned by another team>
## 4. Test Approach
| Dimension | Approach |
|---|---|
| Functional | Positive, negative, boundary, edge |
| Regression | High-risk test cases rerun each build |
| Non-functional | <performance / reliability / usability / security> |
| Exploratory | Charter-based, time-boxed sessions |
| Automation | Stable cases marked `Automation Candidate = Yes` |
## 5. Test Design Techniques Applied
- Equivalence partitioning, boundary value analysis.
- Decision tables for <feature>.
- State transition for <feature>.
- Error guessing on <hot spots>.
- Risk-based prioritization (see `risk-analysis.md`).
## 6. Deliverables
- `test-scenarios.md`
- `test-cases.csv`
- `traceability-matrix.csv`
- `test-data.md`
- `bug-report-samples.md`
- `test-execution-summary.md`
- `risk-analysis.md`
- `non-functional-tests.md`
## 7. Environments
| Env | Purpose | Notes |
|---|---|---|
| Dev | Sanity | local |
| CI | Automated regression | ephemeral |
| Staging | Full system pass | prod-parity |
| Prod | Post-release smoke | read-only checks |
## 8. Roles & Responsibilities
| Role | Owner |
|---|---|
| QA Lead | <name> |
| Developer on call | <name> |
| Release Manager | <name> |
## 9. Schedule
| Phase | Start | End | Exit condition |
|---|---|---|---|
| Test design | | | scenarios + cases signed off |
| Execution | | | all High-risk cases executed |
| Defect fixing | | | no open S1/S2 |
| Sign-off | | | execution summary approved |
## 10. Entry Criteria
- Build deployed and reachable.
- Smoke tests pass.
- Test data + environment ready.
- Spec frozen for the scope under test.
## 11. Exit Criteria
- All High-risk cases executed; 0 open S1/S2.
- ≥ 95% of Medium-risk cases executed.
- Execution summary + recommendation produced.
## 12. Risks & Mitigations
See `risk-analysis.md`.
## 13. Assumptions
- <assumption 1>
- <assumption 2>
## 14. References
- Product spec: <link>
- Design doc: <link>
- Requirements list: `traceability-matrix.csv`
