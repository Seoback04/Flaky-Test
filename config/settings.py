"""Central configuration for the Flaky Test Detector.

All paths and defaults are resolved relative to the project root.
Environment variables (optionally loaded from a ``.env`` file) can override
the defaults without touching code.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

try:  # python-dotenv is optional at runtime
    from dotenv import load_dotenv

    load_dotenv()
except Exception:  # pragma: no cover - defensive
    pass


PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent.parent


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


def _env_float(name: str, default: float) -> float:
    try:
        return float(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


def _env_str(name: str, default: str) -> str:
    v = os.environ.get(name)
    return v if v else default


@dataclass(frozen=True)
class Settings:
    """Runtime-resolved settings."""

    project_root: Path = PROJECT_ROOT

    # Logging
    log_level: str = field(default_factory=lambda: _env_str("FTD_LOG_LEVEL", "INFO"))

    # Defaults for CLI
    default_runs: int = field(default_factory=lambda: _env_int("FTD_DEFAULT_RUNS", 10))
    default_delay: float = field(default_factory=lambda: _env_float("FTD_DEFAULT_DELAY", 0.0))
    default_tests: str = field(default_factory=lambda: _env_str("FTD_DEFAULT_TESTS", "demo"))

    # Directories
    output_dir_name: str = field(default_factory=lambda: _env_str("FTD_OUTPUT_DIR", "outputs"))

    @property
    def output_dir(self) -> Path:
        return self.project_root / self.output_dir_name

    @property
    def raw_dir(self) -> Path:
        return self.output_dir / "raw"

    @property
    def summary_dir(self) -> Path:
        return self.output_dir / "summary"

    @property
    def charts_dir(self) -> Path:
        return self.output_dir / "charts"

    @property
    def html_report_path(self) -> Path:
        return self.output_dir / "report.html"

    @property
    def log_file(self) -> Path:
        return self.output_dir / "flaky_detector.log"

    # Infra-suspect heuristics
    infra_keywords: tuple[str, ...] = (
        "timeout",
        "timed out",
        "connection error",
        "connection refused",
        "connection reset",
        "network",
        "dns",
        "browser crash",
        "webdriver",
        "selenium",
        "chromedriver",
        "setup error",
        "teardown error",
        "fixture error",
        "file lock",
        "permission denied",
        "resource busy",
        "service unavailable",
        "503",
        "504",
        "econnreset",
        "etimedout",
        "unreachable",
    )

    # Classification thresholds
    infra_dominance_threshold: float = 0.5  # fraction of failures matching infra keywords
    flaky_min_runs: int = 2  # below this, skip classification


settings = Settings()


def ensure_output_dirs() -> None:
    """Create the standard output directories if missing."""
    for p in (
        settings.output_dir,
        settings.raw_dir,
        settings.summary_dir,
        settings.charts_dir,
    ):
        p.mkdir(parents=True, exist_ok=True)
