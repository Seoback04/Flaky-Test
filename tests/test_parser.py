"""Unit tests for the pytest-json-report parser."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.models import Outcome
from app.parser import parse_json_report
from app.exceptions import ParserError


def _write_report(tmp_path: Path, payload: dict, name: str = "run_001.json") -> Path:
    p = tmp_path / name
    p.write_text(json.dumps(payload), encoding="utf-8")
    return p


def test_parse_basic_report(tmp_path: Path) -> None:
    report_path = _write_report(
        tmp_path,
        {
            "created": 1700000000.0,
            "duration": 1.5,
            "exitcode": 1,
            "tests": [
                {"nodeid": "demo/test_a.py::t1", "outcome": "passed", "duration": 0.1},
                {
                    "nodeid": "demo/test_a.py::t2",
                    "outcome": "failed",
                    "duration": 0.2,
                    "call": {"outcome": "failed", "longrepr": "AssertionError: boom"},
                },
                {"nodeid": "demo/test_a.py::t3", "outcome": "skipped", "duration": 0.0},
            ],
        },
    )
    result = parse_json_report(report_path, run_index=1, pytest_target="demo")
    assert result.run_index == 1
    assert result.return_code == 1
    assert result.total == 3
    assert result.passed == 1
    assert result.failed == 1
    assert result.skipped == 1

    t2 = next(t for t in result.test_results if t.nodeid.endswith("t2"))
    assert t2.outcome == Outcome.FAILED
    assert "AssertionError" in (t2.error_message or "")
    assert t2.failure_signature is not None


def test_parse_setup_error_becomes_error(tmp_path: Path) -> None:
    report_path = _write_report(
        tmp_path,
        {
            "created": 1700000000.0,
            "duration": 1.0,
            "exitcode": 1,
            "tests": [
                {
                    "nodeid": "t::x",
                    "outcome": "failed",
                    "duration": 0.01,
                    "setup": {"outcome": "error", "longrepr": "fixture broke"},
                    "call": {"outcome": "failed"},
                }
            ],
        },
    )
    result = parse_json_report(report_path, run_index=2, pytest_target="demo")
    assert result.test_results[0].outcome == Outcome.ERROR


def test_parse_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(ParserError):
        parse_json_report(tmp_path / "missing.json", run_index=1, pytest_target="demo")


def test_parse_invalid_json_raises(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text("{not json", encoding="utf-8")
    with pytest.raises(ParserError):
        parse_json_report(p, run_index=1, pytest_target="demo")


def test_parse_empty_tests_array(tmp_path: Path) -> None:
    report_path = _write_report(
        tmp_path,
        {"created": 1700000000.0, "duration": 0.0, "exitcode": 5, "tests": []},
    )
    result = parse_json_report(report_path, run_index=1, pytest_target="demo")
    assert result.total == 0
    assert result.return_code == 5
