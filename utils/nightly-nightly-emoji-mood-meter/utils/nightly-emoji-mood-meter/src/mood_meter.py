import argparse
import sys
from typing import List

# Keyword groups mapped to emojis
_EMOJI_MAP = {
    "happy": ["happy", "joy", "glad", "delighted", "cheerful", "sunny", "great", "fantastic"],
    "sad": ["sad", "unhappy", "down", "depressed", "gloomy", "bad", "terrible"],
    "angry": ["angry", "mad", "furious", "irate", "annoyed", "hate"],
    "love": ["love", "loving", "adore", "cherish", "heart", "❤️"],
    "surprise": ["surprise", "shocked", "amazed", "wow", "astonished"],
}

_EMOJI_OUTPUT = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "love": "❤️",
    "surprise": "😲",
    "default": "😐",
}

def _tokenize(text: str) -> List[str]:
    """Very simple tokenizer: lower‑case and split on whitespace and punctuation."""
    import re
    return re.findall(r"[a-zA-Z]+", text.lower())

def get_mood_emoji(text: str) -> str:
    """Return an emoji representing the mood of *text*.

    The function checks each keyword group in the order defined in ``_EMOJI_MAP``.
    The first matching group wins. If no keywords match, a neutral emoji is returned.
    """
    tokens = set(_tokenize(text))
    for mood, keywords in _EMOJI_MAP.items():
        if any(keyword in tokens for keyword in keywords):
            return _EMOJI_OUTPUT[mood]
    return _EMOJI_OUTPUT["default"]

def _cli() -> None:
    parser = argparse.ArgumentParser(description="Map a short text to a mood emoji.")
    parser.add_argument("text", nargs="+", help="Text to analyse (will be joined with spaces)")
    args = parser.parse_args()
    input_text = " ".join(args.text)
    emoji = get_mood_emoji(input_text)
    print(emoji)

if __name__ == "__main__":
    # When executed as a module: python -m src.mood_meter "I love this!"
    _cli()
