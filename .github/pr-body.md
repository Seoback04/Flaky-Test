## Summary
This PR merges the fully built, verified, and documented **Flaky Test Detector** along with a **documentation-first QA portfolio** into `main`. The detector has been exercised end-to-end with a green verification pass recorded in `VERIFICATION.md`.

## What's included
### Flaky Test Detector (Python CLI)
- Typer CLI: `run`, `analyze`, `report`, `demo`.
- Repeated pytest execution via `pytest-json-report`.
- Deterministic classifier (`stable_pass` / `stable_fail` / `flaky` / `infra_suspect` / `unknown`).
- Per-test metrics: flakiness score, transitions, streaks, duration mean/stddev.
- 7 failure-pattern detectors (alternating, clustered, first-run-only, last-run degradation, sporadic, duration-spike, setup/teardown).
- JSON summary, CSV tables, HTML report.
- 5 matplotlib charts (`top_flaky`, `pass_fail_trend`, `flakiness_distribution`, `duration_variance`, `heatmap`).
- Demo suite (stable / flaky / infra-suspect) for self-contained demonstrations.
- Unit + integration suite: **33 tests, 100% passing** with `-W error::DeprecationWarning`.
- Architecture documentation in `docs/architecture.md`.

### QA documentation portfolio (`qa-test-cases-portfolio/`)
- `docs/` — test strategy, test design techniques, bug reporting guidelines, QA workflow.
- `templates/` — reusable test-plan / test-case / bug-report / matrix / execution-report / exploratory / API + UI checklist templates (8 files).
- `projects/` — four projects, each with the same 10-file contract (overview, plan, scenarios, test-cases.csv, bug-report-samples, traceability-matrix.csv, execution summary, risk analysis, test data, non-functional tests):
  - Flaky Test Detector
  - AI Resume Job Apply Bot
  - API Chaos Testing Tool
  - Visual Regression Engine

### Documentation
- `README.md` — project overview, installation, usage, examples, limitations, resume bullets.
- `VERIFICATION.md` — evidence-driven verification log for the latest release.
- `CHANGELOG.md` — Keep-a-Changelog history covering 1.0.0 → 1.0.2 + portfolio addition.
- `docs/architecture.md` — module map, data flow, testing / failure-handling strategies.

## Verification evidence
End-to-end verification performed on this branch. Full log: [`VERIFICATION.md`](../VERIFICATION.md).

| Item | Result |
|---|---|
| Environment install | Pass (Python 3.13.13, all 10 required packages) |
| `pytest tests/ -W error::DeprecationWarning` | **33 / 33 passed, 0 warnings** |
| `python main.py demo --runs 15` | Exit 0 |
| Artifacts produced | 15 raw JSON + 5 charts + 4 summary files + HTML |
| `summary.json` schema | Validated against `ReportSummary` contract |
| Classifier output | 3 stable_pass / 1 stable_fail / 4 flaky / 4 infra_suspect (as designed) |

## Commit history on this branch
- `ce02a66` — Initial commit: Flaky Test Detector (full portfolio project).
- `78b9be6` — Fix integration test monkeypatch + silence pytest collection warning.
- `2351190` — Fix timezone-aware datetimes + remove unused imports.
- `39340c4` — Add qa-test-cases-portfolio: documentation-first QA portfolio.
- `8702653` — Docs: add `VERIFICATION.md`, `CHANGELOG.md`; link exec summary to verification log.

## How to review
1. Skim `README.md` and `docs/architecture.md` for the engineering picture.
2. Open `qa-test-cases-portfolio/README.md` for the QA documentation picture.
3. Read `VERIFICATION.md` for the evidence that the tool actually works end-to-end.
4. Spot-check any project folder under `qa-test-cases-portfolio/projects/` for the 10-file contract (plan → scenarios → cases → matrix → execution summary).

## Risks / scope notes
- No changes land outside this branch; `main` currently has no overlapping work.
- Known limitations are listed in `README.md` and `VERIFICATION.md` (weak signal below ~5 runs, infra heuristic is English-only, heatmap degrades on sparse test membership — tracked as `BUG-FLAKY-003` in the QA portfolio).
- Follow-up work: fault-injection harness for `TC-FLAKY-020`, perceptual-similarity extension for the Visual Regression project (scoped but not in this PR).

## Checklist
- [x] All self-tests pass with strict deprecation warnings.
- [x] Demo runs cleanly end-to-end and produces all documented artifacts.
- [x] `summary.json` shape matches the Pydantic contract.
- [x] `VERIFICATION.md` committed.
- [x] `CHANGELOG.md` committed.
- [x] README, architecture doc, and QA portfolio cross-reference each other.
