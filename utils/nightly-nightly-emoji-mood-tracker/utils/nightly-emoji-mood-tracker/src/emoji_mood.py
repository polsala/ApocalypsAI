#!/usr/bin/env python3
"""
emoji_mood.py

Utility to translate a numeric mood score (-10 to 10) into a representative emoji.
"""

import argparse
import sys

# Mapping thresholds
_SCORE_EMOJI_MAP = [
    (-10, -7, "😭"),   # Very sad
    (-6, -3, "😞"),    # Sad
    (-2, 0, "😐"),     # Neutral
    (1, 3, "🙂"),      # Slightly happy
    (4, 7, "😄"),      # Happy
    (8, 10, "🤩"),    # Ecstatic
]


def score_to_emoji(score: int) -> str:
    """Convert a mood score to an emoji.

    Parameters
    ----------
    score: int
        Integer between -10 and 10 inclusive.

    Returns
    -------
    str
        Emoji representing the mood.

    Raises
    ------
    ValueError
        If score is outside the allowed range.
    TypeError
        If score is not an integer.
    """
    if not isinstance(score, int):
        raise TypeError("Score must be an integer.")
    if score < -10 or score > 10:
        raise ValueError("Score must be between -10 and 10 inclusive.")
    for low, high, emoji in _SCORE_EMOJI_MAP:
        if low <= score <= high:
            return emoji
    # Should never happen because ranges cover all values
    raise RuntimeError("Unmapped score.")


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Translate a numeric mood score (-10..10) into an emoji."
    )
    parser.add_argument(
        "score",
        type=int,
        help="Mood score integer between -10 (worst) and 10 (best).",
    )
    return parser.parse_args(argv)


def main():
    args = _parse_args()
    try:
        emoji = score_to_emoji(args.score)
        print(emoji)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
