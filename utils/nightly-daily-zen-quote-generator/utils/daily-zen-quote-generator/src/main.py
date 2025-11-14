#!/usr/bin/env python3
"""
Daily Zen Quote Generator

Selects a deterministic quote based on the current date.
"""

import json
import pathlib
import sys
from datetime import date, datetime
from typing import List

# Load quotes from the bundled JSON file
_QUOTE_PATH = pathlib.Path(__file__).with_name("quotes.json")
with _QUOTE_PATH.open(encoding="utf-8") as f:
    _QUOTES: List[str] = json.load(f)


def _date_key(d: date) -> int:
    """Convert a date to an integer key YYYYMMDD."""
    return d.year * 10000 + d.month * 100 + d.day


def get_quote(target_date: date | None = None) -> str:
    """
    Return the quote for the given date.

    If ``target_date`` is ``None`` the current UTC date is used.
    The selection is deterministic: ``_date_key(date) % len(_QUOTES)``.
    """
    if target_date is None:
        target_date = datetime.utcnow().date()
    index = _date_key(target_date) % len(_QUOTES)
    return _QUOTES[index]


def main() -> None:
    """CLI entry point."""
    quote = get_quote()
    print(quote)


if __name__ == "__main__":
    main()
