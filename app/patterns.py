"""Deterministic failure-pattern detectors.

Each detector returns a ``(matched: bool, note: str)`` tuple. A note is only
meaningful when ``matched`` is True. ``detect_patterns`` aggregates every
detector into a single list of human-readable notes for a test.
"""

from __future__ import annotations

from typing import List, Tuple

from .models import AggregatedTestMetrics, Outcome


PatternResult = Tuple[bool, str]


# ---- individual detectors ---------------------------------------------------
def alternating_outcome(metrics: AggregatedTestMetrics) -> PatternResult:
    """Pass/fail alternate almost every run."""
    exec_outcomes = [o for o in metrics.outcomes_sequence if o.is_executed]
    if len(exec_outcomes) < 4:
        return False, ""
    transitions = metrics.transition_count
    # If transitions >= 70% of the possible transitions and at least 3 occur
    possible = len(exec_outcomes) - 1
    if possible <= 0:
        return False, ""
    ratio = transitions / possible
    if transitions >= 3 and ratio >= 0.7:
        return True, f"Alternating outcomes (transition_rate={ratio:.2f})."
    return False, ""


def clustered_failures(metrics: AggregatedTestMetrics) -> PatternResult:
    """Failures are concentrated in a consecutive block."""
    exec_outcomes = [o for o in metrics.outcomes_sequence if o.is_executed]
    if metrics.fail_count < 2 or len(exec_outcomes) < 3:
        return False, ""
    if metrics.longest_fail_streak >= max(2, int(0.6 * metrics.fail_count)) and \
       metrics.longest_fail_streak >= 2 and \
       metrics.transition_count <= 2:
        return (
            True,
            f"Clustered failures (longest_fail_streak={metrics.longest_fail_streak}, "
            f"transitions={metrics.transition_count}).",
        )
    return False, ""


def first_run_failure_only(metrics: AggregatedTestMetrics) -> PatternResult:
    """Only the very first executed run failed; everything afterwards passed."""
    exec_outcomes = [o for o in metrics.outcomes_sequence if o.is_executed]
    if len(exec_outcomes) < 3:
        return False, ""
    if exec_outcomes[0].is_fail and all(o.is_pass for o in exec_outcomes[1:]):
        return True, "First-run-only failure (possible warm-up / cold-cache effect)."
    return False, ""


def last_run_degradation(metrics: AggregatedTestMetrics) -> PatternResult:
    """Trailing runs fail after a long passing prefix (possible regression / leak)."""
    exec_outcomes = [o for o in metrics.outcomes_sequence if o.is_executed]
    if len(exec_outcomes) < 4:
        return False, ""
    tail = exec_outcomes[-2:]
    head = exec_outcomes[:-2]
    if all(o.is_pass for o in head) and all(o.is_fail for o in tail):
        return True, "Last-run degradation (tail failures only; possible leak/regression)."
    return False, ""


def sporadic_single_failures(metrics: AggregatedTestMetrics) -> PatternResult:
    """A small handful of isolated failures scattered across mostly-passing runs."""
    exec_outcomes = [o for o in metrics.outcomes_sequence if o.is_executed]
    if len(exec_outcomes) < 5:
        return False, ""
    if 1 <= metrics.fail_count <= 2 and metrics.longest_fail_streak <= 1 and metrics.pass_count >= 3:
        return (
            True,
            f"Sporadic isolated failures ({metrics.fail_count} fails out of "
            f"{len(exec_outcomes)} runs).",
        )
    return False, ""


def duration_spike_correlated_failures(metrics: AggregatedTestMetrics) -> PatternResult:
    """High duration variance combined with failures → likely timing-related flakiness."""
    if metrics.fail_count == 0 or metrics.average_duration <= 0:
        return False, ""
    if metrics.duration_stddev / metrics.average_duration >= 0.5 and metrics.fail_count >= 1:
        return (
            True,
            f"Duration variance is high (stddev/avg="
            f"{metrics.duration_stddev / metrics.average_duration:.2f}); "
            "timing-related instability likely.",
        )
    return False, ""


def setup_teardown_instability(metrics: AggregatedTestMetrics) -> PatternResult:
    """Errors during setup/teardown rather than the test body."""
    if metrics.error_count >= 1 and metrics.fail_count >= 1:
        return (
            True,
            f"Setup/teardown errors detected ({metrics.error_count}); "
            "investigate fixtures and environment.",
        )
    if metrics.infra_hits >= 1 and metrics.infra_hits >= int(0.5 * max(metrics.fail_count, 1)):
        return (
            True,
            f"Infra-suspect signatures in {metrics.infra_hits}/{metrics.fail_count} "
            "failures.",
        )
    return False, ""


# ---- aggregation ------------------------------------------------------------
_DETECTORS = (
    alternating_outcome,
    clustered_failures,
    first_run_failure_only,
    last_run_degradation,
    sporadic_single_failures,
    duration_spike_correlated_failures,
    setup_teardown_instability,
)


def detect_patterns(metrics: AggregatedTestMetrics) -> List[str]:
    """Run all detectors and return notes for those that matched."""
    notes: List[str] = []
    for detector in _DETECTORS:
        matched, note = detector(metrics)
        if matched and note:
            notes.append(f"{detector.__name__}: {note}")
    return notes
