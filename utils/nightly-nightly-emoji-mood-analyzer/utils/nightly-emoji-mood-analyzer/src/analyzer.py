import argparse
import sys
from typing import Tuple

POSITIVE_WORDS = {
    "love",
    "great",
    "awesome",
    "fantastic",
    "good",
    "happy",
    "joy",
    "excellent",
    "wonderful",
    "amazing",
}

NEGATIVE_WORDS = {
    "hate",
    "bad",
    "terrible",
    "sad",
    "angry",
    "awful",
    "worst",
    "pain",
    "disappoint",
    "poor",
}

EMOJI_MAP = {
    "positive": "😊",
    "negative": "😞",
    "neutral": "😐",
}

def _score_text(text: str) -> int:
    """Return a simple sentiment score based on word occurrences.

    Positive words add +1, negative words subtract -1. The function is case‑insensitive
    and ignores punctuation.
    """
    # Mock rationale: simple deterministic scoring, no external libs.
    import re

    words = re.findall(r"\b\w+\b", text.lower())
    score = 0
    for w in words:
        if w in POSITIVE_WORDS:
            score += 1
        elif w in NEGATIVE_WORDS:
            score -= 1
    return score

def analyze_mood(text: str) -> Tuple[str, str]:
    """Return a tuple of (sentiment, emoji) for *text*.

    Sentiment is one of ``positive``, ``negative`` or ``neutral``.
    """
    score = _score_text(text)
    if score > 0:
        sentiment = "positive"
    elif score < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return sentiment, EMOJI_MAP[sentiment]

def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Analyze the mood of a short piece of text and return an emoji."
    )
    parser.add_argument("text", help="The text to analyze")
    args = parser.parse_args(argv)
    sentiment, emoji = analyze_mood(args.text)
    print(f"{sentiment} {emoji}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
