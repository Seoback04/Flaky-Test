"""Text / message helpers (failure signatures, keyword matching)."""

from __future__ import annotations

import hashlib
import re
from typing import Iterable, Optional


_WHITESPACE_RE = re.compile(r"\s+")
_PATH_RE = re.compile(r"([A-Za-z]:)?[\\/][\w\-./\\]+")
_HEX_RE = re.compile(r"0x[0-9a-fA-F]+")
_NUM_RE = re.compile(r"\b\d{2,}\b")


def shorten(text: Optional[str], max_len: int = 160) -> str:
    """Truncate long messages for display/reporting."""
    if not text:
        return ""
    text = text.strip()
    return text if len(text) <= max_len else text[: max_len - 1] + "…"


def normalize_message(text: Optional[str]) -> str:
    """Normalize a failure message for deduplication/signature hashing."""
    if not text:
        return ""
    t = text.strip().lower()
    t = _PATH_RE.sub("<path>", t)
    t = _HEX_RE.sub("<hex>", t)
    t = _NUM_RE.sub("<n>", t)
    t = _WHITESPACE_RE.sub(" ", t)
    return t


def failure_signature(text: Optional[str]) -> Optional[str]:
    """Return a short stable signature (sha1[:10]) for a failure message."""
    norm = normalize_message(text)
    if not norm:
        return None
    return hashlib.sha1(norm.encode("utf-8")).hexdigest()[:10]


def contains_any_keyword(text: Optional[str], keywords: Iterable[str]) -> bool:
    """Case-insensitive check whether ``text`` contains any keyword."""
    if not text:
        return False
    low = text.lower()
    return any(k.lower() in low for k in keywords)
