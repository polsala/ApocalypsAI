"""emoji_mood_logger
====================

A tiny library that converts a list of mood entries into an emoji‑based daily summary.

Public API
----------

- :func:`load_entries(path: str) -> list[dict]`
- :func:`summarize_moods(entries: list[dict]) -> str`
- :func:`main(argv: list[str] | None = None) -> int`

The module can also be executed as a script::

    python -m src.logger <path-to-json>
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable, List, Tuple

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _emoji_for_average(avg: float) -> str:
    """Return an emoji representing the average mood.

    The mapping mirrors the table in the README.
    """
    if avg <= 1.5:
        return "😢"
    if avg <= 2.5:
        return "🙁"
    if avg <= 3.5:
        return "😐"
    if avg <= 4.5:
        return "🙂"
    return "😄"


def load_entries(path: str | Path) -> List[dict]:
    """Load mood entries from a JSON file.

    The JSON must be an array of objects with ``date`` (ISO‑8601 string) and
    ``mood`` (int 1‑5).  Invalid entries raise :class:`ValueError`.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Mood file not found: {p}")
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Root JSON element must be a list")
    for entry in data:
        if not isinstance(entry, dict) or "date" not in entry or "mood" not in entry:
            raise ValueError(f"Invalid entry format: {entry}")
        if not isinstance(entry["mood"], int) or not (1 <= entry["mood"] <= 5):
            raise ValueError(f"Mood must be int 1‑5: {entry}")
    return data


def summarize_moods(entries: Iterable[dict]) -> str:
    """Return a multi‑line string summarising moods per day.

    Example output::

        2025-11-01: 🙂
        2025-11-02: 😄
    """
    daily: defaultdict[str, List[int]] = defaultdict(list)
    for entry in entries:
        daily[entry["date"]].append(entry["mood"])
    lines: List[str] = []
    for date in sorted(daily):
        avg = sum(daily[date]) / len(daily[date])
        emoji = _emoji_for_average(avg)
        lines.append(f"{date}: {emoji}")
    return "\n".join(lines)


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    Usage: ``python -m src.logger <path-to-json>``
    Returns exit code 0 on success, 1 on error.
    """
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python -m src.logger <path-to-json>", file=sys.stderr)
        return 1
    try:
        entries = load_entries(argv[0])
        summary = summarize_moods(entries)
        print(summary)
        return 0
    except Exception as exc:  # pragma: no cover – defensive
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
