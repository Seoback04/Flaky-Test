# Architecture
This document describes the internals of the Flaky Test Detector. It is intended for engineers who want to extend, audit, or integrate the tool.
## Goals
- **Deterministic**: classification and metrics do not depend on randomness or heuristics that can't be explained.
- **Modular**: each concern (run, parse, aggregate, classify, detect patterns, report, visualize) lives in its own module with a narrow public API.
- **Typed**: every boundary is a Pydantic model or a typed dataclass.
- **Portable**: runs on Windows/macOS/Linux with a standard Python 3.11+ install.
- **CI-friendly**: no GUI dependencies, headless matplotlib backend, JSON-first I/O.
## Module Map
| Module | Responsibility |
|---|---|
| `app/cli.py` | Typer CLI wiring. Commands `run`, `analyze`, `report`, `demo`. |
| `app/runner.py` | Invokes `pytest` N times via `subprocess`, writes `outputs/raw/run_NNN.json`. |
| `app/parser.py` | Parses `pytest-json-report` payloads into `SuiteRunResult`. |
| `app/metrics.py` | Per-test aggregation: counts, streaks, transitions, durations, flakiness score. |
| `app/classifier.py` | Deterministic rules mapping metrics → `Category`. |
| `app/patterns.py` | Pure-function failure-pattern detectors returning human-readable notes. |
| `app/analyzer.py` | Orchestrates metrics + classifier + patterns, produces a `ReportSummary`. |
| `app/reporter.py` | Emits JSON, CSV, and HTML artifacts. |
| `app/visualizer.py` | matplotlib chart generation (headless backend). |
| `app/models.py` | Pydantic/Enum domain models. |
| `app/logger.py` | Rotating-file + console logger. |
| `app/exceptions.py` | Typed exception hierarchy. |
| `app/utils/` | File I/O, time, text helpers. |
| `config/settings.py` | Env-aware configuration and paths. |
## Execution Flow
1. User runs `python main.py run --tests demo --runs 20`.
2. `app.cli.cmd_run` builds a `RunnerConfig` and instantiates `PytestRunner`.
3. `PytestRunner.run_all()` loops `runs` times:
   - Build argv: `python -m pytest <target> --json-report --json-report-file=outputs/raw/run_NNN.json -q [-k ...] [-m ...]`
   - Execute via `subprocess.run` (no shell=True).
   - Parse the resulting JSON via `parser.parse_json_report` into `SuiteRunResult`.
   - Continue even if a single run fails (log + skip).
4. `analyzer.analyze(suite_runs)`:
   - `metrics.aggregate_per_test(...)` → `Dict[nodeid, AggregatedTestMetrics]`.
   - `classifier.classify_all(...)` → `Dict[nodeid, ClassificationResult]`.
   - `patterns.detect_patterns(metrics)` attaches pattern notes to each classification.
   - Produces a single `ReportSummary`.
5. `reporter.write_all_reports(summary, suite_runs)` writes:
   - `outputs/summary/summary.json`
   - `outputs/summary/test_metrics.csv`
   - `outputs/summary/top_flaky.csv`
   - `outputs/summary/raw_history.csv`
   - `outputs/report.html`
6. `visualizer.generate_all_charts(summary, suite_runs)` writes PNGs to `outputs/charts/`.
## Data Flow
```
pytest subprocess
   │ (stdout/stderr)
   ▼
outputs/raw/run_NNN.json (pytest-json-report)
   │
   ▼
parser.parse_json_report ──► SuiteRunResult
   │
   ▼
metrics.aggregate_per_test ──► AggregatedTestMetrics
   │
   ├──► classifier.classify_one ──► ClassificationResult
   └──► patterns.detect_patterns ──► List[str] pattern notes
         │
         ▼
analyzer.analyze ──► ReportSummary
   │
   ├──► reporter.* (JSON, CSV, HTML)
   └──► visualizer.* (PNG charts)
```
## Result Ingestion Strategy
We rely on `pytest-json-report` rather than parsing stdout because:
- pytest's stdout format is not a stable contract.
- The plugin exposes per-test phases (setup / call / teardown) which lets us correctly classify setup/teardown errors as `error`, not just `failed`.
- JSON is trivial to diff, replay, and test against.
Each run's file is self-describing: even if the analyzer is lost, you can re-run `python main.py analyze --input outputs/raw` to reconstruct everything.
## Classification Strategy
Implemented in `app/classifier.py`. Rules are applied in order; first match wins:
1. `executed_runs == 0` → `unknown`
2. `pass_count == executed_runs` → `stable_pass`
3. `fail_count == executed_runs`:
   - infra-dominated → `infra_suspect`
   - otherwise → `stable_fail`
4. Mixed pass/fail:
   - infra-dominated → `infra_suspect`
   - otherwise → `flaky`
"Infra-dominated" = fraction of failures whose error message contains one of the configured infra keywords (see `config/settings.py:infra_keywords`) is `>= infra_dominance_threshold` (default 0.5).
## Pattern Analysis Strategy
Implemented in `app/patterns.py`. Each detector is a pure function `(AggregatedTestMetrics) -> (bool, str)`. Detectors are cheap and additive — a test can match many. Their notes are attached to the `ClassificationResult.notes` field.
Detectors:
- `alternating_outcome` — outcome flips most runs; transition_rate ≥ 0.7.
- `clustered_failures` — failures concentrated in one consecutive block.
- `first_run_failure_only` — only the first executed run failed.
- `last_run_degradation` — tail runs fail after a passing prefix (possible leak/regression).
- `sporadic_single_failures` — 1–2 isolated failures in otherwise passing history.
- `duration_spike_correlated_failures` — `stddev/avg >= 0.5` with at least one failure.
- `setup_teardown_instability` — any errors (ERROR outcomes) or high infra-signature density.
## Reporting Pipeline
- JSON: Pydantic `model_dump(mode="json")` so the format mirrors the models.
- CSV: pandas `DataFrame.to_csv` — easily consumed by spreadsheets or BI tools.
- HTML: one-file jinja2 template, inline CSS, no external JS — safe to email/attach.
## Visualization Pipeline
- `matplotlib.use("Agg")` at import time ensures headless safety.
- Each chart is a pure function that accepts a `ReportSummary` (and/or `List[SuiteRunResult]`) and returns a `Path`.
- Chart failures are caught and logged individually so one broken chart doesn't kill the rest.
## Testing Strategy
- **Unit tests** for deterministic layers (models, metrics, classifier, patterns, parser).
- **Integration test** synthesises `SuiteRunResult`s with a seeded RNG, exercises analyze → report → visualize, and asserts specific classification outcomes and artifact creation.
- The detector's tests are hermetic: they do NOT spawn a child pytest, so they're fast and CI-safe.
- The *demo* tests (under `demo/`) are intentionally flaky by design and should never be run as part of the detector's own test suite (`pytest.ini` restricts `testpaths = tests`).
## Failure Handling Strategy
- **Runner**: a failing individual pytest invocation does not abort the whole session. A missing JSON report for a given run is logged with stdout/stderr snippets and skipped; other runs continue.
- **Parser**: raises `ParserError` with context; the CLI's `analyze` command logs and skips broken reports rather than aborting.
- **Analyzer**: safe with zero suite runs (returns an empty `ReportSummary`).
- **Reporter/Visualizer**: empty datasets produce empty tables / placeholder charts instead of exceptions.
- **Logging**: every module gets its logger through `app.logger.get_logger(__name__)`. Logs go to stdout and to a rotating file at `outputs/flaky_detector.log`.
## Extensibility
- Add a new classification rule: extend `classifier.classify_one`.
- Add a new pattern: write a function in `patterns.py` and add it to the `_DETECTORS` tuple.
- Add a new chart: implement in `visualizer.py` and register in `generate_all_charts`.
- Add a new report format: add a writer to `reporter.py` and call it from `write_all_reports`.
