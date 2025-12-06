"""Emoji Quote of the Day utility.

Provides a function to retrieve a random emoji‑quote pair and a CLI entry point.
"""

import random
from typing import Tuple

_QUOTES = [
    "Keep your face always toward the sunshine—and shadows will fall behind you.",
    "The only way to do great work is to love what you do.",
    "Life is what happens when you're busy making other plans.",
]

_EMOJIS = ["🌞", "🚀", "💡", "🌱", "🎉"]


def get_emoji_quote() -> Tuple[str, str]:
    """Return a random (emoji, quote) pair.

    Returns:
        Tuple[str, str]: Selected emoji and quote.
    """
    emoji = random.choice(_EMOJIS)
    quote = random.choice(_QUOTES)
    return emoji, quote


def main() -> None:
    """CLI entry point: prints the emoji‑quote pair."""
    emoji, quote = get_emoji_quote()
    print(f"{emoji} {quote}")


if __name__ == "__main__":
    main()
