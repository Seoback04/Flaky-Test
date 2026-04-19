# Test Execution Summary — Flaky Test Detector — 1.0.0
_Owner_: QA Portfolio &nbsp;|&nbsp; _Generated_: 2026-03-20 &nbsp;|&nbsp; _Build_: 1.0.0 (commit 2351190)
## 1. Scope Tested
- Classifier (all 5 categories).
- Metrics (flakiness score, transitions, streaks, duration avg/stddev).
- Pattern detectors (7 detectors).
- Parser (happy + malformed inputs).
- Reporter (JSON, CSV, HTML).
- Visualizer (5 PNGs).
- CLI argument validation and output directory creation.
## 2. Summary
| Metric | Count |
|---|---|
| Total test cases | 23 |
| Passed | 20 |
| Failed | 0 |
| Blocked | 0 |
| Not Run | 3 |
| Pass % (of executed) | 100% |
## 3. Coverage by Type
| Type | Planned | Executed | Passed | Failed |
|---|---|---|---|---|
| functional | 10 | 10 | 10 | 0 |
| boundary | 4 | 4 | 4 | 0 |
| negative | 4 | 4 | 4 | 0 |
| edge | 2 | 1 | 1 | 0 |
| error-path | 1 | 1 | 1 | 0 |
| reliability | 1 | 0 | 0 | 0 |
| regression | automated via `pytest tests/` (33 tests) | 33 | 33 | 0 |
## 4. Coverage by Risk
| Risk | Planned | Executed | % Executed |
|---|---|---|---|
| High | 17 | 15 | 88% |
| Medium | 5 | 4 | 80% |
| Low | 1 | 1 | 100% |
## 5. Key Defects
| Bug ID | Title | Severity | Priority | Status |
|---|---|---|---|---|
| BUG-FLAKY-001 | Mixed + all-infra misclassified as flaky | S2 | P1 | Verified |
| BUG-FLAKY-002 | Corrupt JSON crashes `analyze` | S2 | P2 | Fixed |
| BUG-FLAKY-003 | Heatmap crashes on sparse nodeid membership | S3 | P3 | Triaged |
## 6. Top Risks Still Open
- **Sparse heatmap input** (BUG-FLAKY-003) — cosmetic-to-medium; triaged.
- **No fault-injection harness** (TC-FLAKY-020 not yet automated) — reliability claim partially unverified.
- **Non-functional performance baseline** — measured once at 200 runs × 200 tests; not in CI.
## 7. Deviations From Plan
- TC-FLAKY-017 (empty-data chart rendering) deferred — low risk.
- TC-FLAKY-020 (partial-run fault injection) requires a small harness, promoted to a follow-up story.
## 8. Release Recommendation
**Conditional Go for 1.0.0.**
**Rationale**: All High-risk classifier, metrics, and report cases pass. Two S2 defects were fixed and regression-fenced. The remaining open item (BUG-FLAKY-003) is S3 and does not block the primary JSON/CSV/HTML outputs — only the heatmap under a specific filtering pattern.
**Conditions**:
- Document the heatmap limitation in the README "Limitations" section until BUG-FLAKY-003 ships.
- Land TC-FLAKY-020 automation within the next release cycle.
## 9. Known Limitations
- N < ~5 runs → weak flakiness signal (expected, documented).
- Infra-keyword heuristic is English-only.
- Heatmap renders poorly when test membership varies across runs (BUG-FLAKY-003).
- Performance not CI-gated.
## 10. Sign-off
| Role | Name | Date |
|---|---|---|
| QA Owner | QA Portfolio | 2026-03-20 |
| Tech Lead | — | — |
| PM | — | — |
