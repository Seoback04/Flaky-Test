"""Unit tests for failure-pattern detectors."""

from __future__ import annotations

from app.models import AggregatedTestMetrics, Outcome
from app.patterns import (
    alternating_outcome,
    clustered_failures,
    detect_patterns,
    duration_spike_correlated_failures,
    first_run_failure_only,
    last_run_degradation,
    setup_teardown_instability,
    sporadic_single_failures,
)


def _build(outcomes: list[Outcome], **overrides) -> AggregatedTestMetrics:
    exec_count = sum(1 for o in outcomes if o.is_executed)
    passed = sum(1 for o in outcomes if o.is_pass)
    failed = sum(1 for o in outcomes if o.is_fail)
    # simple transition count
    filtered = [o for o in outcomes if o.is_executed]
    transitions = sum(1 for a, b in zip(filtered, filtered[1:]) if a.is_pass != b.is_pass)
    # simple streaks
    lp = lf = cp = cf = 0
    for o in filtered:
        if o.is_pass:
            cp += 1
            cf = 0
            lp = max(lp, cp)
        else:
            cf += 1
            cp = 0
            lf = max(lf, cf)
    base = dict(
        nodeid="t",
        total_runs=len(outcomes),
        executed_runs=exec_count,
        pass_count=passed,
        fail_count=failed,
        skip_count=sum(1 for o in outcomes if o == Outcome.SKIPPED),
        outcomes_sequence=outcomes,
        transition_count=transitions,
        longest_pass_streak=lp,
        longest_fail_streak=lf,
    )
    base.update(overrides)
    return AggregatedTestMetrics(**base)


def test_alternating_outcome_detected() -> None:
    m = _build([Outcome.PASSED, Outcome.FAILED] * 5)
    matched, note = alternating_outcome(m)
    assert matched
    assert "alternating" in note.lower()


def test_alternating_not_detected_when_stable() -> None:
    m = _build([Outcome.PASSED] * 10)
    matched, _ = alternating_outcome(m)
    assert not matched


def test_clustered_failures_detected() -> None:
    m = _build([Outcome.PASSED] * 3 + [Outcome.FAILED] * 4 + [Outcome.PASSED] * 3)
    matched, _ = clustered_failures(m)
    assert matched


def test_first_run_failure_only() -> None:
    m = _build([Outcome.FAILED] + [Outcome.PASSED] * 9)
    matched, _ = first_run_failure_only(m)
    assert matched


def test_last_run_degradation() -> None:
    m = _build([Outcome.PASSED] * 8 + [Outcome.FAILED, Outcome.FAILED])
    matched, _ = last_run_degradation(m)
    assert matched


def test_sporadic_single_failures() -> None:
    m = _build([Outcome.PASSED, Outcome.PASSED, Outcome.FAILED, Outcome.PASSED, Outcome.PASSED, Outcome.PASSED])
    matched, _ = sporadic_single_failures(m)
    assert matched


def test_duration_spike_correlated_failures() -> None:
    outs = [Outcome.PASSED] * 6 + [Outcome.FAILED] * 2
    m = _build(outs, average_duration=0.2, duration_stddev=0.2)
    matched, _ = duration_spike_correlated_failures(m)
    assert matched


def test_setup_teardown_instability_via_error() -> None:
    m = _build([Outcome.PASSED, Outcome.ERROR, Outcome.FAILED, Outcome.PASSED], error_count=1)
    matched, _ = setup_teardown_instability(m)
    assert matched


def test_detect_patterns_aggregates() -> None:
    m = _build([Outcome.PASSED, Outcome.FAILED] * 5)
    notes = detect_patterns(m)
    assert any("alternating_outcome" in n for n in notes)
