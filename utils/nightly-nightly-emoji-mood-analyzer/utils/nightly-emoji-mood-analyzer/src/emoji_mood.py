import argparse
from collections import Counter
from typing import Dict, List

# Define simple sentiment groups for emojis
POSITIVE_EMOJIS: List[str] = [
    "😀", "😃", "😄", "😁", "😆", "😊", "😇", "🥰", "😍", "🤩", "👍", "🤗",
]
NEGATIVE_EMOJIS: List[str] = [
    "☹️", "🙁", "😞", "😔", "😟", "😢", "😭", "😩", "👎", "😡", "🤬",
]

def _count_emojis(text: str) -> Dict[str, int]:
    """Count occurrences of known positive and negative emojis in *text*.

    Returns a dictionary with keys ``"positive"`` and ``"negative"``.
    """
    counter = Counter()
    for ch in text:
        if ch in POSITIVE_EMOJIS:
            counter["positive"] += 1
        elif ch in NEGATIVE_EMOJIS:
            counter["negative"] += 1
    return {"positive": counter["positive"], "negative": counter["negative"]}


def analyze_mood(text: str) -> str:
    """Return ``"happy"``, ``"sad"`` or ``"neutral"`` based on emoji sentiment.

    The algorithm is deliberately simple:
    - If positive count > negative count → ``"happy"``
    - If negative count > positive count → ``"sad"``
    - Otherwise → ``"neutral"``
    """
    counts = _count_emojis(text)
    if counts["positive"] > counts["negative"]:
        return "happy"
    if counts["negative"] > counts["positive"]:
        return "sad"
    return "neutral"


def _build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze the overall mood of a text based on emojis."
    )
    parser.add_argument(
        "text",
        nargs="?",
        default=None,
        help="The text to analyze. If omitted, reads from STDIN.",
    )
    return parser


def main() -> None:
    parser = _build_cli()
    args = parser.parse_args()
    if args.text is None:
        # Read from stdin when no argument is supplied
        import sys
        text = sys.stdin.read()
    else:
        text = args.text
    mood = analyze_mood(text)
    print(mood)


if __name__ == "__main__":
    main()
