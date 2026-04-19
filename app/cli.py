"""Typer-based CLI for the Flaky Test Detector.

Commands:

* ``run``    — execute a pytest target N times and analyze.
* ``analyze``— (re)analyze existing raw JSON reports.
* ``report`` — regenerate reports from a previously-written summary JSON.
* ``demo``   — one-shot run of the bundled demo suite.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from config.settings import ensure_output_dirs, settings

from .analyzer import analyze
from .logger import get_logger
from .models import Category, ReportSummary, SuiteRunResult
from .parser import parse_json_report
from .reporter import write_all_reports
from .runner import PytestRunner, RunnerConfig
from .utils.file_io import list_json_files, read_json
from .visualizer import generate_all_charts

app = typer.Typer(
    add_completion=False,
    help="Flaky Test Detector — run, analyze, and report on flaky pytest tests.",
    no_args_is_help=True,
)
console = Console()
log = get_logger(__name__)


# ---- helpers ---------------------------------------------------------------
def _print_summary_table(summary: ReportSummary) -> None:
    console.print(
        f"[bold]Total runs:[/bold] {summary.total_runs}   "
        f"[bold]Total tests:[/bold] {summary.total_tests}"
    )
    cats = Table(title="Categories", show_header=True, header_style="bold")
    cats.add_column("Category")
    cats.add_column("Count", justify="right")
    for cat, count in summary.category_counts.items():
        cats.add_row(cat, str(count))
    console.print(cats)

    if not summary.worst_offenders:
        console.print("[green]No flaky / unstable tests detected.[/green]")
        return

    t = Table(title="Top flaky / unstable tests", show_lines=False, header_style="bold")
    t.add_column("Test")
    t.add_column("Category")
    t.add_column("Flaky", justify="right")
    t.add_column("Pass", justify="right")
    t.add_column("Fail", justify="right")
    t.add_column("Trans.", justify="right")
    t.add_column("Avg dur", justify="right")
    for r in summary.worst_offenders:
        color = {
            Category.STABLE_FAIL: "red",
            Category.FLAKY: "yellow",
            Category.INFRA_SUSPECT: "cyan",
        }.get(r.category, "white")
        t.add_row(
            r.metrics.nodeid,
            f"[{color}]{r.category.value}[/{color}]",
            f"{r.metrics.flakiness_score:.3f}",
            str(r.metrics.pass_count),
            str(r.metrics.fail_count),
            str(r.metrics.transition_count),
            f"{r.metrics.average_duration:.3f}",
        )
    console.print(t)


def _load_suite_runs_from_raw(raw_dir: Path, pytest_target: str) -> List[SuiteRunResult]:
    files = list_json_files(raw_dir, "run_*.json")
    if not files:
        raise typer.BadParameter(f"No run_*.json files found under {raw_dir}")
    suite_runs: List[SuiteRunResult] = []
    for i, f in enumerate(files, start=1):
        try:
            suite_runs.append(
                parse_json_report(
                    report_path=f,
                    run_index=i,
                    pytest_target=pytest_target,
                )
            )
        except Exception as exc:  # defensive; skip broken reports
            log.warning("Skipping unparsable report %s: %s", f, exc)
    if not suite_runs:
        raise typer.BadParameter(f"No parseable reports in {raw_dir}")
    return suite_runs


# ---- commands --------------------------------------------------------------
@app.command("run")
def cmd_run(
    tests: str = typer.Option(
        settings.default_tests, "--tests", "-t", help="Pytest target path."
    ),
    runs: int = typer.Option(
        settings.default_runs, "--runs", "-n", min=1, help="Number of runs."
    ),
    delay: float = typer.Option(
        settings.default_delay, "--delay", "-d", min=0.0, help="Delay seconds between runs."
    ),
    keyword: Optional[str] = typer.Option(None, "-k", help="pytest -k keyword filter."),
    marker: Optional[str] = typer.Option(None, "-m", help="pytest -m marker filter."),
    top_n: int = typer.Option(10, "--top", help="Top-N for reports."),
    no_charts: bool = typer.Option(False, "--no-charts", help="Skip chart generation."),
) -> None:
    """Run a pytest suite N times and produce analysis + reports."""
    ensure_output_dirs()
    cfg = RunnerConfig(target=tests, runs=runs, delay=delay, keyword=keyword, marker=marker)
    runner = PytestRunner(cfg)
    console.rule("[bold]Executing test suite[/bold]")
    suite_runs = runner.run_all()
    console.rule("[bold]Analyzing results[/bold]")
    summary = analyze(suite_runs, pytest_target=tests, top_n=top_n)
    write_all_reports(summary, suite_runs=suite_runs)
    if not no_charts:
        generate_all_charts(summary, suite_runs)
    _print_summary_table(summary)
    console.print(f"\n[green]Reports written to[/green] {settings.output_dir}")


@app.command("analyze")
def cmd_analyze(
    input_dir: Path = typer.Option(
        settings.raw_dir, "--input", "-i", help="Directory with raw run_*.json reports."
    ),
    tests: str = typer.Option(
        settings.default_tests, "--tests", "-t", help="Original pytest target (metadata)."
    ),
    top_n: int = typer.Option(10, "--top", help="Top-N for reports."),
    no_charts: bool = typer.Option(False, "--no-charts", help="Skip chart generation."),
) -> None:
    """Analyze existing raw JSON reports and regenerate artifacts."""
    ensure_output_dirs()
    suite_runs = _load_suite_runs_from_raw(input_dir, pytest_target=tests)
    summary = analyze(suite_runs, pytest_target=tests, top_n=top_n)
    write_all_reports(summary, suite_runs=suite_runs)
    if not no_charts:
        generate_all_charts(summary, suite_runs)
    _print_summary_table(summary)
    console.print(f"\n[green]Reports written to[/green] {settings.output_dir}")


@app.command("report")
def cmd_report(
    input_dir: Path = typer.Option(
        settings.summary_dir, "--input", "-i", help="Directory containing summary.json."
    ),
) -> None:
    """Reprint a previously-generated summary (no re-analysis)."""
    summary_path = input_dir / "summary.json"
    if not summary_path.exists():
        raise typer.BadParameter(f"No summary.json found in {input_dir}")
    data = read_json(summary_path)
    summary = ReportSummary.model_validate(data)
    _print_summary_table(summary)
    console.print(f"\n[green]Report at[/green] {summary_path}")


@app.command("demo")
def cmd_demo(
    runs: int = typer.Option(15, "--runs", "-n", min=1),
    delay: float = typer.Option(0.0, "--delay", "-d", min=0.0),
    top_n: int = typer.Option(10, "--top"),
) -> None:
    """Run the bundled demo suite and produce all artifacts."""
    cmd_run(
        tests="demo",
        runs=runs,
        delay=delay,
        keyword=None,
        marker=None,
        top_n=top_n,
        no_charts=False,
    )


if __name__ == "__main__":
    app()
