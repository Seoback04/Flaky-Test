"""Deterministic flakiness classifier.

Rules (applied in order, first match wins):

1. No executed runs → ``unknown``
2. pass_count == executed → ``stable_pass``
3. fail_count == executed AND infra-dominated → ``infra_suspect``
4. fail_count == executed → ``stable_fail``
5. Both pass and fail present AND failures are infra-dominated → ``infra_suspect``
6. Both pass and fail present → ``flaky``

"Infra-dominated" means the fraction of failures whose error message matches
one of the configured infra keywords is ``>= infra_dominance_threshold``.
"""

from __future__ import annotations

from typing import Dict, List

from config.settings import settings

from .logger import get_logger
from .models import AggregatedTestMetrics, Category, ClassificationResult

log = get_logger(__name__)


def _infra_ratio(metrics: AggregatedTestMetrics) -> float:
    if metrics.fail_count <= 0:
        return 0.0
    return metrics.infra_hits / metrics.fail_count


def classify_one(metrics: AggregatedTestMetrics) -> ClassificationResult:
    """Classify a single test based on its aggregated metrics."""
    notes: List[str] = []

    executed = metrics.executed_runs
    if executed == 0:
        return ClassificationResult(
            nodeid=metrics.nodeid,
            category=Category.UNKNOWN,
            rationale="No executed runs (all skipped/unknown).",
            infra_hits=metrics.infra_hits,
            notes=["Insufficient data for classification."],
        )

    infra_ratio = _infra_ratio(metrics)
    infra_dominated = (
        metrics.fail_count > 0 and infra_ratio >= settings.infra_dominance_threshold
    )

    if metrics.pass_count == executed:
        return ClassificationResult(
            nodeid=metrics.nodeid,
            category=Category.STABLE_PASS,
            rationale=f"Passed in all {executed} executed runs.",
            infra_hits=metrics.infra_hits,
            notes=notes,
        )

    if metrics.fail_count == executed:
        if infra_dominated:
            notes.append(
                f"All {executed} failures match infra keywords "
                f"(ratio={infra_ratio:.2f})."
            )
            return ClassificationResult(
                nodeid=metrics.nodeid,
                category=Category.INFRA_SUSPECT,
                rationale="All runs failed and failures look infra-related.",
                infra_hits=metrics.infra_hits,
                notes=notes,
            )
        return ClassificationResult(
            nodeid=metrics.nodeid,
            category=Category.STABLE_FAIL,
            rationale=f"Failed in all {executed} executed runs.",
            infra_hits=metrics.infra_hits,
            notes=notes,
        )

    # Mixed outcomes
    if infra_dominated:
        notes.append(
            f"{metrics.infra_hits}/{metrics.fail_count} failures match infra keywords "
            f"(ratio={infra_ratio:.2f})."
        )
        return ClassificationResult(
            nodeid=metrics.nodeid,
            category=Category.INFRA_SUSPECT,
            rationale="Mixed outcomes dominated by infra-like failure signatures.",
            infra_hits=metrics.infra_hits,
            notes=notes,
        )

    return ClassificationResult(
        nodeid=metrics.nodeid,
        category=Category.FLAKY,
        rationale=(
            f"Mixed outcomes: {metrics.pass_count} pass / {metrics.fail_count} fail "
            f"over {executed} executed runs (flakiness={metrics.flakiness_score:.3f})."
        ),
        infra_hits=metrics.infra_hits,
        notes=notes,
    )


def classify_all(
    metrics_by_id: Dict[str, AggregatedTestMetrics],
) -> Dict[str, ClassificationResult]:
    """Classify every test in the aggregated metrics dictionary."""
    classifications = {nid: classify_one(m) for nid, m in metrics_by_id.items()}
    counts: Dict[str, int] = {}
    for c in classifications.values():
        counts[c.category.value] = counts.get(c.category.value, 0) + 1
    log.info("Classification counts: %s", counts)
    return classifications
