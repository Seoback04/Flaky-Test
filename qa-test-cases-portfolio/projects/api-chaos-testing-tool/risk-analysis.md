# Risk Analysis — API Chaos Testing Tool
## Functional Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-F1 | Payload generator emits invalid "valid" payloads (schema bug) | M | H | **High** | Validate generated payloads against the schema before sending. |
| R-F2 | Fault injector fails to actually inject the fault | L | H | **Medium** | Self-test harness: measure observed latency vs requested. |
| R-F3 | Stability score formula drifts (regression) | L | H | **Medium** | Golden-dataset tests locking the score to 6 decimals. |
## Integration Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-I1 | Target API changes contract mid-run | M | M | **Medium** | Baseline run vs current run diff highlights changes. |
| R-I2 | Auth token expires mid-run | M | M | **Medium** | Refresh hook; re-auth on 401. |
## Data Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-D1 | Fuzz mutates persistent data in staging | L | H | **Medium** | POST-only endpoints require `X-Test-Run` header or `--safe-mode`. |
| R-D2 | Tool accidentally run against production | L | H | **High** | `--i-know-this-is-prod` opt-in gate; default to refuse. |
## Usability Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-U1 | NDJSON logs too large to open in editors | M | M | **Medium** | Chunked output; `--max-log-size` flag. |
| R-U2 | Error messages unclear on auth failures | M | M | **Medium** | Dedicated `AuthError` with actionable remediation text. |
## Reliability Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-R1 | Event-loop stalls under high concurrency | M | M | **Medium** | Semaphore-capped concurrency; backpressure. |
| R-R2 | Timing accuracy OS-dependent | M | M | **Medium** | Document tolerance; prefer `time.perf_counter`. |
## Automation Risks
| ID | Risk | L | I | Rating | Mitigation |
|---|---|---|---|---|---|
| R-A1 | Stub API in CI diverges from real API | M | M | **Medium** | Recorded-cassettes updated monthly. |
## Priority Ranking
1. R-D2 — accidental prod run.
2. R-F1 — payload validity.
3. R-R1 — event-loop reliability.
4. R-I1 — contract drift.
5. R-F2 / R-F3.
