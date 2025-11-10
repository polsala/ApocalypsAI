#!/usr/bin/env python3
"""
Daily Zen Quote Generator
"""

import argparse
import json
import pathlib
import sys
from datetime import date

def load_quotes():
    """Load quotes from the bundled JSON file."""
    quotes_path = pathlib.Path(__file__).with_name("quotes.json")
    with quotes_path.open(encoding="utf-8") as f:
        return json.load(f)

def pick_quote(quotes, today=None):
    """Pick a deterministic quote based on the given date."""
    today = today or date.today()
    index = today.toordinal() % len(quotes)
    return quotes[index]

def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Print a Zen‑style quote of the day."
    )
    args = parser.parse_args(argv)

    quotes = load_quotes()
    quote = pick_quote(quotes)
    print(quote)

if __name__ == "__main__":
    sys.exit(main())
