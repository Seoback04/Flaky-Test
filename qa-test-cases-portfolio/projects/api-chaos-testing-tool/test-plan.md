# Test Plan — API Chaos Testing Tool
_Version_: 1.0 &nbsp;|&nbsp; _Owner_: QA Portfolio
## 1. Introduction
Validate the fuzzer + chaos harness end-to-end: spec parsing, payload generation, fault injection, result logging, and stability scoring. Primary correctness concern is that the tool itself does not corrupt the data it reports; a tool that lies about stability is worse than no tool.
## 2. Objectives
- Generate valid payloads that always satisfy the OpenAPI schema.
- Generate invalid payloads that are provably invalid against the schema.
- Inject network faults accurately (latency/timeout/connection drop) with verifiable timing.
- Record every request/response deterministically with timing and outcome.
- Compute a reproducible stability score from the logged results.
## 3. Scope
**In scope**
- OpenAPI 3.x spec parsing (YAML + JSON).
- Payload generation (valid, null, type-swap, oversized, deeply nested, injection strings).
- Fault injection (latency, connect timeout, read timeout, connection reset, 5xx sim).
- Execution: concurrency and rate limiting.
- Stability scoring and reporting.
- CLI argument validation.
**Out of scope**
- Production targets (safety policy).
- gRPC / GraphQL.
- Property-based invariants beyond schema validity.
## 4. Test Approach
| Dimension | Approach |
|---|---|
| Functional | Each payload strategy covered; each fault type covered. |
| Negative | Broken specs, missing auth, oversized responses. |
| Boundary | min/max field lengths, numeric overflow, nested depth. |
| Non-functional | Performance (throughput), observability (structured logs). |
## 5. Test Design Techniques
- EP + BVA on field types, string lengths, numeric ranges.
- Decision tables on rate-limit response behavior.
- Error guessing on content-type mismatches, chunked encoding.
- State transition: request → retry → terminal state.
## 6. Deliverables
Same 10-file contract.
## 7. Environments
- **Dev**: local docker-compose stub API (configurable to respond with specified delays / error codes).
- **CI**: fixture stub API with pre-recorded behaviors.
- **Staging**: real service under low-rate chaos.
## 8. Entry / Exit Criteria
Entry: target reachable; spec parses; auth works.
Exit: all High-risk cases Pass; stability score reproducible across two runs with the same seed.
## 9. Risks
See `risk-analysis.md`.
