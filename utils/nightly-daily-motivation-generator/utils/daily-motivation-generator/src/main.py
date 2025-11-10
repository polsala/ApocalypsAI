"""daily_motivation_generator – core implementation

Provides a deterministic quote for a given date and a tiny CLI.
"""

from __future__ import annotations

import os
import sys
from datetime import date
from typing import List, Tuple

# ---------------------------------------------------------------------------
# Quote database – whimsical but useful
# ---------------------------------------------------------------------------
QUOTES: List[Tuple[str, str]] = [
    ("The only limit to our realization of tomorrow is our doubts of today.", "Franklin D. Roosevelt"),
    ("Do not wait to strike till the iron is hot; but make it hot by striking.", "William Butler Yeats"),
    ("What you get by achieving your goals is not as important as what you become by achieving your goals.", "Zig Ziglar"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("Dream big and dare to fail.", "Norman Vaughan"),
    ("You miss 100% of the shots you don’t take.", "Wayne Gretzky"),
    ("The best way to predict the future is to invent it.", "Alan Kay"),
    ("Keep your face always toward the sunshine—and shadows will fall behind you.", "Walt Whitman"),
]


def _deterministic_index(target_date: date) -> int:
    """Return a stable index into ``QUOTES`` for *target_date*.

    The algorithm uses Python's built‑in ``hash`` on the ISO string of the date.
    ``hash`` is deterministic within a single interpreter session (the hash seed
    is fixed for strings). This yields reproducible results for tests.
    """
    iso = target_date.isoformat()
    return hash(iso) % len(QUOTES)


def get_quote_for_date(target_date: date) -> str:
    """Return a formatted quote for *target_date*.

    Example output:
        "The only limit to our realization of tomorrow is our doubts of today." – Franklin D. Roosevelt
    """
    idx = _deterministic_index(target_date)
    text, author = QUOTES[idx]
    return f'"{text}" – {author}'


def _print_banner() -> None:
    banner = r"""
     __  __       _        _   _                 _ 
    |  \/  | __ _| |_ __ _| |_(_) ___  _ __  ___| |
    | |\/| |/ _` | __/ _` | __| |/ _ \| '_ \/ __| |
    | |  | | (_| | || (_| | |_| | (_) | | | \__ \_|
    |_|  |_|\__,_|\__\__,_|\__|_|\___/|_| |_|___(_)
    """
    print(banner)


def main() -> None:
    today = date.today()
    quote = get_quote_for_date(today)
    # Optional banner controlled by env var for extra whimsy
    if os.getenv("MOTIVATION_BANNER"):
        _print_banner()
    print(f"🌞 Good morning! {quote}")


if __name__ == "__main__":
    # When executed as a module: ``python -m daily_motivation_generator``
    # Adjust sys.path so that ``src`` is importable as a package name.
    # This mirrors the layout used by other utils in the repo.
    current_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    # Export a package name for imports (optional, not required for CLI)
    main()
