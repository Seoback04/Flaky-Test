"""Per-test aggregated metrics: flakiness score, transitions, streaks, durations."""

from __future__ import annotations

import statistics
from collections import defaultdict
from typing import Dict, Iterable, List

from config.settings import settings

from .logger import get_logger
from .models import AggregatedTestMetrics, Outcome, SuiteRunResult, TestCaseResult
from .utils.text_utils import contains_any_keyword

log = get_logger(__name__)


def _sorted_by_run(records: Iterable[TestCaseResult]) -> List[TestCaseResult]:
    return sorted(records, key=lambda r: r.run_index)


def _count_transitions(outcomes: List[Outcome]) -> int:
    """Count pass<->fail state changes (skipped outcomes are ignored)."""
    filtered = [o for o in outcomes if o.is_executed]
    transitions = 0
    for a, b in zip(filtered, filtered[1:]):
        if a.is_pass != b.is_pass:
            transitions += 1
    return transitions


def _streaks(outcomes: List[Outcome]) -> tuple[int, int]:
    """Return (longest_pass_streak, longest_fail_streak) across executed runs."""
    longest_pass = current_pass = 0
    longest_fail = current_fail = 0
    for o in outcomes:
        if not o.is_executed:
            current_pass = 0
            current_fail = 0
            continue
        if o.is_pass:
            current_pass += 1
            current_fail = 0
            longest_pass = max(longest_pass, current_pass)
        elif o.is_fail:
            current_fail += 1
            current_pass = 0
            longest_fail = max(longest_fail, current_fail)
    return longest_pass, longest_fail


def compute_flakiness_score(pass_count: int, fail_count: int, executed: int) -> float:
    """``min(pass, fail) / executed`` (bounded to [0, 0.5])."""
    if executed <= 0:
        return 0.0
    return round(min(pass_count, fail_count) / executed, 6)


def _stddev(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    try:
        return round(statistics.pstdev(values), 6)
    except statistics.StatisticsError:
        return 0.0


def _infra_hits(records: List[TestCaseResult]) -> int:
    return sum(
        1
        for r in records
        if r.outcome.is_fail
        and contains_any_keyword(r.error_message, settings.infra_keywords)
    )


def aggregate_per_test(
    suite_runs: List[SuiteRunResult],
) -> Dict[str, AggregatedTestMetrics]:
    """Aggregate run-level results into per-test metrics.

    The output is keyed by ``nodeid``. Tests that were not present in every
    run still receive a record; missing runs are treated as no-data (not pass,
    not fail) and excluded from rates.
    """
    grouped: Dict[str, List[TestCaseResult]] = defaultdict(list)
    total_runs = len(suite_runs)

    for suite in suite_runs:
        for tc in suite.test_results:
            grouped[tc.nodeid].append(tc)

    metrics: Dict[str, AggregatedTestMetrics] = {}

    for nodeid, records in grouped.items():
        records = _sorted_by_run(records)
        outcomes = [r.outcome for r in records]
        durations = [r.duration for r in records if r.outcome.is_executed]
        executed = sum(1 for o in outcomes if o.is_executed)
        passed = sum(1 for o in outcomes if o.is_pass)
        failed = sum(1 for o in outcomes if o.is_fail)
        skipped = sum(1 for o in outcomes if o == Outcome.SKIPPED)
        errors = sum(1 for o in outcomes if o == Outcome.ERROR)

        transitions = _count_transitions(outcomes)
        longest_pass, longest_fail = _streaks(outcomes)
        pass_rate = round(passed / executed, 6) if executed else 0.0
        fail_rate = round(failed / executed, 6) if executed else 0.0
        flakiness = compute_flakiness_score(passed, failed, executed)
        avg_dur = round(sum(durations) / len(durations), 6) if durations else 0.0
        dur_std = _stddev(durations)
        transition_rate = round(transitions / max(executed - 1, 1), 6) if executed > 1 else 0.0

        metrics[nodeid] = AggregatedTestMetrics(
            nodeid=nodeid,
            total_runs=total_runs,
            executed_runs=executed,
            pass_count=passed,
            fail_count=failed,
            skip_count=skipped,
            error_count=errors,
            pass_rate=pass_rate,
            fail_rate=fail_rate,
            flakiness_score=flakiness,
            transition_count=transitions,
            transition_rate=transition_rate,
            longest_pass_streak=longest_pass,
            longest_fail_streak=longest_fail,
            average_duration=avg_dur,
            duration_stddev=dur_std,
            outcomes_sequence=outcomes,
            durations=durations,
            error_messages=[r.error_message for r in records if r.error_message],
            infra_hits=_infra_hits(records),
        )

    log.info("Aggregated metrics for %d tests across %d runs.", len(metrics), total_runs)
    return metrics
