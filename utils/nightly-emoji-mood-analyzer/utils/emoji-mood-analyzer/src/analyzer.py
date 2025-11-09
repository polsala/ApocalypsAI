import argparse
import re
from typing import List

# Define simple keyword lists for each mood
MOOD_KEYWORDS = {
    "happy": ["happy", "joy", "love", "great", "wonderful", "fantastic"],
    "sad": ["sad", "sorrow", "upset", "depressed", "down"],
    "angry": ["angry", "mad", "furious", "rage", "upset"],
}

MOOD_EMOJIS = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "neutral": "🤔",
}

def _tokenize(text: str) -> List[str]:
    """Return a list of lowercase words stripped of punctuation."""
    # Simple word extraction; keep apostrophes inside words (e.g., "don't")
    return re.findall(r"[A-Za-z']+", text.lower())

def analyze_mood(text: str) -> str:
    """Return an emoji representing the dominant mood in *text*.

    The function checks for keywords in the order: happy → sad → angry.
    The first matching mood is returned. If no keywords are found, a neutral
    emoji is returned.
    """
    tokens = set(_tokenize(text))
    # Priority order
    for mood in ["happy", "sad", "angry"]:
        if any(keyword in tokens for keyword in MOOD_KEYWORDS[mood]):
            return MOOD_EMOJIS[mood]
    return MOOD_EMOJIS["neutral"]

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze a line of text and output a mood emoji.")
    parser.add_argument("text", type=str, help="The text to analyze.")
    return parser.parse_args()

def main() -> None:
    args = _parse_args()
    emoji = analyze_mood(args.text)
    print(emoji)

if __name__ == "__main__":
    main()
