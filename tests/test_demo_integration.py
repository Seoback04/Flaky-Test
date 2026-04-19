"""Integration test: run the full pipeline on synthetic data.

We avoid invoking a subprocess pytest run here (to keep this test hermetic
and fast). Instead we build :class:`SuiteRunResult` objects directly and
exercise analyze → report → visualize end-to-end.
"""

from __future__ import annotations

import random
from datetime import datetime
from pathlib import Path

import pytest

from app.analyzer import analyze
from app.models import (
    AggregatedTestMetrics,
    Category,
    Outcome,
    SuiteRunResult,
    TestCaseResult,
)
from app.reporter import write_all_reports
from app.visualizer import generate_all_charts


def _make_tc(nodeid: str, outcome: Outcome, run_index: int, err: str | None = None) -> TestCaseResult:
    return TestCaseResult(
        nodeid=nodeid,
        outcome=outcome,
        duration=0.05 + 0.01 * run_index,
        run_index=run_index,
        error_message=err,
    )


def _synth_runs(n_runs: int = 15) -> list[SuiteRunResult]:
    rng = random.Random(42)  # deterministic
    runs: list[SuiteRunResult] = []
    for i in range(1, n_runs + 1):
        results = [
            _make_tc("demo/test_stable.py::test_stable_pass", Outcome.PASSED, i),
            _make_tc(
                "demo/test_stable.py::test_stable_fail",
                Outcome.FAILED,
                i,
                err="AssertionError: 2+2 != 5",
            ),
            _make_tc(
                "demo/test_flaky.py::test_random_50_50",
                Outcome.PASSED if rng.random() < 0.5 else Outcome.FAILED,
                i,
                err="Random coin-flip failed.",
            ),
            _make_tc(
                "demo/test_infra.py::test_timeout",
                Outcome.PASSED if rng.random() > 0.4 else Outcome.FAILED,
                i,
                err="Request timed out after 30s",
            ),
        ]
        now = datetime.utcnow()
        runs.append(
            SuiteRunResult(
                run_index=i,
                started_at=now,
                ended_at=now,
                duration=0.5,
                return_code=1,
                pytest_target="demo",
                test_results=results,
            )
        )
    return runs


def test_end_to_end_pipeline(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Redirect output dirs into tmp_path
    from config import settings as settings_mod

    monkeypatch.setattr(settings_mod.settings.__class__, "output_dir", property(lambda self: tmp_path / "outputs"))
    monkeypatch.setattr(settings_mod.settings.__class__, "raw_dir", property(lambda self: tmp_path / "outputs" / "raw"))
    monkeypatch.setattr(settings_mod.settings.__class__, "summary_dir", property(lambda self: tmp_path / "outputs" / "summary"))
    monkeypatch.setattr(settings_mod.settings.__class__, "charts_dir", property(lambda self: tmp_path / "outputs" / "charts"))
    monkeypatch.setattr(settings_mod.settings.__class__, "html_report_path", property(lambda self: tmp_path / "outputs" / "report.html"))

    suite_runs = _synth_runs(n_runs=15)
    summary = analyze(suite_runs, pytest_target="demo", top_n=10)
    assert summary.total_runs == 15
    assert summary.total_tests == 4

    # category counts cover every enum key
    for c in Category:
        assert c.value in summary.category_counts

    # The stable pass must be classified correctly
    pass_id = "demo/test_stable.py::test_stable_pass"
    pass_report = next(r for r in summary.test_reports if r.metrics.nodeid == pass_id)
    assert pass_report.category == Category.STABLE_PASS

    # The stable fail (non-infra) must be stable_fail
    fail_id = "demo/test_stable.py::test_stable_fail"
    fail_report = next(r for r in summary.test_reports if r.metrics.nodeid == fail_id)
    assert fail_report.category == Category.STABLE_FAIL

    # The infra test must classify as infra_suspect
    infra_id = "demo/test_infra.py::test_timeout"
    infra_report = next(r for r in summary.test_reports if r.metrics.nodeid == infra_id)
    assert infra_report.category == Category.INFRA_SUSPECT

    # Write reports + charts to tmp
    paths = write_all_reports(summary, suite_runs=suite_runs)
    assert paths["summary_json"].exists()
    assert paths["metrics_csv"].exists()
    assert paths["top_flaky_csv"].exists()
    assert paths["html"].exists()

    charts = generate_all_charts(summary, suite_runs)
    assert "top_flaky" in charts
    assert charts["top_flaky"].exists()
    assert charts["pass_fail_trend"].exists()
    assert charts["flakiness_distribution"].exists()
    assert charts["heatmap"].exists()
