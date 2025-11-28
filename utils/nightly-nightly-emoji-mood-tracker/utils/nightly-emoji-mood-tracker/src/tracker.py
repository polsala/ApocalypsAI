import argparse
import datetime
import hashlib
from typing import List, Tuple

# A small, whimsical palette of emojis representing "moods"
EMOJIS = [
    "😀",  # happy
    "😐",  # neutral
    "😔",  # sad
    "🤩",  # excited
    "🤖",  # robotic
    "🙃",  # playful
    "😎",  # cool
    "🥳",  # celebratory
    "😴",  # sleepy
    "🤔",  # thoughtful
]

def _emoji_for_date(date_str: str) -> str:
    """Return a deterministic emoji for a given ISO‑date string.

    The function hashes the date string with SHA‑256, interprets the digest as an
    integer, and takes the modulus with the length of ``EMOJIS``.
    """
    digest = hashlib.sha256(date_str.encode("utf-8")).hexdigest()
    idx = int(digest, 16) % len(EMOJIS)
    return EMOJIS[idx]


def generate_mood_calendar(start: str, end: str) -> List[Tuple[str, str]]:
    """Generate a list of ``(date, emoji)`` tuples for the inclusive range.

    Args:
        start: ISO‑formatted start date (e.g., ``"2023-01-01"``).
        end:   ISO‑formatted end date (e.g., ``"2023-01-07"``).

    Returns:
        A list of tuples where each tuple contains the date string and its
        corresponding emoji.

    Raises:
        ValueError: If ``start`` is after ``end`` or if the date strings are
        malformed.
    """
    try:
        start_dt = datetime.date.fromisoformat(start)
        end_dt = datetime.date.fromisoformat(end)
    except Exception as exc:
        raise ValueError(f"Invalid ISO date format: {exc}") from exc

    if start_dt > end_dt:
        raise ValueError("Start date must not be after end date")

    delta = datetime.timedelta(days=1)
    current = start_dt
    result: List[Tuple[str, str]] = []
    while current <= end_dt:
        date_str = current.isoformat()
        emoji = _emoji_for_date(date_str)
        result.append((date_str, emoji))
        current += delta
    return result


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a deterministic emoji mood calendar for a date range"
    )
    parser.add_argument("--start", required=True, help="Start date (ISO format, e.g., 2023-01-01)")
    parser.add_argument("--end", required=True, help="End date (ISO format, inclusive)")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    try:
        calendar = generate_mood_calendar(args.start, args.end)
    except ValueError as e:
        print(f"Error: {e}")
        raise SystemExit(1)
    for date_str, emoji in calendar:
        print(f"{date_str}: {emoji}")


if __name__ == "__main__":
    main()
