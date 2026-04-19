"""Unit tests for the deterministic classifier."""

from __future__ import annotations

from app.classifier import classify_one
from app.models import AggregatedTestMetrics, Category, Outcome


def _m(**overrides) -> AggregatedTestMetrics:
    base = dict(
        nodeid="t",
        total_runs=10,
        executed_runs=10,
        pass_count=10,
        fail_count=0,
        skip_count=0,
        outcomes_sequence=[Outcome.PASSED] * 10,
    )
    base.update(overrides)
    return AggregatedTestMetrics(**base)


def test_stable_pass() -> None:
    m = _m()
    assert classify_one(m).category == Category.STABLE_PASS


def test_stable_fail_non_infra() -> None:
    m = _m(
        pass_count=0,
        fail_count=10,
        outcomes_sequence=[Outcome.FAILED] * 10,
        error_messages=["AssertionError: 2+2 != 5"] * 10,
        infra_hits=0,
    )
    assert classify_one(m).category == Category.STABLE_FAIL


def test_stable_fail_all_infra_becomes_infra_suspect() -> None:
    m = _m(
        pass_count=0,
        fail_count=10,
        outcomes_sequence=[Outcome.FAILED] * 10,
        error_messages=["Request timed out"] * 10,
        infra_hits=10,
    )
    assert classify_one(m).category == Category.INFRA_SUSPECT


def test_flaky_mixed() -> None:
    m = _m(
        pass_count=6,
        fail_count=4,
        outcomes_sequence=[Outcome.PASSED, Outcome.FAILED] * 5,
        error_messages=["AssertionError"] * 4,
        infra_hits=0,
    )
    assert classify_one(m).category == Category.FLAKY


def test_flaky_dominated_by_infra_is_infra_suspect() -> None:
    m = _m(
        pass_count=6,
        fail_count=4,
        outcomes_sequence=[Outcome.PASSED] * 6 + [Outcome.FAILED] * 4,
        error_messages=["timeout waiting for service"] * 4,
        infra_hits=4,
    )
    assert classify_one(m).category == Category.INFRA_SUSPECT


def test_unknown_when_no_executed_runs() -> None:
    m = _m(
        executed_runs=0,
        pass_count=0,
        fail_count=0,
        skip_count=10,
        outcomes_sequence=[Outcome.SKIPPED] * 10,
    )
    assert classify_one(m).category == Category.UNKNOWN


def test_rationale_contains_counts_for_flaky() -> None:
    m = _m(
        pass_count=5,
        fail_count=5,
        outcomes_sequence=[Outcome.PASSED] * 5 + [Outcome.FAILED] * 5,
        infra_hits=0,
    )
    result = classify_one(m)
    assert result.category == Category.FLAKY
    assert "5 pass" in result.rationale and "5 fail" in result.rationale
