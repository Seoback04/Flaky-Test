"""Custom exception hierarchy for the Flaky Test Detector."""

from __future__ import annotations


class FlakyDetectorError(Exception):
    """Base class for all Flaky Test Detector errors."""


class RunnerError(FlakyDetectorError):
    """Raised when the pytest runner encounters a non-recoverable issue."""


class ParserError(FlakyDetectorError):
    """Raised when parsing a JSON report fails."""


class AnalyzerError(FlakyDetectorError):
    """Raised when analysis of aggregated results fails."""


class ReporterError(FlakyDetectorError):
    """Raised when report generation fails."""


class VisualizerError(FlakyDetectorError):
    """Raised when chart generation fails."""
