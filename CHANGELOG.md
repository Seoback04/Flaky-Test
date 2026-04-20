# Changelog
All notable changes to this repository are recorded here.
The format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions apply to the Flaky Test Detector tool. The QA documentation portfolio (`qa-test-cases-portfolio/`) ships on a dedicated branch and is versioned alongside the tool via git tags.
## [Unreleased]
### Added
- `VERIFICATION.md` at the repository root — records the latest end-to-end verification pass (environment, self-tests, demo run, artifact counts, schema check).
- `CHANGELOG.md` at the repository root — this file.
## [qa-portfolio] — 2026-04-19
### Added
- `qa-test-cases-portfolio/` — a full documentation-first QA portfolio covering four projects (Flaky Test Detector, AI Resume Job Apply Bot, API Chaos Testing Tool, Visual Regression Engine).
  - `docs/` — test strategy, test design techniques, bug reporting guidelines, QA workflow.
  - `templates/` — reusable test-plan / test-case / bug-report / matrix / execution-report / exploratory / API + UI checklist templates.
  - `projects/*/` — 10-file QA artifact set per project (overview, plan, scenarios, cases.csv, bug samples, matrix.csv, execution summary, risk, test data, non-functional tests).
## [1.0.x] — Flaky Test Detector
### Added (1.0.0, 2026-04-19)
- Repeated pytest execution via `pytest-json-report`.
- Deterministic classifier (`stable_pass`, `stable_fail`, `flaky`, `infra_suspect`, `unknown`).
- Per-test metrics: flakiness score, transitions, streaks, duration mean/stddev.
- 7 failure-pattern detectors (alternating, clustered, first-run-only, last-run degradation, sporadic, duration-spike, setup/teardown).
- JSON summary, CSV tables, and HTML report.
- 5 matplotlib charts (top flaky, pass/fail trend, flakiness distribution, duration variance, heatmap).
- Typer CLI: `run`, `analyze`, `report`, `demo`.
- Demo suite (stable / flaky / infra-suspect tests) for self-contained demonstrations.
- Unit + integration test suite (33 tests).
- `docs/architecture.md` describing module layout, data flow, and strategies.
### Fixed (1.0.1, 2026-04-19)
- Integration test monkeypatched the `Settings` class via an incorrect attribute path; updated to patch the class directly.
- `TestCaseResult` pydantic model flagged as a test class by pytest collection; added `__test__ = False` to suppress the warning.
### Fixed (1.0.2, 2026-04-19)
- Replaced deprecated `datetime.utcnow()` with `datetime.now(tz=timezone.utc)` in `app/models.py` and in all test files; verified clean under `-W error::DeprecationWarning`.
- Removed unused imports (`Outcome` from `app/patterns.py`, `VisualizerError` from `app/visualizer.py`).
---
## Versioning Conventions
- **Tool versions** (`1.x.y`) follow semver for the Flaky Test Detector itself.
- **Documentation artifacts** (`qa-test-cases-portfolio/`) are dated; they rev when the underlying projects or portfolio structure materially change.
- Every production release has a matching entry in `VERIFICATION.md` as evidence that it was actually built, installed, tested, and demoed end-to-end.
