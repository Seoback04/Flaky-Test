"""Top-level entrypoint for the Flaky Test Detector CLI.

Run with:  python main.py --help
"""

from __future__ import annotations

from app.cli import app


def main() -> None:
    """Invoke the Typer CLI app."""
    app()


if __name__ == "__main__":
    main()
