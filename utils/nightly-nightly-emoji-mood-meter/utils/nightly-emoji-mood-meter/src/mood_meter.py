import argparse
import re
from typing import Dict, List

# Simple keyword‑to‑emoji mapping. The order matters – first match wins.
_MOOD_MAP: List[Dict[str, str]] = [
    {"keywords": ["love", "awesome", "great", "fantastic", "good", "happy", "joy", "excellent"], "emoji": "😄"},
    {"keywords": ["sad", "unhappy", "bad", "terrible", "hate", "angry", "mad", "frustrated"], "emoji": "😞"},
    {"keywords": ["error", "failed", "exception", "bug", "crash", "broken"], "emoji": "💥"},
    {"keywords": ["warning", "caution", "slow", "delay"], "emoji": "⚠️"},
    {"keywords": ["question", "?", "maybe", "uncertain"], "emoji": "🤔"},
]

_DEFAULT_EMOJI = "🤖"


def _normalize(text: str) -> str:
    """Lower‑case and strip punctuation for simple matching."""
    return re.sub(r"[\W_]+", " ", text.lower()).strip()


def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the mood of *text*.

    The function performs a case‑insensitive keyword search. The first matching
    keyword set determines the emoji. If no keywords are found, a default
    robot emoji is returned.
    """
    normalized = _normalize(text)
    for entry in _MOOD_MAP:
        for kw in entry["keywords"]:
            if kw in normalized:
                return entry["emoji"]
    return _DEFAULT_EMOJI


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Infer mood emoji from a short text.")
    parser.add_argument("text", nargs="+", help="Text to analyse (will be joined with spaces)")
    args = parser.parse_args()
    input_text = " ".join(args.text)
    print(get_mood_emoji(input_text))


if __name__ == "__main__":
    _cli()
