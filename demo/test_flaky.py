"""Intentionally flaky tests driven by randomness.

Each test uses ``random`` without a fixed seed so outcomes differ across runs.
"""

from __future__ import annotations

import random
import time


def test_random_50_50() -> None:
    """~50/50 pass/fail. Maximally flaky."""
    assert random.random() < 0.5, "Random coin-flip failed."


def test_random_mostly_passes() -> None:
    """~85% pass rate."""
    assert random.random() < 0.85, "Mostly-passing test happened to fail."


def test_random_mostly_fails() -> None:
    """~80% fail rate (a bad, high-failure-rate flaky test)."""
    assert random.random() < 0.2, "Mostly-failing test passed by chance."


def test_slow_and_sometimes_fails() -> None:
    """Simulates timing-sensitive flakiness — variable duration."""
    # random small sleep
    time.sleep(random.uniform(0.01, 0.15))
    # 30% chance of failure
    assert random.random() > 0.3, "Timing-sensitive test failed under load."
