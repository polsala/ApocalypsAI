import argparse
import sys
from typing import List, Dict

# Mapping of emojis to simple mood scores.
EMOJI_SCORES: Dict[str, int] = {
    "😀": 1,
    "😃": 1,
    "😄": 1,
    "😁": 1,
    "😂": 1,
    "🤣": 1,
    "😊": 1,
    "😍": 1,
    "🥰": 1,
    "🎉": 1,
    "👍": 1,
    "❤️": 1,
    "😢": -1,
    "😭": -1,
    "😡": -1,
    "😠": -1,
    "👎": -1,
    "💔": -1,
    "💩": -1,
}


def extract_emojis(text: str) -> List[str]:
    """Return a list of emojis from *text* that are present in ``EMOJI_SCORES``.

    This simple implementation iterates over each character; because the
    supported emojis are single Unicode code points, this works without external
    libraries.
    """
    return [ch for ch in text if ch in EMOJI_SCORES]


def mood_score(emojis: List[str]) -> int:
    """Calculate the total mood score for a list of emojis."""
    return sum(EMOJI_SCORES.get(e, 0) for e in emojis)


def mood_summary(score: int) -> str:
    """Translate a numeric *score* into a human‑readable mood description.

    The thresholds are deliberately simple:
    * score >= 3   → "Very Happy"
    * score 1‑2    → "Happy"
    * score 0      → "Neutral"
    * score -1‑-2  → "Sad"
    * score <= -3  → "Very Sad"
    """
    if score >= 3:
        return "Very Happy"
    if score >= 1:
        return "Happy"
    if score == 0:
        return "Neutral"
    if score >= -2:
        return "Sad"
    return "Very Sad"


def analyze_text(text: str) -> str:
    """Convenience wrapper that returns the mood summary for *text*."""
    emojis = extract_emojis(text)
    score = mood_score(emojis)
    return mood_summary(score)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Analyze emojis in a text and report an aggregated mood."
    )
    parser.add_argument(
        "--text",
        type=str,
        help="Text to analyze. If omitted, reads from STDIN.",
    )
    args = parser.parse_args(argv)

    if args.text is not None:
        input_text = args.text
    else:
        input_text = sys.stdin.read()

    summary = analyze_text(input_text)
    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
