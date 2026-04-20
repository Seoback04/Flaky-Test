# Non-Functional Tests — AI Resume Job Apply Bot
## Performance
- **End-to-end flow** from resume to safe-submit preview < 30 s on a modern laptop with 100 Mbps network (LLM included).
- **Field detection** on a 200-element form < 2 s.
- **Autofill** of a 40-field form < 5 s.
- Measured via `time.perf_counter` wrappers in staging smoke suite.
## Reliability
- Re-run the same apply flow 20 times against a fixture page → 0 intermittent failures.
- Kill the browser process mid-autofill → bot logs the error, exits cleanly, no orphaned processes.
- Network interruption during LLM call → exponential backoff up to 3 attempts; then actionable error.
## Robustness
- Markup variance: fields with missing `id` but present `name`; fields with `aria-label` only; fields inside iframes.
- Input variance: unicode, emoji, very long strings.
- File path variance: spaces, unicode, UNC paths (Windows).
## Usability
- Every blocked submission explains why in plain English.
- `--help` shows all flags with examples.
- Dry-run produces a human-readable preview (not just JSON).
## Observability
- Structured JSON logs with `request_id`, `job_id`, `step`, `field`, `confidence`.
- Every submission produces pre/post screenshots plus a `mapping.json` + `submission.json`.
- Failure modes each have a unique exit code (0 success, 2 validation, 3 safe-submit-blocked, 4 CAPTCHA, 5 LLM failure).
## Security / Privacy
- PII masking filter applied on the root logger, at every level (BUG-JOBBOT-002 regression).
- Credentials / tokens never echoed.
- HTTP layer uses TLS; certificate verification enforced.
- Local storage of resume contents disabled by default.
## Maintainability
- Browser layer behind an adapter interface; swapping Selenium ↔ Playwright is a 1-file change.
- Profile schema is versioned; migration helper for old profiles.
## Not Covered (Explicit)
- Bypassing CAPTCHA / anti-bot systems.
- Full pen testing.
- Load testing at thousands-of-concurrent-applications scale.
