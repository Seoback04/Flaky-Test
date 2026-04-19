# Test Scenarios — API Chaos Testing Tool
## TS-API-001 — Valid Request Injection
Generate and send schema-valid requests; expect 2xx response envelopes.
_Requirements_: REQ-API-001
_Test cases_: TC-API-001, TC-API-002
## TS-API-002 — Invalid Payload Fuzzing
Generate type-swapped / malformed / oversized payloads; expect 4xx responses, no 5xx.
_Requirements_: REQ-API-002
_Test cases_: TC-API-003, TC-API-004, TC-API-005
## TS-API-003 — Null and Missing Field Behavior
Omit required fields or send null; expect 400 with field-level error, not 500.
_Requirements_: REQ-API-003
_Test cases_: TC-API-006, TC-API-007
## TS-API-004 — Rate Limiting
Exceed the documented rate limit; expect 429 with `Retry-After`.
_Requirements_: REQ-API-004
_Test cases_: TC-API-008
## TS-API-005 — Timeout Handling
Inject latency that exceeds client timeout; request is aborted, logged, classified `client_timeout`.
_Requirements_: REQ-API-005
_Test cases_: TC-API-009
## TS-API-006 — Server Error Capture
Inject 500/502/503/504 upstream responses; results logged with status and classified `server_error`.
_Requirements_: REQ-API-006
_Test cases_: TC-API-010
## TS-API-007 — Response Time Measurement
Timing is measured from send to final byte received; within 10 ms of independent wall clock.
_Requirements_: REQ-API-007
_Test cases_: TC-API-011
## TS-API-008 — Result Logging
Every request produces one NDJSON line containing method, path, status, latency_ms, request_id.
_Requirements_: REQ-API-008
_Test cases_: TC-API-012
## TS-API-009 — Stability Scoring
Score formula deterministic given the logged results; stable across seeded runs.
_Requirements_: REQ-API-009
_Test cases_: TC-API-013, TC-API-014
## TS-API-010 — Malformed Schema Handling
Broken OpenAPI → clean, actionable error; no traceback to user.
_Requirements_: REQ-API-010
_Test cases_: TC-API-015
## TS-API-011 — Configuration Validation
Invalid concurrency / duration / auth config → reject with clear error.
_Requirements_: REQ-API-011
_Test cases_: TC-API-016, TC-API-017
