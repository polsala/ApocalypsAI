import argparse
import sys
from typing import List

# Keyword groups for each mood
MOOD_KEYWORDS = {
    "happy": ["happy", "joy", "love", "great", "awesome", "fantastic", "good", "wonderful"],
    "sad": ["sad", "bad", "terrible", "upset", "depressed", "unhappy", "down"],
    "angry": ["angry", "mad", "furious", "irate", "annoyed", "hate"],
}

MOOD_EMOJIS = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "neutral": "🤔",
}

def _match_mood(tokens: List[str]) -> str:
    """Return the first mood whose keywords appear in *tokens*.

    The order of checking is happy → sad → angry. If none match, returns "neutral".
    """
    for mood, keywords in MOOD_KEYWORDS.items():
        if any(k in tokens for k in keywords):
            return mood
    return "neutral"

def analyze_mood(text: str) -> str:
    """Return an emoji representing the mood of *text*.

    The algorithm is deliberately simple and deterministic:
    1. Lower‑case the input.
    2. Split on whitespace.
    3. Look for the first matching keyword group.
    4. Return the corresponding emoji.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    tokens = text.lower().split()
    mood = _match_mood(tokens)
    return MOOD_EMOJIS[mood]

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Map a short text to a mood emoji.")
    parser.add_argument(
        "text",
        nargs="?",
        help="The text to analyze. If omitted, reads from STDIN.",
    )
    return parser

def main(argv: List[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.text is not None:
        input_text = args.text
    else:
        # Read from stdin; strip trailing newlines
        input_text = sys.stdin.read().strip()
    emoji = analyze_mood(input_text)
    print(emoji)
    return 0

if __name__ == "__main__":
    sys.exit(main())
