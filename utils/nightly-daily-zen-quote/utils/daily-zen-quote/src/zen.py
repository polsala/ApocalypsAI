import argparse
import random
import sys
from typing import Tuple, List

# ---------------------------------------------------------------------------
# Internal quote database (author, quote)
# ---------------------------------------------------------------------------
QUOTES: List[Tuple[str, str]] = [
    ("The journey of a thousand miles begins with one step.", "Lao Tzu"),
    ("When the mind is still, the universe surrenders.", "Lao Tzu"),
    ("Simplicity is the ultimate sophistication.", "Leonardo da Vinci"),
    ("Nature does not hurry, yet everything is accomplished.", "Lao Tzu"),
]


def _seed_random(seed: int | None) -> None:
    """Seed the global random generator if a seed is provided.

    The function isolates the seeding logic so tests can call the public
    helpers without worrying about side‑effects.
    """
    if seed is not None:
        random.seed(seed)


def get_random_quote(seed: int | None = None) -> Tuple[str, str]:
    """Return a random ``(quote, author)`` pair.

    Parameters
    ----------
    seed:
        Optional integer seed for deterministic output.  When ``None`` the
        global random state is used.
    """
    _seed_random(seed)
    quote, author = random.choice(QUOTES)
    return quote, author


def filter_by_max_length(max_len: int, seed: int | None = None) -> Tuple[str, str]:
    """Return a random quote whose *text* length does not exceed ``max_len``.

    Raises
    ------
    ValueError
        If no quote satisfies the length constraint.
    """
    if max_len < 0:
        raise ValueError("max_len must be non‑negative")
    _seed_random(seed)
    filtered = [(q, a) for q, a in QUOTES if len(q) <= max_len]
    if not filtered:
        raise ValueError("No quotes fit the length constraint")
    return random.choice(filtered)


def _format_output(quote: str, author: str) -> str:
    return f'"{quote}" — {author}'


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a random Zen quote")
    parser.add_argument(
        "--max-length",
        type=int,
        help="Maximum number of characters for the quote text",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Seed for deterministic output (useful for scripts or testing)",
    )
    args = parser.parse_args()

    try:
        if args.max_length is not None:
            quote, author = filter_by_max_length(args.max_length, args.seed)
        else:
            quote, author = get_random_quote(args.seed)
        print(_format_output(quote, author))
    except Exception as exc:  # pragma: no cover – defensive, not exercised in tests
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
