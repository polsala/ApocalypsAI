"""quote.py – deterministic quote‑of‑the‑day utility.

The module exposes a `get_quote` function and a tiny CLI.
It selects a quote based on the ISO calendar day number (1‑366) and
optionally filters by a tag.
"""

import json
import sys
from datetime import date
from pathlib import Path
from typing import List, Dict, Optional

# Path to the bundled JSON file (relative to this file)
_QUOTE_FILE = Path(__file__).with_name("quotes.json")


def _load_quotes() -> List[Dict[str, object]]:
    """Load the quote database.

    Returns a list of dictionaries with keys:
        - "text": the quote string
        - "author": author name
        - "tags": list of tags (optional)
    """
    with _QUOTE_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def _filter_by_tag(quotes: List[Dict[str, object]], tag: Optional[str]) -> List[Dict[str, object]]:
    if not tag:
        return quotes
    tag_lower = tag.lower()
    return [q for q in quotes if tag_lower in [t.lower() for t in q.get("tags", [])]]


def _pick_quote(quotes: List[Dict[str, object]], today: date) -> Dict[str, object]:
    """Deterministically pick a quote based on the day of year.

    The algorithm is simple: `index = day_of_year % len(quotes)`.
    This guarantees the same quote for a given date across runs.
    """
    if not quotes:
        raise ValueError("No quotes available after filtering.")
    day_of_year = today.timetuple().tm_yday  # 1‑366
    index = day_of_year % len(quotes)
    return quotes[index]


def get_quote(tag: Optional[str] = None, today: Optional[date] = None) -> str:
    """Return a formatted quote string.

    Parameters
    ----------
    tag: Optional[str]
        If provided, only quotes containing this tag are considered.
    today: Optional[date]
        Allows injection of a custom date (useful for testing). If omitted,
        the current UTC date is used.
    """
    quotes = _load_quotes()
    quotes = _filter_by_tag(quotes, tag)
    chosen = _pick_quote(quotes, today or date.today())
    text = chosen["text"]
    author = chosen.get("author", "Unknown")
    return f"\"{text}\" — {author}"


def _parse_args(argv: List[str]) -> Optional[str]:
    """Very small CLI parser – returns the tag if supplied.

    Expected usage:
        python -m quote [--tag <tag>]
    """
    if "--tag" in argv:
        idx = argv.index("--tag")
        try:
            return argv[idx + 1]
        except IndexError:
            print("Error: --tag requires a value", file=sys.stderr)
            sys.exit(1)
    return None


def main() -> None:
    tag = _parse_args(sys.argv[1:])
    try:
        print(get_quote(tag))
    except Exception as exc:
        print(f"Failed to retrieve quote: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
