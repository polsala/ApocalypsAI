import sys
from pathlib import Path

POSITIVE_WORDS = {
    "happy",
    "joy",
    "love",
    "awesome",
    "great",
    "fantastic",
    "good",
    "wonderful",
    "excellent",
    "sunny",
}

NEGATIVE_WORDS = {
    "sad",
    "angry",
    "bad",
    "terrible",
    "horrible",
    "pain",
    "hate",
    "depressed",
    "rainy",
    "worst",
}

EMOJI_POSITIVE = "😄"
EMOJI_NEGATIVE = "😞"
EMOJI_NEUTRAL = "🤔"

def _tokenize(text: str) -> list[str]:
    """Very simple tokenizer: lower‑case and split on whitespace and punctuation."""
    import re
    return re.findall(r"\b\w+\b", text.lower())

def mood_emoji(text: str) -> str:
    """Return an emoji representing the overall mood of *text*.

    The algorithm counts occurrences of words from ``POSITIVE_WORDS`` and ``NEGATIVE_WORDS``.
    If positives > negatives → positive emoji, if negatives > positives → negative emoji,
    otherwise neutral.
    """
    tokens = _tokenize(text)
    pos = sum(tok in POSITIVE_WORDS for tok in tokens)
    neg = sum(tok in NEGATIVE_WORDS for tok in tokens)
    if pos > neg:
        return EMOJI_POSITIVE
    if neg > pos:
        return EMOJI_NEGATIVE
    return EMOJI_NEUTRAL

def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: python -m nightly_emoji_mood_meter \"Your text\"")
        return 2
    text = " ".join(argv)
    print(mood_emoji(text))
    return 0

if __name__ == "__main__":
    sys.exit(main())
