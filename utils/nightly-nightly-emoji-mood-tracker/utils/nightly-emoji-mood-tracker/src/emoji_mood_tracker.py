import argparse
import datetime
import hashlib
import sys
from typing import List, Tuple

# List of emojis representing various moods. Feel free to extend.
EMOJIS = [
    "😀", "😐", "😔", "🤩", "😎", "🤔", "😡", "🥳", "😴", "🤖",
    "🌟", "🌧️", "☀️", "🌈", "💤", "🔥", "💧", "🍀", "⚡", "🌀",
]


def _hash_date(date: datetime.date) -> int:
    """Return an integer hash for *date* using SHA‑256.

    The hash is deterministic and independent of the runtime environment.
    """
    iso = date.isoformat().encode("utf-8")
    digest = hashlib.sha256(iso).hexdigest()
    # Convert a slice of the hex digest to an int for indexing.
    return int(digest[:8], 16)


def mood_for_date(date: datetime.date) -> str:
    """Return the emoji mood for *date*.

    The emoji is selected by hashing the date and taking the result modulo the
    number of available emojis.
    """
    idx = _hash_date(date) % len(EMOJIS)
    return EMOJIS[idx]


def mood_for_range(start: datetime.date, end: datetime.date) -> List[Tuple[datetime.date, str]]:
    """Return a list of ``(date, emoji)`` tuples for the inclusive range.

    Raises:
        ValueError: If *start* is after *end*.
    """
    if start > end:
        raise ValueError("start date must not be after end date")
    delta = datetime.timedelta(days=1)
    current = start
    results: List[Tuple[datetime.date, str]] = []
    while current <= end:
        results.append((current, mood_for_date(current)))
        current += delta
    return results


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deterministic emoji mood tracker")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="Specific date (YYYY-MM-DD). Defaults to today.",
    )
    group.add_argument(
        "--range",
        nargs=2,
        metavar=("START", "END"),
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d").date(),
        help="Inclusive date range (YYYY-MM-DD YYYY-MM-DD).",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.range:
        start, end = args.range
        try:
            entries = mood_for_range(start, end)
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        for d, emoji in entries:
            print(f"{d.isoformat()}: {emoji}")
    else:
        target_date = args.date or datetime.date.today()
        print(f"{target_date.isoformat()}: {mood_for_date(target_date)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
