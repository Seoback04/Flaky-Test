"""Pydantic data models for the Flaky Test Detector.

These models form the stable contract between the runner, parser, analyzer,
reporter and visualizer layers. All I/O (JSON on disk) is serialized through
these classes to keep the system self-describing.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


def _utcnow() -> datetime:
    """Timezone-aware UTC now (replaces deprecated ``datetime.utcnow()``)."""
    return datetime.now(tz=timezone.utc)


class Outcome(str, Enum):
    """Normalized test outcome enum."""

    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    XFAILED = "xfailed"
    XPASSED = "xpassed"
    UNKNOWN = "unknown"

    @property
    def is_pass(self) -> bool:
        return self in (Outcome.PASSED, Outcome.XPASSED)

    @property
    def is_fail(self) -> bool:
        return self in (Outcome.FAILED, Outcome.ERROR)

    @property
    def is_executed(self) -> bool:
        """Counts as an executed run for classification purposes."""
        return self in (
            Outcome.PASSED,
            Outcome.FAILED,
            Outcome.ERROR,
            Outcome.XPASSED,
        )


class Category(str, Enum):
    """Flakiness classification category."""

    STABLE_PASS = "stable_pass"
    STABLE_FAIL = "stable_fail"
    FLAKY = "flaky"
    INFRA_SUSPECT = "infra_suspect"
    UNKNOWN = "unknown"


class TestCaseResult(BaseModel):
    """Result of a single test case within one pytest run."""

    # Tell pytest not to try to collect this pydantic model as a test class.
    __test__ = False

    model_config = ConfigDict(use_enum_values=False)

    nodeid: str
    outcome: Outcome
    duration: float = 0.0
    run_index: int = 0
    timestamp: datetime = Field(default_factory=_utcnow)
    error_message: Optional[str] = None
    failure_signature: Optional[str] = None  # short, deduplicated error summary


class SuiteRunResult(BaseModel):
    """Aggregated result of a full pytest suite run (one pass of N)."""

    run_index: int
    started_at: datetime
    ended_at: datetime
    duration: float
    return_code: int
    pytest_target: str
    keyword_filter: Optional[str] = None
    marker_filter: Optional[str] = None
    test_results: List[TestCaseResult] = Field(default_factory=list)
    report_path: Optional[str] = None  # path to raw JSON report

    @property
    def total(self) -> int:
        return len(self.test_results)

    @property
    def passed(self) -> int:
        return sum(1 for t in self.test_results if t.outcome.is_pass)

    @property
    def failed(self) -> int:
        return sum(1 for t in self.test_results if t.outcome.is_fail)

    @property
    def skipped(self) -> int:
        return sum(1 for t in self.test_results if t.outcome == Outcome.SKIPPED)


class AggregatedTestMetrics(BaseModel):
    """Per-test metrics aggregated across all runs."""

    nodeid: str
    total_runs: int
    executed_runs: int
    pass_count: int
    fail_count: int
    skip_count: int
    error_count: int = 0
    pass_rate: float = 0.0
    fail_rate: float = 0.0
    flakiness_score: float = 0.0
    transition_count: int = 0
    transition_rate: float = 0.0
    longest_pass_streak: int = 0
    longest_fail_streak: int = 0
    average_duration: float = 0.0
    duration_stddev: float = 0.0
    outcomes_sequence: List[Outcome] = Field(default_factory=list)
    durations: List[float] = Field(default_factory=list)
    error_messages: List[str] = Field(default_factory=list)
    infra_hits: int = 0


class ClassificationResult(BaseModel):
    """Result of applying classification rules to a single test."""

    nodeid: str
    category: Category
    rationale: str
    infra_hits: int = 0
    notes: List[str] = Field(default_factory=list)


class TestReport(BaseModel):
    """Combined per-test view used by reporters and visualizers."""

    metrics: AggregatedTestMetrics
    classification: ClassificationResult

    @property
    def nodeid(self) -> str:
        return self.metrics.nodeid

    @property
    def category(self) -> Category:
        return self.classification.category

    @property
    def flakiness_score(self) -> float:
        return self.metrics.flakiness_score


class ReportSummary(BaseModel):
    """Top-level suite summary artifact (``summary.json``)."""

    generated_at: datetime = Field(default_factory=_utcnow)
    pytest_target: str
    total_runs: int
    total_tests: int
    category_counts: dict[str, int] = Field(default_factory=dict)
    worst_offenders: List[TestReport] = Field(default_factory=list)
    test_reports: List[TestReport] = Field(default_factory=list)
    run_metadata: List[dict] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
