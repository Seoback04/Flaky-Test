"""High-level analyzer: metrics + classification + pattern detection.

Takes a list of :class:`SuiteRunResult` and produces a fully-populated
:class:`ReportSummary`.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .classifier import classify_all
from .logger import get_logger
from .metrics import aggregate_per_test
from .models import (
    AggregatedTestMetrics,
    Category,
    ClassificationResult,
    ReportSummary,
    SuiteRunResult,
    TestReport,
)
from .patterns import detect_patterns
from .utils.time_utils import utcnow

log = get_logger(__name__)


def _build_reports(
    metrics_by_id: Dict[str, AggregatedTestMetrics],
    classifications: Dict[str, ClassificationResult],
) -> List[TestReport]:
    reports: List[TestReport] = []
    for nid, metrics in metrics_by_id.items():
        classification = classifications[nid]
        pattern_notes = detect_patterns(metrics)
        if pattern_notes:
            classification = classification.model_copy(
                update={"notes": [*classification.notes, *pattern_notes]}
            )
        reports.append(TestReport(metrics=metrics, classification=classification))
    return reports


def _category_counts(reports: List[TestReport]) -> Dict[str, int]:
    counts: Dict[str, int] = {c.value: 0 for c in Category}
    for r in reports:
        counts[r.category.value] += 1
    return counts


def _sort_by_instability(reports: List[TestReport]) -> List[TestReport]:
    """Sort most-unstable-first.

    Primary key: flakiness_score desc (ties broken by transition rate desc,
    then fail rate desc). Stable categories sink to the bottom.
    """
    def _key(r: TestReport) -> tuple:
        unstable = r.category in (Category.FLAKY, Category.INFRA_SUSPECT)
        return (
            -int(unstable),
            -r.metrics.flakiness_score,
            -r.metrics.transition_rate,
            -r.metrics.fail_rate,
            r.metrics.nodeid,
        )

    return sorted(reports, key=_key)


def analyze(
    suite_runs: List[SuiteRunResult],
    pytest_target: Optional[str] = None,
    top_n: int = 10,
) -> ReportSummary:
    """Build a :class:`ReportSummary` from raw suite-run results."""
    if not suite_runs:
        log.warning("analyze() called with zero suite runs.")
        return ReportSummary(
            generated_at=utcnow(),
            pytest_target=pytest_target or "",
            total_runs=0,
            total_tests=0,
        )

    metrics_by_id = aggregate_per_test(suite_runs)
    classifications = classify_all(metrics_by_id)
    reports = _build_reports(metrics_by_id, classifications)
    sorted_reports = _sort_by_instability(reports)

    worst = [
        r for r in sorted_reports
        if r.category in (Category.FLAKY, Category.INFRA_SUSPECT, Category.STABLE_FAIL)
    ][:top_n]

    run_meta = [
        {
            "run_index": s.run_index,
            "started_at": s.started_at.isoformat(),
            "ended_at": s.ended_at.isoformat(),
            "duration": s.duration,
            "return_code": s.return_code,
            "total": s.total,
            "passed": s.passed,
            "failed": s.failed,
            "skipped": s.skipped,
        }
        for s in suite_runs
    ]

    summary = ReportSummary(
        generated_at=utcnow(),
        pytest_target=pytest_target or (suite_runs[0].pytest_target if suite_runs else ""),
        total_runs=len(suite_runs),
        total_tests=len(metrics_by_id),
        category_counts=_category_counts(reports),
        worst_offenders=worst,
        test_reports=sorted_reports,
        run_metadata=run_meta,
        notes=[],
    )
    return summary
