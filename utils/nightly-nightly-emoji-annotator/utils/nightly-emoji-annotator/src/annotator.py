import os
import sys
from typing import List

# Base keyword lists (very small on purpose)
POSITIVE_WORDS = {"good", "great", "awesome", "fantastic", "happy", "love", "excellent"}
NEGATIVE_WORDS = {"bad", "terrible", "sad", "hate", "poor", "awful", "worst"}


def load_extra_positive() -> List[str]:
    """Load extra positive words from the `EXTRA_POSITIVE` env var.

    The variable should contain a comma‑separated list, e.g. "splendid,marvelous".
    Returns an empty list if the variable is not set.
    """
    raw = os.getenv("EXTRA_POSITIVE", "")
    return [w.strip().lower() for w in raw.split(",") if w.strip()]


def get_sentiment(line: str) -> str:
    """Return 'positive', 'negative', or 'neutral' for *line*.

    The algorithm is a simple count of keyword occurrences.
    """
    words = {w.lower() for w in line.split()}
    pos = len(words & POSITIVE_WORDS)
    neg = len(words & NEGATIVE_WORDS)
    # Include any extra positive words supplied via env var
    extra_pos = set(load_extra_positive())
    pos += len(words & extra_pos)
    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    return "neutral"


def emoji_for_sentiment(sentiment: str) -> str:
    return {"positive": "😊", "negative": "😞", "neutral": "😐"}.get(sentiment, "😐")


def annotate_line(line: str) -> str:
    sentiment = get_sentiment(line)
    emoji = emoji_for_sentiment(sentiment)
    return f"{line.rstrip()} {emoji}\n"


def annotate_file(input_path: str, output_path: str | None = None) -> None:
    with open(input_path, "r", encoding="utf-8") as fin:
        lines = fin.readlines()
    annotated = [annotate_line(l) for l in lines]
    if output_path:
        with open(output_path, "w", encoding="utf-8") as fout:
            fout.writelines(annotated)
    else:
        sys.stdout.writelines(annotated)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m utils.nightly-emoji-annotator.src.annotator <input> [output]", file=sys.stderr)
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    annotate_file(input_file, output_file)
