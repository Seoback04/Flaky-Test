"""Deterministic tests: some always pass, one always fails.

Run via the detector to see these land in ``stable_pass`` / ``stable_fail``.
"""

from __future__ import annotations


def test_stable_addition_passes() -> None:
    assert 1 + 1 == 2


def test_stable_string_passes() -> None:
    assert "flaky".upper() == "FLAKY"


def test_stable_list_passes() -> None:
    items = [1, 2, 3]
    assert sum(items) == 6


def test_stable_always_fails() -> None:
    # Intentional stable failure (simulates a real bug)
    assert 2 + 2 == 5, "Expected 5 but got 4 (this is an intentional stable failure)."
