import sys
import datetime
from typing import List

# A curated list of mood‑representing emojis.
MOOD_EMOJIS: List[str] = [
    "😀",  # Happy
    "🙂",  # Slightly happy
    "😐",  # Neutral
    "🙁",  # Slightly sad
    "😢",  # Sad
    "🤔",  # Thoughtful
    "🤩",  # Excited
    "😴",  # Sleepy
    "🤯",  # Mind‑blown
    "🥳",  # Celebratory
]


def _deterministic_index(date: datetime.date) -> int:
    """Return a reproducible index into ``MOOD_EMOJIS`` based on *date*.

    The algorithm is deliberately simple: hash the ISO‑formatted date string,
    take the absolute value, and modulo the length of ``MOOD_EMOJIS``.
    """
    # ``hash`` is salted per‑process, so we use a stable hash function.
    # ``int.from_bytes`` on the UTF‑8 bytes gives a deterministic integer.
    date_bytes = date.isoformat().encode("utf-8")
    deterministic_int = int.from_bytes(date_bytes, "big")
    return deterministic_int % len(MOOD_EMOJIS)


def get_mood_emoji(date: datetime.date) -> str:
    """Return the mood emoji for *date*.

    Parameters
    ----------
    date: datetime.date
        The calendar date for which to compute the mood.

    Returns
    -------
    str
        A single emoji character.
    """
    index = _deterministic_index(date)
    return MOOD_EMOJIS[index]


def _parse_cli_arg(arg: str) -> datetime.date:
    """Parse a CLI argument into a ``datetime.date``.

    Accepts ISO‑8601 dates (YYYY‑MM‑DD). If parsing fails, the function raises
    ``ValueError`` with a helpful message.
    """
    try:
        return datetime.date.fromisoformat(arg)
    except Exception as exc:
        raise ValueError(f"Invalid date format '{arg}'. Expected YYYY-MM-DD.") from exc


def main() -> None:
    """CLI entry point.

    * No arguments → use today's date.
    * One argument → treat it as an ISO‑8601 date.
    """
    if len(sys.argv) == 1:
        target_date = datetime.date.today()
    elif len(sys.argv) == 2:
        target_date = _parse_cli_arg(sys.argv[1])
    else:
        print("Usage: python -m nightly_emoji_mood_tracker [YYYY-MM-DD]", file=sys.stderr)
        sys.exit(1)

    emoji = get_mood_emoji(target_date)
    print(f"{target_date.isoformat()}: {emoji}")


if __name__ == "__main__":
    main()
