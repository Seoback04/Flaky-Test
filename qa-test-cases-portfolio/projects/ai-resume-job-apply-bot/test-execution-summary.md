# Test Execution Summary — AI Resume Job Apply Bot — 0.9.0-rc1
_Owner_: QA Portfolio &nbsp;|&nbsp; _Generated_: 2026-03-25 &nbsp;|&nbsp; _Build_: 0.9.0-rc1
## 1. Scope Tested
- Resume ingestion (PDF, DOCX, TXT).
- LLM-driven profile extraction (mock + real).
- Field detection + mapping engine.
- Autofill for text / select / file / radio / checkbox.
- Safe-submit gate (low-confidence, missing required, dry-run).
- Screenshot capture.
- PII masking in logs.
- CAPTCHA detection abort path.
## 2. Summary
| Metric | Count |
|---|---|
| Total test cases | 24 |
| Passed | 22 |
| Failed | 1 |
| Blocked | 0 |
| Not Run | 1 |
| Pass % (of executed) | 95.6% |
## 3. Coverage by Type
| Type | Planned | Executed | Passed | Failed |
|---|---|---|---|---|
| functional | 13 | 13 | 13 | 0 |
| negative | 5 | 5 | 4 | 1 |
| boundary | 1 | 1 | 1 | 0 |
| edge | 1 | 1 | 1 | 0 |
| error-path | 1 | 1 | 1 | 0 |
| security | 1 | 1 | 1 | 0 |
## 4. Coverage by Risk
| Risk | Planned | Executed | % Executed |
|---|---|---|---|
| High | 19 | 19 | 100% |
| Medium | 5 | 4 | 80% |
## 5. Key Defects
| Bug ID | Title | Severity | Priority | Status |
|---|---|---|---|---|
| BUG-JOBBOT-001 | Phone mapped into Fax field | S1 | P1 | Fixed |
| BUG-JOBBOT-002 | DEBUG logs leak PII | S1 | P1 | Fixed |
| BUG-JOBBOT-003 | `--dry-run` ignored on URLs with query strings | S1 | P1 | Triaged |
## 6. Top Risks Still Open
- **BUG-JOBBOT-003** — violates the safe-submit safety contract. Ship-blocker.
- LLM provider drift in production (temperature / model updates) — mitigated by schema validation + retry.
## 7. Deviations From Plan
- TC-JOBBOT-017 (required-field block) required a broader decision-table pass; 2 hours added to schedule.
## 8. Release Recommendation
**No-Go until BUG-JOBBOT-003 is fixed and verified.**
**Rationale**: Submissions firing despite an explicit `--dry-run` flag is a safety-contract violation (S1). All other High-risk cases pass.
**Conditions for re-evaluation**:
- Land the fix, pass TC-JOBBOT-019, add regression test, rerun High-risk suite.
## 9. Known Limitations
- No support for sites requiring OAuth or multi-factor auth flows.
- CAPTCHA detection triggers abort; no automated bypass.
- LLM latency can push end-to-end flow to > 30 s on slow networks.
## 10. Sign-off
| Role | Name | Date |
|---|---|---|
| QA Owner | QA Portfolio | 2026-03-25 |
| Tech Lead | — | Pending BUG-JOBBOT-003 fix |
| PM | — | — |
