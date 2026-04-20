# Non-Functional Tests — Flaky Test Detector
## Performance
- **Scenario**: 200 runs × 200 tests (synthetic).
- **Targets**:
  - `analyze()` completes in < 5 s on a modern laptop.
  - `write_all_reports()` completes in < 2 s.
  - `generate_all_charts()` completes in < 10 s.
- **Method**: Seeded-RNG synthetic generator; measure `time.perf_counter`.
- **Pass criteria**: No target exceeds 2× its budget.
## Reliability
- **Partial-run failure**: kill one pytest subprocess mid-execution; verify analyzer still produces a valid summary on the surviving runs.
- **Disk full during chart generation**: simulated with a write-only filesystem; verify graceful logging, no crash of the whole pipeline.
- **Repeated `demo --runs 10` invocations back-to-back**: no resource leaks, log file size bounded by rotation.
## Robustness
- Corrupt JSON input (BUG-FLAKY-002 regression).
- Zero-byte JSON file.
- File with BOM / CRLF variance.
- Unicode test nodeids and error messages.
- Extremely long longrepr strings (> 10 KB).
## Usability
- CLI `--help` output is human-readable and includes example commands.
- Error messages on invalid args name the offending option and the valid range.
- Report HTML opens and is readable on a default browser without a web server.
- Chart axis labels and legends are legible at the default DPI.
## Maintainability
- All analytics code paths have unit tests; coverage ≥ 85%.
- Pydantic models make the on-disk shape self-describing.
- `config/settings.py` centralizes defaults and infra keywords.
## Observability
- Every module uses `app.logger.get_logger(__name__)`.
- Rotating log file: 2 MB × 3 backups.
- `outputs/flaky_detector.log` survives across invocations.
- Each run's JSON report is self-contained — replay-able.
## Security Considerations
- Runner executes `pytest` as a subprocess with user-provided paths. **Mitigation**: no `shell=True`; arguments passed as a list.
- No network surface; no tokens or secrets handled.
- No remote code execution vector in the CLI.
## Not Covered (Explicit)
- Multi-tenant / multi-user concurrent access.
- Cross-machine distributed runs.
- Large-scale (10 000+ tests) load testing.
- Formal penetration testing.
