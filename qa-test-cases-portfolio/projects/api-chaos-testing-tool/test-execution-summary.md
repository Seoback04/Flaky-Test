# Test Execution Summary — API Chaos Testing Tool — 0.8.0
_Owner_: QA Portfolio &nbsp;|&nbsp; _Generated_: 2026-04-02 &nbsp;|&nbsp; _Build_: 0.8.0
## 1. Scope Tested
- OpenAPI parsing (valid + malformed).
- Payload generation (valid, type-swap, oversized, null/missing, injection).
- Chaos injection (timeout, 5xx).
- Executor (concurrency, latency, NDJSON logging).
- Stability scoring (formula + determinism).
- CLI argument validation.
## 2. Summary
| Metric | Count |
|---|---|
| Total test cases | 17 |
| Passed | 16 |
| Failed | 0 |
| Blocked | 0 |
| Not Run | 1 (Windows timing recheck pending hotfix) |
| Pass % (of executed) | 100% |
## 3. Coverage by Type
| Type | Planned | Executed | Passed | Failed |
|---|---|---|---|---|
| functional | 8 | 8 | 8 | 0 |
| negative | 5 | 5 | 5 | 0 |
| boundary | 1 | 1 | 1 | 0 |
| security | 1 | 1 | 1 | 0 |
| reliability | 1 | 1 | 1 | 0 |
| performance | 1 | 1 | 1 | 0 |
## 4. Coverage by Risk
| Risk | Planned | Executed | % Executed |
|---|---|---|---|
| High | 13 | 12 | 92% |
| Medium | 4 | 4 | 100% |
## 5. Key Defects
| Bug ID | Title | Severity | Priority | Status |
|---|---|---|---|---|
| BUG-API-001 | Injection triggers 500 on POST /users | S1 | P1 | Reported upstream (server bug) |
| BUG-API-002 | Score non-reproducible under concurrency | S2 | P1 | Fixed |
| BUG-API-003 | Latency off by ~50 ms on Windows | S3 | P2 | Triaged |
## 6. Top Risks Still Open
- BUG-API-003 — Windows timing variance.
- Spec drift in staging that silently changes contracts — mitigated by rerunning baseline on every deploy.
## 7. Deviations From Plan
- Tested only stub API under CI; staging run used a single canary endpoint due to environment constraints.
## 8. Release Recommendation
**Conditional Go.**
**Rationale**: Tool correctness is solid (16/16 executed Pass). Windows timing deviation is cosmetic at tool level, documented.
**Conditions**:
- Document Windows tolerance in README.
- Hotfix BUG-API-003 within one sprint.
## 9. Known Limitations
- gRPC, GraphQL, async SSE streams unsupported.
- Only one auth mode per run (bearer OR API key).
- Production targets rejected by policy.
## 10. Sign-off
| Role | Name | Date |
|---|---|---|
| QA Owner | QA Portfolio | 2026-04-02 |
| Tech Lead | — | — |
