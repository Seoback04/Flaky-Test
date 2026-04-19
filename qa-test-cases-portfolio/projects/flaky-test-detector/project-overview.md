# Project Overview — Flaky Test Detector
## What It Is
A Python CLI that **repeatedly executes a pytest test suite**, captures structured per-run results, aggregates them into per-test metrics, classifies each test (stable_pass / stable_fail / flaky / infra_suspect), detects failure patterns, and emits JSON / CSV / HTML reports plus matplotlib charts.
## Why It Matters
Flaky tests erode CI trust: engineers re-run pipelines until green, real regressions get masked, and release confidence decays. This tool provides **quantitative, explainable** evidence of instability so teams can quarantine, fix, or delete bad tests instead of arguing about gut feelings.
## User Personas
- **SDET / Test Tooling Engineer** — runs the detector across CI history.
- **Release Manager** — consumes the execution summary and top-flaky list.
- **Developer** — uses pattern notes to localize the root cause of flakiness.
## Core Surfaces Under Test
1. **Runner** — subprocess-driven pytest invocation with pytest-json-report.
2. **Parser** — JSON → domain models (`TestCaseResult`, `SuiteRunResult`).
3. **Metrics** — flakiness score, transitions, streaks, duration variance.
4. **Classifier** — deterministic rules → category.
5. **Pattern Detectors** — alternating / clustered / first-run-only / last-run degradation / sporadic / duration-spike / setup-teardown.
6. **Reporter** — JSON summary, CSVs, HTML.
7. **Visualizer** — top-flaky bar, pass/fail trend, distribution, duration variance, heatmap.
8. **CLI** — `run`, `analyze`, `report`, `demo` commands with argument validation.
## Inputs / Outputs
- **Inputs**: a pytest target path, `--runs`, `--delay`, `-k`, `-m`, previously-written raw JSON reports (for `analyze`).
- **Outputs**: `outputs/raw/run_NNN.json`, `outputs/summary/{summary.json,test_metrics.csv,top_flaky.csv,raw_history.csv}`, `outputs/charts/*.png`, `outputs/report.html`.
## Key Contracts
- Skipped runs are excluded from classification math.
- Flakiness score = `min(pass_count, fail_count) / executed_runs`.
- "Infra-dominated" = `infra_hits / fail_count >= infra_dominance_threshold` (default 0.5).
- Classifier is deterministic; no randomness or ML.
## Known Constraints
- N < ~5 runs produce weak signals.
- Infra classification depends on keyword heuristics; custom signatures can be added via config.
- Runner assumes `pytest-json-report` is installed.
## Testability Notes
- All metrics are pure functions of run history → easy to test with synthetic data.
- CLI is thin; most coverage sits below it in the analyzer / metrics / classifier layers.
- The "flaky demo suite" provides a reproducible signal for integration-level testing.
