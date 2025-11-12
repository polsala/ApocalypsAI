"""
emoji_id.py – Generate emoji‑based identifiers.

Provides:
- ``generate_id(length=4, seed=None)`` → ``str``
- ``main()`` – CLI entry point.
"""

import argparse
import random
from typing import List

# A modest palette of emojis that render well in most terminals.
_EMOJIS: List[str] = [
    "😀", "😂", "🥰", "🤔", "🙃", "😎", "🤖", "🐱", "🐶", "🦊",
    "🐸", "🐵", "🦁", "🚀", "🌟", "🔥", "💧", "🍎", "🍕", "⚡",
    "🎈", "🎉", "📚", "🔑", "🧩",
]


def _choose_emojis(length: int, rnd: random.Random) -> List[str]:
    """Return a list of *length* emojis chosen via *rnd*.

    This helper is isolated for easier testing/mocking.
    """
    return [rnd.choice(_EMOJIS) for _ in range(length)]


def generate_id(length: int = 4, seed: int | None = None) -> str:
    """Generate a string of ``length`` emojis.

    Args:
        length: Number of emojis in the identifier (must be > 0).
        seed: Optional seed for deterministic output.

    Returns:
        A concatenated string of emojis.

    Raises:
        ValueError: If ``length`` is not a positive integer.
    """
    if not isinstance(length, int) or length <= 0:
        raise ValueError("length must be a positive integer")
    rnd = random.Random(seed)
    emojis = _choose_emojis(length, rnd)
    return "".join(emojis)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a short emoji identifier.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen_parser = subparsers.add_parser("generate", help="Generate an emoji ID")
    gen_parser.add_argument(
        "--length",
        type=int,
        default=4,
        help="Number of emojis (default: 4)",
    )
    gen_parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    if args.command == "generate":
        try:
            eid = generate_id(length=args.length, seed=args.seed)
            print(eid)
        except ValueError as exc:
            parser.error(str(exc))


if __name__ == "__main__":
    main()
