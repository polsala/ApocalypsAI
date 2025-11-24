import argparse
import sys
from typing import List

# Simple keyword → emoji mapping (order matters: first match wins)
MOOD_MAP: List[tuple[str, str]] = [
    ("happy|joy|wonderful|great|fantastic|awesome|glad|delighted|smile", "😄"),
    ("sad|unhappy|down|depressed|gloom|miserable|cry|tears", "😞"),
    ("angry|mad|furious|irate|annoyed|hate", "😠"),
    ("love|loving|adore|cherish|heart", "❤️"),
    ("surprised|shocked|amazed|wow|astonished", "😲"),
    ("fear|scared|terrified|afraid|panic", "😨"),
]

DEFAULT_EMOJI = "😐"


def detect_mood(text: str) -> str:
    """Return an emoji representing the mood of *text*.

    The function lower‑cases the input and checks each regular‑expression pattern
    in ``MOOD_MAP``. The first matching pattern determines the emoji. If none match,
    a neutral face is returned.
    """
    import re

    lowered = text.lower()
    for pattern, emoji in MOOD_MAP:
        if re.search(pattern, lowered):
            return emoji
    return DEFAULT_EMOJI


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Detect mood from a short text and output a corresponding emoji."
    )
    parser.add_argument(
        "--text",
        type=str,
        help="Text to analyze. If omitted, reads from STDIN.",
    )
    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.text:
        input_text = args.text
    else:
        # Read from stdin; strip trailing newlines for clean output
        input_text = sys.stdin.read().strip()

    emoji = detect_mood(input_text)
    print(emoji)
    return 0


if __name__ == "__main__":
    sys.exit(main())
