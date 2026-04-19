"""Report artifacts: JSON summary, CSV tables, HTML report.

All artifacts are written under :attr:`config.settings.Settings.summary_dir`
except for the HTML report which goes in the top-level output dir.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd

from config.settings import settings

from .exceptions import ReporterError
from .logger import get_logger
from .models import ReportSummary, SuiteRunResult, TestReport
from .utils.file_io import ensure_dir, write_json

log = get_logger(__name__)


_HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Flaky Test Detector - Report</title>
<style>
  body { font-family: -apple-system, Segoe UI, Roboto, sans-serif; margin: 2rem; color: #222; }
  h1 { margin-bottom: 0.2rem; }
  .meta { color: #666; margin-bottom: 1.5rem; font-size: 0.9rem; }
  .cards { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 2rem; }
  .card { background: #f5f5f7; border-radius: 8px; padding: 1rem 1.2rem; min-width: 140px; }
  .card .num { font-size: 1.6rem; font-weight: 600; }
  .card .lbl { color: #666; font-size: 0.85rem; }
  table { border-collapse: collapse; width: 100%; margin-top: 1rem; font-size: 0.9rem; }
  th, td { text-align: left; padding: 0.5rem 0.75rem; border-bottom: 1px solid #e5e5ea; }
  th { background: #fafafa; }
  .cat { font-weight: 600; font-size: 0.8rem; padding: 2px 6px; border-radius: 4px; }
  .cat.stable_pass { background: #d4edda; color: #155724; }
  .cat.stable_fail { background: #f8d7da; color: #721c24; }
  .cat.flaky      { background: #fff3cd; color: #856404; }
  .cat.infra_suspect { background: #d1ecf1; color: #0c5460; }
  .cat.unknown    { background: #e2e3e5; color: #383d41; }
  .notes { color: #444; font-size: 0.85rem; }
  code { background: #f0f0f3; padding: 1px 4px; border-radius: 3px; }
  .imgs img { max-width: 480px; margin: 0.5rem; border: 1px solid #e5e5ea; border-radius: 6px; }
</style>
</head>
<body>
  <h1>Flaky Test Detector — Report</h1>
  <div class="meta">
    Generated: {{ generated_at }} &middot;
    Target: <code>{{ pytest_target }}</code> &middot;
    Runs: <b>{{ total_runs }}</b> &middot;
    Tests: <b>{{ total_tests }}</b>
  </div>

  <div class="cards">
  {% for cat, count in category_counts.items() %}
    <div class="card">
      <div class="num">{{ count }}</div>
      <div class="lbl">{{ cat }}</div>
    </div>
  {% endfor %}
  </div>

  <h2>Top flaky / unstable tests</h2>
  <table>
    <thead>
      <tr>
        <th>Test</th><th>Category</th><th>Flakiness</th>
        <th>Pass</th><th>Fail</th><th>Trans.</th><th>Avg dur (s)</th><th>Notes</th>
      </tr>
    </thead>
    <tbody>
    {% for r in worst_offenders %}
      <tr>
        <td><code>{{ r.metrics.nodeid }}</code></td>
        <td><span class="cat {{ r.classification.category.value }}">{{ r.classification.category.value }}</span></td>
        <td>{{ "%.3f"|format(r.metrics.flakiness_score) }}</td>
        <td>{{ r.metrics.pass_count }}</td>
        <td>{{ r.metrics.fail_count }}</td>
        <td>{{ r.metrics.transition_count }}</td>
        <td>{{ "%.3f"|format(r.metrics.average_duration) }}</td>
        <td class="notes">{{ r.classification.rationale }}<br>{{ r.classification.notes|join("<br>") }}</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>

  <h2>Charts</h2>
  <div class="imgs">
    <img src="charts/top_flaky.png" alt="top flaky">
    <img src="charts/pass_fail_trend.png" alt="pass/fail trend">
    <img src="charts/flakiness_distribution.png" alt="flakiness distribution">
    <img src="charts/duration_variance.png" alt="duration variance">
    <img src="charts/heatmap.png" alt="heatmap">
  </div>
</body>
</html>
"""


def _test_reports_to_rows(reports: List[TestReport]) -> List[dict]:
    rows = []
    for r in reports:
        m = r.metrics
        rows.append({
            "nodeid": m.nodeid,
            "category": r.classification.category.value,
            "total_runs": m.total_runs,
            "executed_runs": m.executed_runs,
            "pass_count": m.pass_count,
            "fail_count": m.fail_count,
            "skip_count": m.skip_count,
            "error_count": m.error_count,
            "pass_rate": m.pass_rate,
            "fail_rate": m.fail_rate,
            "flakiness_score": m.flakiness_score,
            "transition_count": m.transition_count,
            "transition_rate": m.transition_rate,
            "longest_pass_streak": m.longest_pass_streak,
            "longest_fail_streak": m.longest_fail_streak,
            "average_duration": m.average_duration,
            "duration_stddev": m.duration_stddev,
            "infra_hits": m.infra_hits,
            "rationale": r.classification.rationale,
            "notes": " | ".join(r.classification.notes),
        })
    return rows


def write_summary_json(summary: ReportSummary, *, path: Path | None = None) -> Path:
    """Write the full summary to ``summary/summary.json``."""
    target = path or (settings.summary_dir / "summary.json")
    ensure_dir(target.parent)
    return write_json(target, summary.model_dump(mode="json"))


def write_metrics_csv(summary: ReportSummary, *, path: Path | None = None) -> Path:
    """Write a full per-test metrics table to CSV."""
    target = path or (settings.summary_dir / "test_metrics.csv")
    ensure_dir(target.parent)
    df = pd.DataFrame(_test_reports_to_rows(summary.test_reports))
    df.to_csv(target, index=False, encoding="utf-8")
    return target


def write_top_flaky_csv(summary: ReportSummary, *, path: Path | None = None, top_n: int = 20) -> Path:
    """Write the top-N worst offenders to CSV."""
    target = path or (settings.summary_dir / "top_flaky.csv")
    ensure_dir(target.parent)
    rows = _test_reports_to_rows(summary.worst_offenders[:top_n])
    df = pd.DataFrame(rows)
    df.to_csv(target, index=False, encoding="utf-8")
    return target


def write_raw_history_csv(
    suite_runs: List[SuiteRunResult], *, path: Path | None = None
) -> Path:
    """Write all per-run, per-test records to a flat CSV."""
    target = path or (settings.summary_dir / "raw_history.csv")
    ensure_dir(target.parent)
    rows: List[dict] = []
    for suite in suite_runs:
        for tc in suite.test_results:
            rows.append({
                "run_index": suite.run_index,
                "nodeid": tc.nodeid,
                "outcome": tc.outcome.value,
                "duration": tc.duration,
                "timestamp": tc.timestamp.isoformat(),
                "error_message": tc.error_message or "",
                "failure_signature": tc.failure_signature or "",
            })
    df = pd.DataFrame(rows)
    df.to_csv(target, index=False, encoding="utf-8")
    return target


def write_html_report(summary: ReportSummary, *, path: Path | None = None) -> Path:
    """Render a simple, self-contained HTML summary."""
    try:
        from jinja2 import Environment, BaseLoader, select_autoescape
    except ImportError as exc:  # pragma: no cover
        raise ReporterError("jinja2 is required for HTML report generation.") from exc

    target = path or settings.html_report_path
    ensure_dir(target.parent)
    env = Environment(loader=BaseLoader(), autoescape=select_autoescape(["html"]))
    tpl = env.from_string(_HTML_TEMPLATE)
    rendered = tpl.render(
        generated_at=summary.generated_at.isoformat(),
        pytest_target=summary.pytest_target,
        total_runs=summary.total_runs,
        total_tests=summary.total_tests,
        category_counts=summary.category_counts,
        worst_offenders=summary.worst_offenders,
    )
    target.write_text(rendered, encoding="utf-8")
    return target


def write_all_reports(
    summary: ReportSummary,
    suite_runs: List[SuiteRunResult] | None = None,
) -> dict[str, Path]:
    """Convenience wrapper to emit all artifacts at once."""
    paths: dict[str, Path] = {
        "summary_json": write_summary_json(summary),
        "metrics_csv": write_metrics_csv(summary),
        "top_flaky_csv": write_top_flaky_csv(summary),
        "html": write_html_report(summary),
    }
    if suite_runs is not None:
        paths["raw_history_csv"] = write_raw_history_csv(suite_runs)
    log.info("Wrote reports: %s", {k: str(v) for k, v in paths.items()})
    return paths
