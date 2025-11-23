"""
Utility to map a numeric mood score (1‑5) to a corresponding emoji.
"""

from typing import Literal

MoodScore = Literal[1, 2, 3, 4, 5]

_EMOJI_MAP = {
    1: "😞",  # Very sad
    2: "☹️",  # Sad
    3: "😐",  # Neutral
    4: "🙂",  # Happy
    5: "😁",  # Very happy
}


def get_mood_emoji(score: MoodScore) -> str:
    """Return the emoji representing the given mood score.

    Args:
        score: An integer from 1 (worst) to 5 (best).

    Returns:
        A string containing a single emoji.

    Raises:
        ValueError: If ``score`` is not in the range 1‑5.
    """
    if score not in _EMOJI_MAP:
        raise ValueError(f"Score must be between 1 and 5 inclusive, got {score}")
    return _EMOJI_MAP[score]


def main() -> None:
    """Simple CLI: ``python -m src.mood <score>``.
    """
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Convert a mood score (1‑5) to an emoji.")
    parser.add_argument("score", type=int, help="Mood score between 1 and 5")
    args = parser.parse_args()

    try:
        emoji = get_mood_emoji(args.score)
        print(emoji)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
