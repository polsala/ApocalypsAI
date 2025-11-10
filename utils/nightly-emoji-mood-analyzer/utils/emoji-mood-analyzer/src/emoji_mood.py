import argparse
import re
from typing import List

# Simple keyword‑based sentiment dictionaries
POSITIVE_WORDS: List[str] = [
    "love",
    "happy",
    "joy",
    "awesome",
    "great",
    "fantastic",
    "good",
    "wonderful",
    "excellent",
    "delight",
]

NEGATIVE_WORDS: List[str] = [
    "hate",
    "sad",
    "bad",
    "terrible",
    "awful",
    "horrible",
    "worst",
    "pain",
    "angry",
    "depress",
]

def _tokenize(text: str) -> List[str]:
    """Return a list of lowercase word tokens from *text*.

    Non‑alphabetic characters are stripped; this keeps the function
    deterministic and offline.
    """
    # Replace non‑letters with spaces, then split
    cleaned = re.sub(r"[^a-zA-Z]", " ", text)
    return [token.lower() for token in cleaned.split() if token]

def analyze_mood(text: str) -> str:
    """Return an emoji representing the overall mood of *text*.

    The algorithm counts occurrences of words from the positive and negative
    lists. The resulting score determines the emoji:

    * score > 0 → 😊 (happy)
    * score < 0 → 😞 (sad)
    * score == 0 → 😐 (neutral)
    """
    tokens = _tokenize(text)
    pos_count = sum(token in POSITIVE_WORDS for token in tokens)
    neg_count = sum(token in NEGATIVE_WORDS for token in tokens)
    score = pos_count - neg_count

    if score > 0:
        return "😊"
    elif score < 0:
        return "😞"
    else:
        return "😐"

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Return an emoji representing the mood of the supplied text."
    )
    parser.add_argument("text", help="Text to analyze for mood")
    args = parser.parse_args()
    emoji = analyze_mood(args.text)
    print(emoji)

if __name__ == "__main__":
    main()
