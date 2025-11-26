import argparse
import random
from typing import List

EMOJIS: List[str] = [
    "😀", "🚀", "🌟", "🔥", "💧", "🍀", "🎉", "🧩", "📚", "🛸",
]


def _pick_emoji() -> str:
    """Return a random emoji from the pool.

    The function is isolated so it can be easily mocked in tests.
    """
    return random.choice(EMOJIS)


def annotate(text: str, seed: int | None = None) -> str:
    """Append a random emoji to each word in *text*.

    Args:
        text: Input sentence.
        seed: Optional seed for ``random`` to make the output deterministic.

    Returns:
        The annotated string.
    """
    if seed is not None:
        random.seed(seed)
    words = text.split()
    annotated_words = [f"{word} {_pick_emoji()}" for word in words]
    return " ".join(annotated_words)


def _build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Annotate each word with a random emoji.")
    parser.add_argument("text", help="The text to annotate.")
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional seed for deterministic output.",
    )
    return parser


def main() -> None:
    parser = _build_cli()
    args = parser.parse_args()
    result = annotate(args.text, seed=args.seed)
    print(result)


if __name__ == "__main__":
    main()
