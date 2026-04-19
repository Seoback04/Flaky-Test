"""Centralized structured logger for the Flaky Test Detector."""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from config.settings import settings

_LOG_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_configured = False


def get_logger(name: str = "ftd", log_file: Optional[Path] = None) -> logging.Logger:
    """Return a singleton, structured logger writing to console and file."""
    global _configured
    logger = logging.getLogger(name)

    if _configured:
        return logger

    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(level)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler (best-effort)
    try:
        target = log_file or settings.log_file
        target.parent.mkdir(parents=True, exist_ok=True)
        fh = RotatingFileHandler(target, maxBytes=2_000_000, backupCount=3, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except Exception as exc:  # pragma: no cover - defensive
        logger.warning("Could not attach file log handler: %s", exc)

    _configured = True
    return logger
