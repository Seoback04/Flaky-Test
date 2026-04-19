"""matplotlib chart generation for the Flaky Test Detector.

All charts are saved as PNGs to :attr:`config.settings.Settings.charts_dir`.
The module uses a non-interactive backend so it works headless (CI-friendly).
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import matplotlib

matplotlib.use("Agg")  # headless-safe; must come before pyplot import
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from config.settings import settings  # noqa: E402

from .exceptions import VisualizerError  # noqa: E402
from .logger import get_logger  # noqa: E402
from .models import Category, Outcome, ReportSummary, SuiteRunResult  # noqa: E402
from .utils.file_io import ensure_dir  # noqa: E402

log = get_logger(__name__)


def _short(nodeid: str, width: int = 45) -> str:
    if len(nodeid) <= width:
        return nodeid
    return "…" + nodeid[-(width - 1):]


def _savefig(fig, path: Path) -> Path:
    ensure_dir(path.parent)
    fig.tight_layout()
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    return path


# ---- individual chart functions ---------------------------------------------
def chart_top_flaky(summary: ReportSummary, *, top_n: int = 10, path: Path | None = None) -> Path:
    """Horizontal bar chart: top N flakiness scores."""
    target = path or settings.charts_dir / "top_flaky.png"
    reports = [r for r in summary.worst_offenders if r.metrics.flakiness_score > 0][:top_n]
    if not reports:
        # Fallback: use any tests that had at least some failures
        reports = [
            r for r in summary.test_reports if r.metrics.fail_count > 0
        ][:top_n]

    fig, ax = plt.subplots(figsize=(9, max(3, 0.5 * max(len(reports), 1) + 1)))
    if not reports:
        ax.text(0.5, 0.5, "No flaky tests detected.", ha="center", va="center")
        ax.set_axis_off()
    else:
        labels = [_short(r.metrics.nodeid) for r in reports][::-1]
        scores = [r.metrics.flakiness_score for r in reports][::-1]
        colors = [
            "#d9534f" if r.category == Category.INFRA_SUSPECT
            else "#f0ad4e" if r.category == Category.FLAKY
            else "#999" for r in reports
        ][::-1]
        ax.barh(labels, scores, color=colors)
        ax.set_xlim(0, 0.5)
        ax.set_xlabel("Flakiness score (0 = stable, 0.5 = max flaky)")
        ax.set_title(f"Top {len(reports)} Flaky / Unstable Tests")
    return _savefig(fig, target)


def chart_pass_fail_trend(suite_runs: List[SuiteRunResult], *, path: Path | None = None) -> Path:
    """Stacked line chart of pass/fail counts across runs."""
    target = path or settings.charts_dir / "pass_fail_trend.png"
    runs = sorted(suite_runs, key=lambda s: s.run_index)
    xs = [s.run_index for s in runs]
    ps = [s.passed for s in runs]
    fs = [s.failed for s in runs]
    sk = [s.skipped for s in runs]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(xs, ps, marker="o", label="passed", color="#2ca02c")
    ax.plot(xs, fs, marker="s", label="failed", color="#d62728")
    ax.plot(xs, sk, marker="^", label="skipped", color="#7f7f7f", alpha=0.6)
    ax.set_xlabel("Run index")
    ax.set_ylabel("Test count")
    ax.set_title("Pass / Fail Trend Across Runs")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend()
    return _savefig(fig, target)


def chart_flakiness_distribution(summary: ReportSummary, *, path: Path | None = None) -> Path:
    """Histogram of per-test flakiness scores."""
    target = path or settings.charts_dir / "flakiness_distribution.png"
    scores = [r.metrics.flakiness_score for r in summary.test_reports]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if scores:
        ax.hist(scores, bins=20, range=(0.0, 0.5), color="#f0ad4e", edgecolor="#333")
    ax.set_xlabel("Flakiness score")
    ax.set_ylabel("Number of tests")
    ax.set_title("Distribution of Flakiness Scores")
    ax.set_xlim(0, 0.5)
    ax.grid(True, linestyle="--", alpha=0.4)
    return _savefig(fig, target)


def chart_duration_variance(summary: ReportSummary, *, top_n: int = 10, path: Path | None = None) -> Path:
    """Bar chart with error bars: avg duration +/- stddev for top unstable tests."""
    target = path or settings.charts_dir / "duration_variance.png"
    reports = [r for r in summary.worst_offenders if r.metrics.average_duration > 0][:top_n]
    if not reports:
        reports = sorted(
            summary.test_reports,
            key=lambda r: -r.metrics.duration_stddev,
        )[:top_n]

    fig, ax = plt.subplots(figsize=(9, max(3, 0.5 * max(len(reports), 1) + 1)))
    if not reports:
        ax.text(0.5, 0.5, "No duration data available.", ha="center", va="center")
        ax.set_axis_off()
    else:
        labels = [_short(r.metrics.nodeid) for r in reports][::-1]
        means = [r.metrics.average_duration for r in reports][::-1]
        stds = [r.metrics.duration_stddev for r in reports][::-1]
        ax.barh(labels, means, xerr=stds, color="#5bc0de", ecolor="#333", capsize=3)
        ax.set_xlabel("Avg duration (s) ± stddev")
        ax.set_title("Duration Variance — Top Unstable Tests")
    return _savefig(fig, target)


def chart_heatmap(suite_runs: List[SuiteRunResult], summary: ReportSummary, *, path: Path | None = None) -> Path:
    """Matrix of tests (rows) × runs (cols): green=pass, red=fail, grey=skip."""
    target = path or settings.charts_dir / "heatmap.png"
    runs = sorted(suite_runs, key=lambda s: s.run_index)
    if not runs or not summary.test_reports:
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.text(0.5, 0.5, "No data for heatmap.", ha="center", va="center")
        ax.set_axis_off()
        return _savefig(fig, target)

    # Order tests by flakiness_score desc so unstable ones sit at the top
    ordered_ids = [r.metrics.nodeid for r in summary.test_reports]
    # Build lookup
    lookup: dict[tuple[str, int], Outcome] = {}
    for suite in runs:
        for tc in suite.test_results:
            lookup[(tc.nodeid, suite.run_index)] = tc.outcome

    # 0 = skip/unknown, 1 = pass, -1 = fail
    matrix = np.zeros((len(ordered_ids), len(runs)), dtype=float)
    for i, nid in enumerate(ordered_ids):
        for j, suite in enumerate(runs):
            o = lookup.get((nid, suite.run_index), Outcome.SKIPPED)
            if o.is_pass:
                matrix[i, j] = 1
            elif o.is_fail:
                matrix[i, j] = -1
            else:
                matrix[i, j] = 0

    fig, ax = plt.subplots(figsize=(min(14, 1 + 0.3 * len(runs)), min(14, 1 + 0.25 * len(ordered_ids))))
    cmap = plt.get_cmap("RdYlGn")
    ax.imshow(matrix, aspect="auto", cmap=cmap, vmin=-1, vmax=1, interpolation="nearest")
    ax.set_xticks(range(len(runs)))
    ax.set_xticklabels([s.run_index for s in runs], fontsize=8)
    ax.set_yticks(range(len(ordered_ids)))
    ax.set_yticklabels([_short(n, width=50) for n in ordered_ids], fontsize=7)
    ax.set_xlabel("Run index")
    ax.set_title("Test × Run Outcome Heatmap (green=pass, red=fail)")
    return _savefig(fig, target)


def generate_all_charts(
    summary: ReportSummary, suite_runs: List[SuiteRunResult]
) -> dict[str, Path]:
    """Generate every chart. Individual failures are logged and skipped."""
    ensure_dir(settings.charts_dir)
    results: dict[str, Path] = {}
    chart_fns = (
        ("top_flaky", lambda: chart_top_flaky(summary)),
        ("pass_fail_trend", lambda: chart_pass_fail_trend(suite_runs)),
        ("flakiness_distribution", lambda: chart_flakiness_distribution(summary)),
        ("duration_variance", lambda: chart_duration_variance(summary)),
        ("heatmap", lambda: chart_heatmap(suite_runs, summary)),
    )
    for name, fn in chart_fns:
        try:
            results[name] = fn()
        except Exception as exc:  # pragma: no cover - defensive
            log.exception("Failed to generate chart %s: %s", name, exc)
    return results
