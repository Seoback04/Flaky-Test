"""Parser for pytest-json-report output into our domain models.

The ``pytest-json-report`` plugin produces a structured JSON document per run.
We normalize it into :class:`SuiteRunResult` + :class:`TestCaseResult` objects
so downstream layers never see raw plugin shapes.

Reference shape (pytest-json-report v1.5+):

.. code-block:: json

    {
      "created": 1700000000.0,
      "duration": 1.23,
      "exitcode": 0,
      "root": "/path/to/project",
      "summary": {"total": 4, "passed": 3, "failed": 1},
      "tests": [
        {
          "nodeid": "demo/test_x.py::test_a",
          "outcome": "passed",
          "duration": 0.01,
          "call": {"longrepr": "..."},
          "setup": {"outcome": "passed"},
          "teardown": {"outcome": "passed"}
        }
      ]
    }
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .exceptions import ParserError
from .logger import get_logger
from .models import Outcome, SuiteRunResult, TestCaseResult
from .utils.file_io import read_json
from .utils.text_utils import failure_signature, shorten

log = get_logger(__name__)


_OUTCOME_MAP: Dict[str, Outcome] = {
    "passed": Outcome.PASSED,
    "failed": Outcome.FAILED,
    "skipped": Outcome.SKIPPED,
    "error": Outcome.ERROR,
    "xfailed": Outcome.XFAILED,
    "xpassed": Outcome.XPASSED,
}


def _normalize_outcome(raw: Any) -> Outcome:
    if not isinstance(raw, str):
        return Outcome.UNKNOWN
    return _OUTCOME_MAP.get(raw.lower(), Outcome.UNKNOWN)


def _extract_error_message(test_entry: Dict[str, Any]) -> Optional[str]:
    """Pull an error message out of setup/call/teardown sections, if any."""
    for phase in ("setup", "call", "teardown"):
        section = test_entry.get(phase) or {}
        outcome = (section.get("outcome") or "").lower()
        if outcome in {"failed", "error"}:
            longrepr = section.get("longrepr") or section.get("crash", {}).get("message")
            if longrepr:
                return str(longrepr)
    # Fallback to top-level longrepr if present
    longrepr = test_entry.get("longrepr")
    return str(longrepr) if longrepr else None


def _entry_outcome(test_entry: Dict[str, Any]) -> Outcome:
    """Combined outcome: if setup/teardown errored, surface that."""
    for phase in ("setup", "teardown"):
        section = test_entry.get(phase) or {}
        if (section.get("outcome") or "").lower() in {"failed", "error"}:
            return Outcome.ERROR
    return _normalize_outcome(test_entry.get("outcome"))


def parse_json_report(
    report_path: Path,
    run_index: int,
    pytest_target: str,
    keyword_filter: Optional[str] = None,
    marker_filter: Optional[str] = None,
) -> SuiteRunResult:
    """Parse a single ``pytest-json-report`` JSON file into a SuiteRunResult."""
    report_path = Path(report_path)
    if not report_path.exists():
        raise ParserError(f"Report file does not exist: {report_path}")

    try:
        data = read_json(report_path)
    except Exception as exc:
        raise ParserError(f"Failed to read JSON report {report_path}: {exc}") from exc

    try:
        created_ts = float(data.get("created") or 0.0)
        duration = float(data.get("duration") or 0.0)
        exitcode = int(data.get("exitcode") or 0)
        started_at = datetime.fromtimestamp(created_ts, tz=timezone.utc) if created_ts else datetime.now(timezone.utc)
        ended_at = datetime.fromtimestamp(created_ts + duration, tz=timezone.utc) if created_ts else started_at

        raw_tests: List[Dict[str, Any]] = list(data.get("tests") or [])
        test_results: List[TestCaseResult] = []

        for entry in raw_tests:
            nodeid = str(entry.get("nodeid") or "").strip()
            if not nodeid:
                continue
            outcome = _entry_outcome(entry)
            dur = float(entry.get("duration") or 0.0)
            err_full = _extract_error_message(entry) if outcome.is_fail else None
            err_short = shorten(err_full, max_len=500) if err_full else None
            sig = failure_signature(err_full) if err_full else None

            test_results.append(
                TestCaseResult(
                    nodeid=nodeid,
                    outcome=outcome,
                    duration=dur,
                    run_index=run_index,
                    timestamp=started_at,
                    error_message=err_short,
                    failure_signature=sig,
                )
            )

        return SuiteRunResult(
            run_index=run_index,
            started_at=started_at,
            ended_at=ended_at,
            duration=duration,
            return_code=exitcode,
            pytest_target=pytest_target,
            keyword_filter=keyword_filter,
            marker_filter=marker_filter,
            test_results=test_results,
            report_path=str(report_path),
        )
    except ParserError:
        raise
    except Exception as exc:
        log.exception("Unexpected error parsing %s", report_path)
        raise ParserError(f"Unexpected error parsing {report_path}: {exc}") from exc
