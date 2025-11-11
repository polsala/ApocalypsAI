import sys
import datetime
from typing import Tuple

# Mapping of weekday (0=Monday) to emoji and description
_WEEKDAY_MAP: dict[int, Tuple[str, str]] = {
    0: ("🟦", "Start of the week!"),
    1: ("🟪", "Mid‑week magic!"),
    2: ("🟩", "Hump day vibes!"),
    3: ("🟧", "Almost there!"),
    4: ("🟥", "Weekend is near!"),
    5: ("🟨", "Saturday sunshine!"),
    6: ("⬜️", "Sunday serenity.")
}


def get_emoji_for_date(d: datetime.date) -> str:
    """Return the emoji representing the weekday of *d*.

    Args:
        d: A ``datetime.date`` instance.
    Returns:
        A single‑character emoji string.
    """
    emoji, _ = _WEEKDAY_MAP[d.weekday()]
    return emoji


def get_description_for_date(d: datetime.date) -> str:
    """Return a short description for the weekday of *d*.

    Args:
        d: A ``datetime.date`` instance.
    Returns:
        Human‑readable description.
    """
    _, desc = _WEEKDAY_MAP[d.weekday()]
    return desc


def format_for_cli(d: datetime.date) -> str:
    """Combine emoji and description for command‑line output."""
    return f"{get_emoji_for_date(d)} – {get_description_for_date(d)}"


def _parse_date(arg: str) -> datetime.date:
    """Parse a ``YYYY-MM-DD`` string into ``datetime.date``.

    # Mock rationale: Simple parsing without external libs; raises ValueError on bad format.
    """
    try:
        year, month, day = map(int, arg.split("-"))
        return datetime.date(year, month, day)
    except Exception as e:
        raise ValueError(f"Invalid date format '{arg}'. Expected YYYY-MM-DD.") from e


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Usage: ``python -m src.calendar <YYYY-MM-DD>``
    Returns exit code 0 on success, 1 on error.
    """
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python -m src.calendar <YYYY-MM-DD>")
        return 1
    try:
        d = _parse_date(argv[0])
        print(format_for_cli(d))
        return 0
    except ValueError as ve:
        print(str(ve), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
