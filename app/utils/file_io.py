"""File-I/O helpers (JSON, directories)."""

from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, List, Union

PathLike = Union[str, Path]


def ensure_dir(path: PathLike) -> Path:
    """Create ``path`` (recursively) if it does not exist and return it."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def _json_default(obj: Any) -> Any:
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, Path):
        return str(obj)
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def write_json(path: PathLike, data: Any, *, indent: int = 2) -> Path:
    """Write ``data`` as JSON to ``path`` (pretty-printed by default)."""
    p = Path(path)
    ensure_dir(p.parent)
    p.write_text(
        json.dumps(data, indent=indent, default=_json_default, ensure_ascii=False),
        encoding="utf-8",
    )
    return p


def read_json(path: PathLike) -> Any:
    """Read and decode a JSON file."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def list_json_files(directory: PathLike, pattern: str = "run_*.json") -> List[Path]:
    """Return sorted list of JSON files in ``directory`` matching ``pattern``."""
    p = Path(directory)
    if not p.exists():
        return []
    return sorted(p.glob(pattern))


def iter_lines(paths: Iterable[PathLike]) -> Iterable[str]:
    """Utility iterator over lines in multiple files (UTF-8)."""
    for path in paths:
        with Path(path).open(encoding="utf-8") as f:
            for line in f:
                yield line.rstrip("\n")
