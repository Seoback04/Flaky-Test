"""Repeated pytest suite runner.

The runner invokes ``pytest`` as a subprocess, N times, capturing a structured
JSON report for each run via the ``pytest-json-report`` plugin. It is
deliberately tolerant of individual-run failures: a crash in run k does not
prevent runs k+1..N from executing.
"""

from __future__ import annotations

import shlex
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from config.settings import ensure_output_dirs, settings

from .exceptions import RunnerError
from .logger import get_logger
from .models import SuiteRunResult
from .parser import parse_json_report
from .utils.file_io import ensure_dir
from .utils.time_utils import utcnow

log = get_logger(__name__)


@dataclass
class RunnerConfig:
    """Configuration for a repeated-execution session."""

    target: str
    runs: int = 10
    delay: float = 0.0
    keyword: Optional[str] = None
    marker: Optional[str] = None
    raw_dir: Path = settings.raw_dir
    extra_pytest_args: Optional[List[str]] = None
    python_executable: str = sys.executable

    def validate(self) -> None:
        if self.runs < 1:
            raise RunnerError(f"runs must be >= 1, got {self.runs}")
        if self.delay < 0:
            raise RunnerError(f"delay must be >= 0, got {self.delay}")


class PytestRunner:
    """Repeatedly invoke pytest and collect SuiteRunResult objects."""

    def __init__(self, config: RunnerConfig) -> None:
        self.config = config
        self.config.validate()
        ensure_output_dirs()
        ensure_dir(self.config.raw_dir)

    # ---- helpers -------------------------------------------------------
    def _report_path(self, run_index: int) -> Path:
        return self.config.raw_dir / f"run_{run_index:03d}.json"

    def _build_command(self, run_index: int) -> List[str]:
        cmd: List[str] = [
            self.config.python_executable,
            "-m",
            "pytest",
            self.config.target,
            "--json-report",
            f"--json-report-file={self._report_path(run_index)}",
            "--json-report-indent=2",
            "-q",
        ]
        if self.config.keyword:
            cmd += ["-k", self.config.keyword]
        if self.config.marker:
            cmd += ["-m", self.config.marker]
        if self.config.extra_pytest_args:
            cmd += list(self.config.extra_pytest_args)
        return cmd

    def _run_once(self, run_index: int) -> SuiteRunResult:
        report_path = self._report_path(run_index)
        cmd = self._build_command(run_index)
        log.info("Run %d/%d: %s", run_index, self.config.runs, " ".join(shlex.quote(c) for c in cmd))

        started_at = utcnow()
        try:
            completed = subprocess.run(
                cmd,
                check=False,
                text=True,
                capture_output=True,
                cwd=str(settings.project_root),
            )
        except FileNotFoundError as exc:
            raise RunnerError(f"Failed to invoke pytest: {exc}") from exc
        except Exception as exc:  # pragma: no cover - defensive
            raise RunnerError(f"Unexpected runner error: {exc}") from exc

        ended_at = utcnow()
        log.debug("Run %d exitcode=%s", run_index, completed.returncode)
        if completed.returncode not in (0, 1, 2, 3, 4, 5):
            # pytest exit codes 0-5 are expected; anything else is unusual
            log.warning("Unusual pytest exit code: %s", completed.returncode)
        if completed.stderr:
            log.debug("pytest stderr (run %d): %s", run_index, completed.stderr.strip()[:500])

        if not report_path.exists():
            # pytest-json-report didn't write a file; log stdout/stderr for debugging
            log.error(
                "JSON report missing for run %d. stdout=%s | stderr=%s",
                run_index,
                (completed.stdout or "").strip()[:400],
                (completed.stderr or "").strip()[:400],
            )
            raise RunnerError(
                f"pytest-json-report did not produce {report_path}. "
                "Is the plugin installed? (pip install pytest-json-report)"
            )

        result = parse_json_report(
            report_path=report_path,
            run_index=run_index,
            pytest_target=self.config.target,
            keyword_filter=self.config.keyword,
            marker_filter=self.config.marker,
        )
        # override timestamps with wall-clock values (more accurate)
        result.started_at = started_at
        result.ended_at = ended_at
        result.return_code = completed.returncode
        return result

    # ---- public API ----------------------------------------------------
    def run_all(self) -> List[SuiteRunResult]:
        """Execute the suite N times and return all :class:`SuiteRunResult`."""
        results: List[SuiteRunResult] = []
        for i in range(1, self.config.runs + 1):
            try:
                results.append(self._run_once(i))
            except RunnerError as exc:
                log.error("Run %d failed to produce results: %s", i, exc)
            except Exception:
                log.exception("Unexpected failure in run %d", i)
            if i < self.config.runs and self.config.delay > 0:
                time.sleep(self.config.delay)
        if not results:
            raise RunnerError("All runs failed to produce a parseable report.")
        log.info("Completed %d/%d runs successfully.", len(results), self.config.runs)
        return results
