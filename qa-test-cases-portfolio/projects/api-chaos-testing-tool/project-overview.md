# Project Overview — API Chaos Testing Tool
## What It Is
A schema-aware API fuzzer and fault-injection harness. Given an OpenAPI / JSON-schema spec and a set of auth credentials, it generates valid and invalid payloads, injects network faults (latency, timeouts, connection drops), measures response time and error rates, and produces a **stability score** per endpoint.
## Why It Matters
APIs are only as reliable as the weakest client request that reaches production. Standard integration tests only cover happy paths. This tool systematically probes the inputs real clients might never send on purpose but will *accidentally* send eventually (malformed payloads, huge bodies, retries under partial network failure).
## User Personas
- **Backend engineer** — runs chaos locally before shipping.
- **SRE / Reliability engineer** — runs it in staging to validate SLOs.
- **Security-minded engineer** — uses it to catch obvious 500s from hostile input.
## Core Surfaces Under Test
1. **Spec ingestion** — OpenAPI 3.x parsing.
2. **Payload generator** — schema-driven valid and invalid payloads.
3. **Fault injector** — latency, timeouts, connection resets, 5xx upstream simulation.
4. **Request executor** — async HTTP client with configurable concurrency.
5. **Result logger** — structured per-request logs (request, response, timing).
6. **Stability scorer** — success rate × p95 latency × 5xx rate → composite score.
7. **Reporter** — per-endpoint CSV + overall Markdown summary.
8. **CLI** — `fuzz`, `chaos`, `baseline`, `report` commands.
## Inputs / Outputs
- **Inputs**: OpenAPI JSON/YAML, auth config, concurrency, duration, fault profiles.
- **Outputs**: `results.ndjson`, `stability.csv`, `chaos-report.md`.
## Key Contracts
- A **valid** payload (per schema) must never produce 5xx; 5xx on valid = real bug.
- **Invalid** payloads must produce 4xx, not 5xx.
- Fault injection must never mutate real data on the target.
## Known Constraints
- Only tested against REST APIs; gRPC not supported.
- Chaos is run against staging, not production.
- Auth is expected to be non-interactive (bearer / API key).
## Testability Notes
- The payload generator is a pure function over the schema; unit-testable with fixture specs.
- Fault injector is a layered proxy, easily toggleable.
- Stability scoring is deterministic and spreadsheet-reproducible.
