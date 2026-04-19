# Risk Analysis — Flaky Test Detector
Each risk is scored on **Likelihood × Impact** → H / M / L. Test cases associated with High risks are **must-pass for release**.
## Functional Risks
| ID | Risk | Likelihood | Impact | Rating | Mitigation |
|---|---|---|---|---|---|
| R-F1 | Classifier misclassifies flaky vs infra_suspect | Medium | High | **High** | Decision-table-driven test cases; unit coverage in `tests/test_classifier.py`. |
| R-F2 | Flakiness score arithmetic error (off-by-one, divide-by-zero) | Low | High | **Medium** | BVA-driven cases including zero executed runs. |
| R-F3 | Transition count miscounts skipped runs | Medium | Medium | **Medium** | Dedicated test cases TC-FLAKY-010 / TC-FLAKY-011. |
| R-F4 | Pattern detector emits false positives/negatives | Medium | Medium | **Medium** | 7 detectors each covered by a unit test. |
## Integration Risks
| ID | Risk | Likelihood | Impact | Rating | Mitigation |
|---|---|---|---|---|---|
| R-I1 | pytest-json-report plugin missing at runtime | Medium | High | **High** | Runner detects missing report file, logs actionable error. |
| R-I2 | pytest stdout/stderr overrun blocks subprocess | Low | Medium | **Low** | Output captured via `capture_output=True`; no PIPE blocking. |
| R-I3 | Clock skew / non-UTC timestamps distort duration math | Low | Medium | **Low** | All timestamps via `datetime.now(tz=timezone.utc)`. |
## Data Risks
| ID | Risk | Likelihood | Impact | Rating | Mitigation |
|---|---|---|---|---|---|
| R-D1 | Malformed JSON from the plugin crashes the analyzer | Medium | High | **High** | Parser raises `ParserError`; CLI logs and skips. |
| R-D2 | Extremely large number of tests or runs produces oversized report | Low | Medium | **Low** | CSV + JSON outputs; test-metrics table scales linearly. |
| R-D3 | Unicode nodeids break CSV/HTML rendering | Low | Medium | **Low** | UTF-8 everywhere; verified in manual exploratory pass. |
## Usability Risks
| ID | Risk | Likelihood | Impact | Rating | Mitigation |
|---|---|---|---|---|---|
| R-U1 | CLI error messages are cryptic | Medium | Medium | **Medium** | Typer-validated args; defensive messages in runner/parser. |
| R-U2 | Report HTML is hard to read on mobile | Low | Low | **Low** | Minimal, readable inline CSS. |
## Reliability Risks
| ID | Risk | Likelihood | Impact | Rating | Mitigation |
|---|---|---|---|---|---|
| R-R1 | Single bad run aborts the whole session | Medium | High | **High** | Runner catches per-run exceptions, logs, and continues. |
| R-R2 | Concurrent runs race on the same output directory | Low | High | **Medium** | Current recommendation: one session at a time; documented. |
## Automation Risks
| ID | Risk | Likelihood | Impact | Rating | Mitigation |
|---|---|---|---|---|---|
| R-A1 | Regression tests rely on non-deterministic randomness | Medium | Medium | **Medium** | Integration test uses `random.Random(42)` for determinism. |
| R-A2 | Matplotlib non-headless crash on CI | Low | Medium | **Low** | `matplotlib.use("Agg")` set at import. |
## Priority Ranking
1. R-F1 — classifier misclassification (analytics correctness).
2. R-D1 — malformed JSON handling (robustness).
3. R-R1 — partial-run failure handling.
4. R-I1 — missing pytest-json-report plugin.
5. R-F2 / R-F3 — metric math correctness.
6. Everything else.
