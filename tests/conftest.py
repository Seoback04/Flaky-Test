"""Shared fixtures and path setup for the detector's own tests."""

from __future__ import annotations

import sys
from pathlib import Path

# Make project root importable for `import app`, `import config`
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
