import argparse
import random
from typing import List, Optional

# A curated list of emojis that render well in most terminals.
_EMOJIS: List[str] = [
    "😀", "😂", "🥳", "🤖", "🌟", "🚀", "🍕", "🐍", "🧩", "📚",
    "🎉", "💡", "🛠️", "⚡", "🌈", "🧠", "🕹️", "🏆", "🔧", "🧪",
]


def get_random_emoji(seed: Optional[int] = None) -> str:
    """Return a random emoji.

    Args:
        seed: Optional integer to seed the RNG for deterministic output.
    Returns:
        A single emoji string.
    """
    rng = random.Random(seed) if seed is not None else random
    return rng.choice(_EMOJIS)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random emoji.")
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional seed for deterministic output (useful for testing).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    emoji = get_random_emoji(seed=args.seed)
    print(emoji)


if __name__ == "__main__":
    main()
