"""Unit tests for metrics aggregation."""

from __future__ import annotations

from datetime import datetime

from app.metrics import (
    _count_transitions,
    _streaks,
    aggregate_per_test,
    compute_flakiness_score,
)
from app.models import Outcome, SuiteRunResult, TestCaseResult


def _make_run(index: int, results: list[tuple[str, Outcome, float, str | None]]) -> SuiteRunResult:
    now = datetime.utcnow()
    tc = [
        TestCaseResult(
            nodeid=nid, outcome=oc, duration=dur, run_index=index, error_message=msg
        )
        for (nid, oc, dur, msg) in results
    ]
    return SuiteRunResult(
        run_index=index,
        started_at=now,
        ended_at=now,
        duration=0.5,
        return_code=0,
        pytest_target="demo",
        test_results=tc,
    )


def test_flakiness_score_bounds() -> None:
    assert compute_flakiness_score(10, 0, 10) == 0.0
    assert compute_flakiness_score(0, 10, 10) == 0.0
    assert compute_flakiness_score(5, 5, 10) == 0.5
    assert compute_flakiness_score(3, 7, 10) == 0.3
    assert compute_flakiness_score(0, 0, 0) == 0.0


def test_count_transitions() -> None:
    seq = [Outcome.PASSED, Outcome.FAILED, Outcome.PASSED, Outcome.PASSED, Outcome.FAILED]
    assert _count_transitions(seq) == 3


def test_count_transitions_skips_non_executed() -> None:
    seq = [Outcome.PASSED, Outcome.SKIPPED, Outcome.FAILED]
    assert _count_transitions(seq) == 1


def test_streaks() -> None:
    seq = [Outcome.PASSED, Outcome.PASSED, Outcome.FAILED, Outcome.FAILED, Outcome.FAILED, Outcome.PASSED]
    lp, lf = _streaks(seq)
    assert lp == 2
    assert lf == 3


def test_aggregate_per_test_basic() -> None:
    runs = [
        _make_run(1, [("a", Outcome.PASSED, 0.1, None), ("b", Outcome.FAILED, 0.2, "AssertionError")]),
        _make_run(2, [("a", Outcome.PASSED, 0.12, None), ("b", Outcome.PASSED, 0.2, None)]),
        _make_run(3, [("a", Outcome.FAILED, 0.11, "err"), ("b", Outcome.PASSED, 0.19, None)]),
    ]
    metrics = aggregate_per_test(runs)
    assert set(metrics.keys()) == {"a", "b"}
    a = metrics["a"]
    assert a.total_runs == 3
    assert a.pass_count == 2
    assert a.fail_count == 1
    assert a.executed_runs == 3
    assert a.flakiness_score == round(1 / 3, 6)
    assert a.transition_count == 1  # P,P,F -> one transition

    b = metrics["b"]
    assert b.pass_count == 2
    assert b.fail_count == 1
    assert b.transition_count == 1


def test_aggregate_per_test_infra_hits() -> None:
    runs = [
        _make_run(1, [("x", Outcome.FAILED, 0.1, "Request timed out")]),
        _make_run(2, [("x", Outcome.FAILED, 0.1, "Connection error: refused")]),
        _make_run(3, [("x", Outcome.FAILED, 0.1, "Assertion: 2+2 != 5")]),
    ]
    metrics = aggregate_per_test(runs)
    assert metrics["x"].infra_hits == 2
