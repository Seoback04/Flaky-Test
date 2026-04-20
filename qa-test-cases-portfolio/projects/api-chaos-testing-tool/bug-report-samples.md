# Bug Report Samples — API Chaos Testing Tool
---
## BUG-API-001 — [Fuzzer] Injection corpus triggers 500 on `POST /users` (real server bug surfaced)
| Field | Value |
|---|---|
| **Bug ID** | BUG-API-001 |
| **Severity** | S1 |
| **Priority** | P1 |
| **Frequency** | Always for `$where` payload |
| **Status** | Reported to backend team |
| **Linked Test Case** | TC-API-005 |
| **Linked Requirement** | REQ-API-002 |
### Preconditions
- Staging API up; auth valid.
### Steps to Reproduce
1. `python -m chaos fuzz --spec staging.yaml --only POST:/users --injection-corpus default`.
2. Inspect the NDJSON log for status 500 rows.
### Expected Result
All injection payloads result in `4xx` responses (400 for bad input).
### Actual Result
`$where` payload produces `500 Internal Server Error` with traceback leakage visible in the response body: `MongoWriteError: $where not allowed ...`.
### Impact
Hostile client can trivially trigger 500s; traceback leaks internal DB type and error shape — reconnaissance risk.
### Root Cause Hypothesis
Server-side validator does not reject `$`-prefixed keys before passing input into MongoDB update expression.
### Notes
- This is a **tool-correctness pass** — the fuzzer itself worked as expected. Reporting upstream to backend team.
- Added `$where` payload to the regression corpus.
---
## BUG-API-002 — [Scoring] Stability score non-reproducible when request IDs collide
| Field | Value |
|---|---|
| **Bug ID** | BUG-API-002 |
| **Severity** | S2 |
| **Priority** | P1 |
| **Frequency** | Always when concurrency ≥ 8 |
| **Status** | Fixed |
| **Linked Test Case** | TC-API-013 |
| **Linked Requirement** | REQ-API-009 |
### Preconditions
- Run fuzz with `--concurrency 16 --seed 42 --duration 10s` twice.
### Expected Result
Two runs produce identical `stability.csv`.
### Actual Result
Scores differ by ~0.01 across runs; diff tracks back to duplicate `request_id` entries in `results.ndjson`.
### Impact
The tool's core claim (reproducible scoring) is violated — blocks use as a release gate.
### Root Cause Hypothesis
`request_id` is generated from `uuid4` per worker thread, not seeded; under concurrency the collision rate is low but not zero, and the dedup step drops one of the rows.
### Notes
- Fix: derive `request_id` deterministically from `(seed, worker_id, index)`.
- Regression test: TC-API-013.
---
## BUG-API-003 — [Chaos] Latency injection off by ~50 ms under Windows asyncio
| Field | Value |
|---|---|
| **Bug ID** | BUG-API-003 |
| **Severity** | S3 |
| **Priority** | P2 |
| **Frequency** | Always on Windows |
| **Status** | Triaged |
| **Linked Test Case** | TC-API-009 |
| **Linked Requirement** | REQ-API-005 |
### Preconditions
- Run on Windows 11.
- `--latency 100ms --requests 100`.
### Expected Result
Observed latency per request ≈ 100 ± 10 ms.
### Actual Result
Observed latency ≈ 150 ± 10 ms on Windows (fine on Linux / macOS).
### Impact
Timing measurements are off on Windows only — stability score on Windows does not match Linux by ~5%.
### Root Cause Hypothesis
Windows default asyncio event loop (`ProactorEventLoop`) has coarser timer resolution than Linux epoll; needs explicit `asyncio.sleep` calibration.
### Notes
- Workaround: document a ±50 ms tolerance on Windows in the README.
- Fix candidate: use `time.perf_counter` + busy-wait calibration for sub-100 ms delays.
