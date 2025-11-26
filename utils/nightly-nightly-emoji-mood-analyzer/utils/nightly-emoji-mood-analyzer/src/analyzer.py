import argparse
import re
import sys

# Simple handcrafted sentiment lexicon – deterministic and offline.
POSITIVE_WORDS = {
    "love",
    "happy",
    "joy",
    "wonderful",
    "great",
    "awesome",
    "fantastic",
    "good",
    "sunny",
    "delight",
    "pleased",
    "excited",
}

NEGATIVE_WORDS = {
    "hate",
    "sad",
    "angry",
    "terrible",
    "bad",
    "awful",
    "worst",
    "rainy",
    "depressed",
    "upset",
    "disappointed",
    "frustrated",
}


def _tokenize(text: str) -> list[str]:
    """Return a list of lowercase word tokens from *text*.

    Uses a simple regex to avoid external dependencies.
    """
    return re.findall(r"\b\w+\b", text.lower())


def analyze_mood(text: str) -> dict:
    """Analyze *text* and return a dict with ``sentiment`` and ``emoji``.

    The algorithm counts occurrences of words from the positive and negative
    lexicons.  Ties are considered neutral.
    """
    tokens = _tokenize(text)
    pos_count = sum(token in POSITIVE_WORDS for token in tokens)
    neg_count = sum(token in NEGATIVE_WORDS for token in tokens)

    if pos_count > neg_count:
        sentiment = "positive"
        emoji = "😊"
    elif neg_count > pos_count:
        sentiment = "negative"
        emoji = "😞"
    else:
        sentiment = "neutral"
        emoji = "😐"

    return {"sentiment": sentiment, "emoji": emoji}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Analyze the mood of a text snippet and output an emoji."
    )
    parser.add_argument(
        "text",
        nargs="+",
        help="The text to analyze (provide as a single quoted string or multiple words).",
    )
    args = parser.parse_args(argv)
    text = " ".join(args.text)
    result = analyze_mood(text)
    print(f"{result['emoji']} ({result['sentiment']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
