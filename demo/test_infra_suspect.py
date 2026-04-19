"""Tests that simulate infra-suspect failures via keyword-rich error messages.

The messages contain phrases like ``timeout`` / ``connection error`` that the
detector's infra classifier will match.
"""

from __future__ import annotations

import random


def test_fake_network_timeout() -> None:
    """~40% fail with a 'timeout' message — looks infra-related."""
    if random.random() < 0.4:
        raise TimeoutError("Request timed out after 30s waiting for upstream service.")
    assert True


def test_fake_connection_error() -> None:
    """~30% fail with a 'connection error' message."""
    if random.random() < 0.3:
        raise ConnectionError("Connection error: connection refused by 10.0.0.5:8080.")
    assert True


def test_fake_service_unavailable() -> None:
    """~25% fail with '503 service unavailable'."""
    if random.random() < 0.25:
        raise RuntimeError("503 Service unavailable — downstream degraded.")
    assert True


def test_fake_browser_crash() -> None:
    """~20% fail with a webdriver/browser crash-style message."""
    if random.random() < 0.2:
        raise RuntimeError("Selenium webdriver: browser crash detected, chromedriver exited.")
    assert True
