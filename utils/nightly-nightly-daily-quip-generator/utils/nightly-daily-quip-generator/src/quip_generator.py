'''\
quip_generator.py - Provides a deterministic daily quip.
\'''

import datetime
from typing import List

# A small collection of whimsical programming quotes.
QUIPS: List[str] = [
    "Keep calm and code on.",
    "Debugging: where you become a detective in a world of zeros and ones.",
    "When in doubt, add a comment.",
    "Version control: because you can't remember everything.",
    "Commit early, commit often, and never commit on a Friday night.",
    "If it works, ship it. If it doesn't, blame the compiler.",
    "Code is like humor. When you have to explain it, it's bad.",
    "There are only two hard things in computer science: cache invalidation, naming things, and off‑by‑one errors.",
    "Talk is cheap. Show me the code.",
    "First, solve the problem. Then, write the code."
]


def get_daily_quip(date: datetime.date | None = None) -> str:
    """Return a deterministic quip for the given date (UTC).

    If *date* is ``None`` the current local date is used.
    The selection algorithm is deterministic and offline:
    ``index = date.toordinal() % len(QUIPS)``.
    """
    if date is None:
        date = datetime.date.today()
    index = date.toordinal() % len(QUIPS)
    return QUIPS[index]


def main() -> None:
    """CLI entry point – prints today's quip to stdout."""
    print(get_daily_quip())


if __name__ == "__main__":
    main()
