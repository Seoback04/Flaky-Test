# Risk Analysis — AI Resume Job Apply Bot
## Functional Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-F1 | Mapping engine sends wrong data to wrong field | M | H | **High** | Confidence threshold + exact-match preference + per-type stop-lists. |
| R-F2 | LLM fabricates fields (hallucinates email, phone) | M | H | **High** | Schema validation; null propagation; retry once on schema failure. |
| R-F3 | Resume parser silently drops sections | L | M | **Low** | Section-count smoke tests on golden fixtures. |
| R-F4 | Required field missing not detected | L | H | **Medium** | Form-level `required` attribute honored in safe-submit gate. |
## Integration Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-I1 | LLM provider outage / rate limit | M | M | **Medium** | Exponential backoff + user-visible error; offline mode fallback. |
| R-I2 | Browser automation library version drift | M | M | **Medium** | Pinned major version; headless smoke on upgrade. |
| R-I3 | Target site markup changes break detectors | H | M | **High** | Fixture-based regression; public-demo canary. |
## Data Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-D1 | PII leakage in logs / screenshots | M | H | **High** | Masking filter on all log levels; redacted screenshot mode. |
| R-D2 | Resume data persisted beyond session | L | H | **Medium** | No disk persistence by default; opt-in cache. |
| R-D3 | Uploaded file path injection | L | H | **Medium** | Path validation; pin allowed directories. |
## Usability Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-U1 | User unaware that submit was blocked | M | M | **Medium** | Structured reason returned + clear CLI output. |
| R-U2 | CAPTCHA abort appears as crash | L | M | **Low** | Specific log message; exit code 4 reserved for manual intervention. |
## Reliability Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-R1 | Partial autofill leaves form in dirty state | M | M | **Medium** | Rollback on error; screenshot before submit. |
| R-R2 | Network jitter mid-submit double-fires POST | L | H | **Medium** | Submission is idempotent per job ID; guard flag set pre-submit. |
## Security / Safety Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-S1 | `--dry-run` bypass (see BUG-JOBBOT-003) | L | H | **High** | Fix config-merge logic; add E2E regression. |
| R-S2 | Credential leakage in logs | L | H | **Medium** | Same masking filter; explicit deny-list for keys containing `token` / `password`. |
## Automation Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-A1 | Tests coupled to real LLM flakiness | H | M | **High** | LLM mocked in unit/integration; real LLM only in staging smoke. |
| R-A2 | Playwright browser downloads fail in CI | M | M | **Medium** | Cached browser binaries in CI image. |
## Priority Ranking
1. R-S1 — dry-run bypass (ship-blocker).
2. R-F1 / R-F2 — mapping + schema correctness.
3. R-D1 — PII leakage.
4. R-I3 — site markup drift.
5. R-A1 — LLM-coupled tests.
