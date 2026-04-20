# Non-Functional Tests — API Chaos Testing Tool
## Performance
- **Throughput**: sustain 500 req/s against stub for 60 s on a modern laptop with no memory growth > 100 MB.
- **Startup**: spec parse + warm-up < 2 s.
- **Score computation**: < 1 s for 100 000 NDJSON rows.
## Reliability
- 60-minute soak against stub at 100 req/s → zero file descriptor leaks.
- Recover from intermittent TCP resets without missing requests.
- Idempotent rerun: same seed + same stub + same duration → identical score.
## Robustness
- Chunked responses, gzip mismatch, truncated bodies.
- Server closing connection mid-response → client classifies as `connection_reset`.
- HTTP 1.1 keep-alive behavior with and without `Connection: close`.
## Usability
- `--dry-run` prints planned requests without sending.
- `--only METHOD:PATH` filter for focused runs.
- Error messages include the endpoint + payload shape that failed.
## Observability
- One NDJSON line per request; correlation `request_id`.
- Per-endpoint summary printed at the end with status code histogram.
- Optional Prometheus textfile exporter.
## Security / Safety
- Production URL pattern detection requires `--i-know-this-is-prod`.
- Injection corpus is opt-in via `--injection-corpus default`; off by default on shared environments.
- Auth tokens masked in logs.
## Maintainability
- Fault injector is a single module with a pluggable strategy interface.
- Stability scoring is expressed as a single pure function with a golden-dataset test.
## Not Covered (Explicit)
- GraphQL / gRPC / SSE / WebSockets.
- Distributed (multi-machine) load generation.
- Full pen testing.
