# Flaky Test Detector

A professional-grade, portfolio-ready **test analytics system** that repeatedly executes a pytest test suite, captures structured run history, classifies flaky behavior, computes instability metrics, and generates developer-friendly reports and visualizations.

> Built to demonstrate senior-level SDET / QA Automation / Test Intelligence engineering skills: pytest internals, CI reliability analysis, data-driven quality engineering, and clean Python architecture.

---

## Table of Contents
- [Why Flaky Tests Matter](#why-flaky-tests-matter)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Architecture Summary](#architecture-summary)
- [Classification Logic](#classification-logic)
- [Flakiness Scoring Method](#flakiness-scoring-method)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Example Outputs](#example-outputs)
- [Generated Charts](#generated-charts)
- [Testing](#testing)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Portfolio Positioning](#portfolio-positioning)
- [Screenshots](#screenshots)
- [Resume Bullet Points](#resume-bullet-points)

---

## Why Flaky Tests Matter
Flaky tests — tests that sometimes pass and sometimes fail without any code change — are one of the top causes of **broken trust in CI/CD pipelines**. Teams that tolerate flakiness pay for it in:
- wasted engineer time re-running pipelines,
- masked real regressions (engineers start ignoring failures),
- delayed deploys,
- lower confidence in automation.

Detecting, measuring and triaging flakiness is a core QA reliability concern.

## Problem Statement
Given a pytest suite, we want to:
1. Run the same tests repeatedly under similar conditions.
2. Record every test outcome per run.
3. Classify each test as **stable pass / stable fail / flaky / infra suspect**.
4. Compute quantitative instability metrics (fail rate, transitions, streaks, duration variance, flakiness score).
5. Produce ranked reports, CSV/JSON artifacts, and visualizations that engineers can act on.

## Features
- **Repeated execution** of any pytest target (N runs, optional delay, optional `-k` filter or markers).
- **Structured result capture** via the `pytest-json-report` plugin (robust, no fragile stdout parsing).
- **Deterministic classification**: `stable_pass`, `stable_fail`, `flaky`, `infra_suspect`.
- **Rich metrics**: pass/fail counts, fail rate, transitions, longest streaks, duration mean/stddev, flakiness score.
- **Failure-pattern detectors**: alternating outcomes, clustered failures, first-run-only failures, sporadic singles, duration-spike correlation, setup/teardown instability.
- **Reports**: JSON summary, CSV table of per-test metrics, `top_flaky.csv`, ranked offenders, optional HTML report.
- **Visualizations** (matplotlib only): flakiness-score distribution, top-N flaky bar chart, pass/fail trend across runs, tests-vs-runs heatmap, duration-variance chart.
- **Demo test suite** with stable, flaky, and infra-suspect tests so the project is fully runnable with zero external setup.
- **Self-tested**: unit tests for classifier, metrics, parser, patterns; an integration test that runs the demo end-to-end.
- **Clean architecture**: typed Pydantic models, separated runner/parser/analyzer/classifier/metrics/patterns/reporter/visualizer layers.

## Architecture Summary
```
CLI (typer)
   │
   ▼
Runner  ──►  pytest + pytest-json-report  ──►  outputs/raw/run_NNN.json
   │
   ▼
Parser  ──►  TestCaseResult / SuiteRunResult (pydantic)
   │
   ▼
Analyzer  ──►  Metrics + Classifier + PatternDetector
   │
   ▼
Reporter  ──►  JSON summary, CSVs, HTML
   │
   ▼
Visualizer  ──►  matplotlib PNGs in outputs/charts/
```
See [`docs/architecture.md`](docs/architecture.md) for a deeper breakdown.

## Classification Logic
Given `N` executed runs per test (skipped runs are ignored for classification):
- **stable_pass** — passed in all executed runs.
- **stable_fail** — failed in all executed runs, and failures do **not** look infra-related.
- **infra_suspect** — all or most failures match infra/environment signatures (timeout, connection error, browser crash, setup/teardown error, file lock, network, service unavailable, intermittent resource issue).
- **flaky** — mixture of pass and fail outcomes across runs.
- **unknown** — degenerate case (no executed runs, all skipped/xfailed only).

Rules are deterministic, explicit, and implemented in `app/classifier.py`. No ML guessing.

## Flakiness Scoring Method
Primary score:
```
flakiness_score = min(pass_count, fail_count) / total_executed_runs
```
- `0.0` = stable (all pass or all fail).
- `0.5` = maximum flakiness (half pass, half fail).

Secondary indicator:
```
transition_rate = transitions / max(total_executed_runs - 1, 1)
```
Where a **transition** is any change in outcome between consecutive runs (pass→fail or fail→pass). High transition rate signals high instability independent of fail rate.

## Tech Stack
Python 3.11+, `pytest`, `pytest-json-report`, `pandas`, `matplotlib`, `pydantic v2`, `typer`, `jinja2`, `rich`, standard library (`logging`, `pathlib`, `subprocess`, `statistics`, `collections`).

## Installation
Requires Python 3.11+.

```bash
# clone
git clone https://github.com/Seoback04/Flaky-Test.git
cd Flaky-Test

# create & activate a virtual env
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

## Usage
All commands are exposed through `main.py`:

```bash
# show help
python main.py --help

# run the bundled demo suite 20 times and analyze
python main.py run --tests demo --runs 20

# run against your own project
python main.py run --tests path/to/tests --runs 15 --delay 1.0

# keyword filter
python main.py run --tests tests/ --runs 10 -k login

# analyze previously captured raw runs
python main.py analyze --input outputs/raw

# regenerate report from the latest analysis
python main.py report --input outputs/summary

# one-shot demo: run demo suite + analyze + report + charts
python main.py demo --runs 15
```

## Example Outputs
```
outputs/
├── raw/
│   ├── run_001.json
│   ├── run_002.json
│   └── ...
├── summary/
│   ├── summary.json
│   ├── test_metrics.csv
│   ├── top_flaky.csv
│   └── raw_history.csv
├── charts/
│   ├── top_flaky.png
│   ├── pass_fail_trend.png
│   ├── flakiness_distribution.png
│   ├── duration_variance.png
│   └── heatmap.png
└── report.html
```

`summary.json` (shape):
```json
{
  "generated_at": "2025-01-01T12:34:56",
  "total_runs": 20,
  "total_tests": 12,
  "categories": {"stable_pass": 5, "stable_fail": 1, "flaky": 4, "infra_suspect": 2},
  "top_flaky": [
    {"nodeid": "demo/test_flaky.py::test_random_50_50", "flakiness_score": 0.5, "fail_rate": 0.5}
  ]
}
```

## Generated Charts
- `top_flaky.png` — top N most unstable tests by flakiness score.
- `pass_fail_trend.png` — pass vs fail counts across runs 1..N.
- `flakiness_distribution.png` — histogram of per-test flakiness scores.
- `duration_variance.png` — average duration with stddev error bars for top tests.
- `heatmap.png` — matrix of tests × runs (green=pass, red=fail, grey=skip).

## Testing
```bash
# run the detector's own unit + integration tests
pytest tests/
```
The suite contains:
- `test_models.py` — pydantic schema sanity.
- `test_classifier.py` — deterministic classification rules.
- `test_metrics.py` — flakiness score and transition math.
- `test_patterns.py` — failure-pattern detectors.
- `test_parser.py` — JSON-report parsing.
- `test_demo_integration.py` — end-to-end run of the demo suite → reports produced.

## Limitations
- Flakiness inherently requires multiple executions; very small `--runs` values produce weak signals.
- Infra classification is heuristic (keyword-based); it can be extended with custom signatures.
- HTML report is intentionally lightweight and dependency-minimal (jinja2).
- Parallel test execution (`pytest-xdist`) is not explicitly orchestrated (but can be passed via pytest args).

## Future Improvements
- Persist history across sessions into SQLite for longitudinal trend tracking.
- Integrate with GitHub Actions / Jenkins to ingest CI runs directly.
- Add a lightweight FastAPI dashboard.
- Optional LLM-based failure-message clustering (on top of deterministic rules).
- Quarantine-suggestion workflow + auto-PR generation.

## Portfolio Positioning
This project is designed to showcase:
- **Test intelligence & reliability engineering**, not just scripting.
- **Clean Python architecture** with clear module boundaries.
- **Deterministic analytics**: explainable metrics over black-box ML.
- **Real-world QA pain-point solving** (flakiness triage is a known CI bottleneck).

Good fit for roles: SDET, QA Automation Engineer, Test Tooling Engineer, CI/DevEx Engineer, Release Reliability Engineer.

## Screenshots
> Replace these placeholders with actual screenshots after running the demo once.

- `docs/screenshots/top_flaky.png` — *top flaky tests bar chart*
- `docs/screenshots/trend.png` — *pass/fail trend across runs*
- `docs/screenshots/report_html.png` — *HTML summary report*

## Resume Bullet Points
- Built a Python-based flaky test detection system that executed pytest suites across repeated runs, classified instability patterns, and ranked unreliable tests using transition-aware flakiness metrics.
- Engineered a modular test analytics pipeline with structured result ingestion, deterministic failure classification, CSV/JSON reporting, and matplotlib visualizations to improve CI trustworthiness.
- Designed and validated a QA reliability tool that distinguished stable, flaky, and infrastructure-suspect failures through repeat execution analysis, pattern detection, and automated report generation.

---
© Flaky Test Detector — portfolio project.
