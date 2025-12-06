"""mood_art.py

Utility to map a mood keyword to a whimsical ASCII‑art representation.

Provides:
- `MOOD_ART` dictionary (public) for easy extension.
- `get_art(mood: str) -> str` – core function.
- Simple CLI for interactive use.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict

# Pre‑defined ASCII art for each mood.
MOOD_ART: Dict[str, str] = {
    "happy": r"""
      .-"""-.
    .'  _   _ '.
   /   (o) (o)  \
  |     ___     |
  \   (_____ ) /
   '.  \___/ .'
     '-.__.-'
""",
    "sad": r"""
      .-"""-.
    .'  _   _ '.
   /   (o) (o)  \
  |     ___     |
  \   (_____ ) /
   '.  \___/ .'
     '-.__.-'
   (  .   .  )
    \  ---  /
     '-----'
""",
    "angry": r"""
      .-"""-.
    .'  >   < '.
   /   (o) (o)  \
  |     ___     |
  \   (_____ ) /
   '.  \___/ .'
     '-.__.-'
""",
    "surprised": r"""
      .-"""-.
    .'  O   O '.
   /    ___    \
  |    (___)   |
  \            /
   '.  \_/  .'
     '-.__.-'
""",
    "neutral": r"""
      .-"""-.
    .'  -   - '.
   /    ___    \
  |    (___)   |
  \            /
   '.  \_/  .'
     '-.__.-'
""",
    "default": r"""
      .-"""-.
    .'  .   . '.
   /    ___    \
  |    (___)   |
  \            /
   '.  \_/  .'
     '-.__.-'
""",
}


def get_art(mood: str) -> str:
    """Return the ASCII art for *mood*.

    The lookup is case‑insensitive. If the mood is not recognised, the
    ``default`` art is returned.
    """
    key = mood.lower().strip()
    return MOOD_ART.get(key, MOOD_ART["default"])


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print ASCII art for a given mood.")
    parser.add_argument(
        "mood",
        nargs="?",
        default="neutral",
        help="Mood keyword (happy, sad, angry, surprised, neutral).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    art = get_art(args.mood)
    print(art)
    return 0


if __name__ == "__main__":
    sys.exit(main())
