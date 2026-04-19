"""Unit tests for pydantic models."""

from __future__ import annotations

from datetime import datetime, timezone

from app.models import (
    AggregatedTestMetrics,
    Category,
    Outcome,
    SuiteRunResult,
    TestCaseResult,
)


def test_outcome_flags() -> None:
    assert Outcome.PASSED.is_pass
    assert Outcome.XPASSED.is_pass
    assert Outcome.FAILED.is_fail
    assert Outcome.ERROR.is_fail
    assert Outcome.SKIPPED.is_executed is False
    assert Outcome.PASSED.is_executed is True


def test_testcase_result_defaults() -> None:
    tc = TestCaseResult(nodeid="demo/test_x.py::test_a", outcome=Outcome.PASSED)
    assert tc.duration == 0.0
    assert tc.run_index == 0
    assert isinstance(tc.timestamp, datetime)
    assert tc.error_message is None


def test_suite_run_result_counts() -> None:
    now = datetime.now(tz=timezone.utc)
    tc1 = TestCaseResult(nodeid="a", outcome=Outcome.PASSED)
    tc2 = TestCaseResult(nodeid="b", outcome=Outcome.FAILED)
    tc3 = TestCaseResult(nodeid="c", outcome=Outcome.SKIPPED)
    suite = SuiteRunResult(
        run_index=1,
        started_at=now,
        ended_at=now,
        duration=1.0,
        return_code=1,
        pytest_target="demo",
        test_results=[tc1, tc2, tc3],
    )
    assert suite.total == 3
    assert suite.passed == 1
    assert suite.failed == 1
    assert suite.skipped == 1


def test_aggregated_metrics_roundtrip() -> None:
    m = AggregatedTestMetrics(
        nodeid="x",
        total_runs=5,
        executed_runs=5,
        pass_count=3,
        fail_count=2,
        skip_count=0,
    )
    dumped = m.model_dump()
    restored = AggregatedTestMetrics.model_validate(dumped)
    assert restored.nodeid == "x"
    assert restored.pass_count == 3


def test_category_enum_values() -> None:
    assert Category.STABLE_PASS.value == "stable_pass"
    assert Category.FLAKY.value == "flaky"
    assert Category.INFRA_SUSPECT.value == "infra_suspect"
