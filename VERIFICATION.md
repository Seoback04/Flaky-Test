# Verification Log — Flaky Test Detector
This document records the most recent end-to-end verification pass of the Flaky Test Detector, including environment, self-test execution, demo-pipeline run, and artifact validation. It is intentionally terse and evidence-driven.
## 1. Verification Summary
| Item | Result |
|---|---|
| Environment install | Pass |
| Self-tests (`pytest tests/`) | 33 / 33 passed, 0 warnings (with `-W error::DeprecationWarning`) |
| Demo run (`python main.py demo --runs 15`) | Pass (exit 0) |
| Artifact count | 15 raw JSON + 5 charts + 4 summary files + HTML report |
| `summary.json` schema contract | Validated |
| Overall status | **Green** — tool is functional and internally consistent |
## 2. Environment
| Item | Value |
|---|---|
| OS | Windows |
| Shell | PowerShell 5.1.26100.8115 |
| Python | 3.13.13 |
| Virtualenv | `.venv/` |
| Repository branch | `qa-portfolio` |
### Installed packages (subset verified)
| Package | Version |
|---|---|
| pytest | 9.0.3 |
| pytest-json-report | 1.5.0 |
| pandas | 3.0.2 |
| matplotlib | 3.10.8 |
| pydantic | 2.13.2 |
| typer | 0.24.1 |
| rich | 15.0.0 |
| jinja2 | 3.1.6 |
| numpy | 2.4.4 |
| python-dotenv | 1.2.2 |
## 3. Self-Test Execution
```text
pytest tests/ -W error::DeprecationWarning
collected 33 items
tests/test_classifier.py .......             [ 21%]
tests/test_demo_integration.py .             [ 24%]
tests/test_metrics.py ......                 [ 42%]
tests/test_models.py .....                   [ 57%]
tests/test_parser.py .....                   [ 72%]
tests/test_patterns.py .........             [100%]
33 passed in 5.58s
```
### Test file inventory
| File | Coverage |
|---|---|
| `tests/test_models.py` | Pydantic models + Outcome flags (5 tests) |
| `tests/test_classifier.py` | Deterministic classification rules (7 tests) |
| `tests/test_metrics.py` | Flakiness score, transitions, streaks, aggregation (6 tests) |
| `tests/test_patterns.py` | 7 failure-pattern detectors (9 tests) |
| `tests/test_parser.py` | JSON-report parser (5 tests) |
| `tests/test_demo_integration.py` | End-to-end analyze → report → visualize (1 test) |
## 4. Demo Run
Command:
```bash
python main.py demo --runs 15
```
Result (trimmed):
```text
Total runs: 15   Total tests: 12
+-----------------------+
| Category      | Count |
|---------------+-------|
| stable_pass   |     3 |
| stable_fail   |     1 |
| flaky         |     4 |
| infra_suspect |     4 |
| unknown       |     0 |
+-----------------------+
Reports written to D:\QA Proj\Flaky Test Detector\outputs
```
### Classification observations
- **stable_pass (3)** — `test_stable_addition_passes`, `test_stable_string_passes`, `test_stable_list_passes`.
- **stable_fail (1)** — `test_stable_always_fails` (15 / 15 fails with AssertionError).
- **flaky (4)** — the four randomness-driven tests in `demo/test_flaky.py`.
- **infra_suspect (4)** — the four tests in `demo/test_infra_suspect.py` whose failure messages contain infra keywords (`timeout`, `connection error`, `503`, `webdriver`).
This matches the expected classifier behavior documented in `docs/architecture.md`.
## 5. Artifact Validation
| Artifact | Path | Count / Status |
|---|---|---|
| Raw pytest-json-report files | `outputs/raw/run_NNN.json` | 15 files |
| Per-test CSV | `outputs/summary/test_metrics.csv` | Present |
| Top-flaky CSV | `outputs/summary/top_flaky.csv` | Present |
| Raw history CSV | `outputs/summary/raw_history.csv` | Present |
| Full JSON summary | `outputs/summary/summary.json` | Present |
| HTML report | `outputs/report.html` | Present |
| Charts | `outputs/charts/*.png` | 5 PNGs (`top_flaky`, `pass_fail_trend`, `flakiness_distribution`, `duration_variance`, `heatmap`) |
| Rotating log | `outputs/flaky_detector.log` | Written |
### `summary.json` contract check
Top-level keys returned: `generated_at`, `pytest_target`, `total_runs`, `total_tests`, `category_counts`, `worst_offenders`, `test_reports`, `run_metadata`, `notes`.
Key field values on this run:
- `total_runs = 15`
- `total_tests = 12`
- `category_counts = {"stable_pass": 3, "stable_fail": 1, "flaky": 4, "infra_suspect": 4, "unknown": 0}`
- `worst_offenders` length = 9
All keys and shapes match the Pydantic `ReportSummary` contract defined in `app/models.py`.
## 6. Known Limitations (carried from README)
- `--runs < ~5` produces weak signals by design.
- Infra classification uses English keyword heuristics; custom signatures can be added in `config/settings.py`.
- Parallel test execution via `pytest-xdist` is not orchestrated by the runner (but can be passed through via pytest args).
- Heatmap rendering degrades when a test appears in only a subset of runs (tracked in the QA portfolio as `BUG-FLAKY-003`).
## 7. How to Reproduce This Verification
```powershell
# from the repo root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# self-tests (strict)
pytest tests/ -W error::DeprecationWarning
# demo run
python main.py demo --runs 15
# inspect artifacts
Get-ChildItem outputs -Recurse -File
```
## 8. Sign-off
| Role | Name | Date |
|---|---|---|
| QA Owner | Portfolio Author | 2026-04-20 |
| Tool Version | 1.0.x (commit on `qa-portfolio`) | — |
