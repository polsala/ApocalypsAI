import argparse
import sys
import random
from typing import Optional

EMOJIS = [
    "🚀", "✨", "🐛", "🔧", "📦", "✅", "⚡", "🧹", "🛠️", "🎉",
    "💡", "🔒", "🧪", "📈", "🗑️", "🧩", "🔁", "🧭", "🪄", "🤖",
]

MAX_LENGTH = 72


def _pick_emoji(rng: random.Random) -> str:
    """Select a random emoji using the provided Random instance."""
    return rng.choice(EMOJIS)


def enhance_message(message: str, seed: Optional[int] = None) -> str:
    """Return *message* with a random emoji appended.

    The final string will never exceed ``MAX_LENGTH`` characters. If the original
    *message* is too long, it is truncated to make room for a space and the emoji.

    Parameters
    ----------
    message:
        The original commit message.
    seed:
        Optional seed for deterministic emoji selection.
    """
    rng = random.Random(seed)
    emoji = _pick_emoji(rng)
    # Reserve space for a single space and the emoji
    allowance = MAX_LENGTH - len(emoji) - 1
    trimmed = message[:allowance]
    return f"{trimmed} {emoji}".strip()


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append a random emoji to a git commit message, respecting the 72‑char limit."
    )
    parser.add_argument(
        "--message",
        type=str,
        help="Commit message. If omitted, reads from stdin.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional seed for deterministic emoji selection.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv or sys.argv[1:])
    if args.message is not None:
        raw_msg = args.message
    else:
        raw_msg = sys.stdin.read().strip()
    enhanced = enhance_message(raw_msg, seed=args.seed)
    print(enhanced)


if __name__ == "__main__":
    main()
