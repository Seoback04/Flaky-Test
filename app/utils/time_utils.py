"""Time / duration helpers."""

from __future__ import annotations

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Return a timezone-aware UTC ``datetime``."""
    return datetime.now(tz=timezone.utc)


def iso(dt: datetime) -> str:
    """Return ``dt`` as ISO-8601 string."""
    return dt.isoformat()


def elapsed_seconds(start: datetime, end: datetime) -> float:
    """Return positive seconds between ``start`` and ``end``."""
    return max(0.0, (end - start).total_seconds())
