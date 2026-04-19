# API Test Checklist — <Endpoint / Service>
Use this as a per-endpoint sanity pass. Tick each item or mark N/A with reason.
## 1. Contract
- [ ] Method matches spec (GET/POST/PUT/PATCH/DELETE).
- [ ] URL path matches spec (including versioning).
- [ ] Required headers documented and enforced.
- [ ] Response schema matches spec (happy path).
- [ ] Response schema matches spec (each error path).
- [ ] Content-Type is correct and consistent.
## 2. Authentication / Authorization
- [ ] Unauthenticated request → 401.
- [ ] Authenticated but unauthorized → 403.
- [ ] Expired / malformed token → 401 with clear error.
- [ ] Tokens are not leaked in logs or error bodies.
## 3. Input Validation
- [ ] Missing required fields → 400 with field-level message.
- [ ] Extra unknown fields → documented behavior (ignored or 400).
- [ ] Wrong field types → 400.
- [ ] Out-of-range numeric values → 400.
- [ ] Too-long strings / oversized payloads → 413.
- [ ] Unicode, emoji, RTL text accepted or rejected per spec.
- [ ] SQL / NoSQL / template injection attempts safely rejected.
## 4. Idempotency & Side Effects
- [ ] Idempotent methods (GET/PUT/DELETE) are truly idempotent.
- [ ] POST retries do not duplicate side effects when idempotency key is supplied.
## 5. Status Codes
- [ ] 2xx used only on success.
- [ ] 4xx used only for client errors; never 500 for bad input.
- [ ] 5xx responses return a stable error envelope, no stack traces.
## 6. Rate Limiting / Throttling
- [ ] Limits documented.
- [ ] Exceeding limit returns 429 with `Retry-After`.
- [ ] No user can DoS another tenant.
## 7. Performance
- [ ] p50, p95, p99 latencies recorded on happy path.
- [ ] Slow upstream simulated; endpoint times out gracefully.
- [ ] Large-response pagination tested.
## 8. Observability
- [ ] Correlation ID / request ID present in response and logs.
- [ ] Error responses log enough detail for post-mortem.
- [ ] Metrics emitted for success, failure, and latency buckets.
## 9. Security
- [ ] TLS-only.
- [ ] CORS policy matches spec.
- [ ] No sensitive data in URL query parameters.
- [ ] PII is redacted in logs.
## 10. Backward Compatibility
- [ ] New fields are additive; existing clients not broken.
- [ ] Deprecated fields return with a deprecation header.
