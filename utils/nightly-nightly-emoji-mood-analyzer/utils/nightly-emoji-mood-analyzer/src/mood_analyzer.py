"""Simple keyword‑based mood analyzer returning an emoji.

The implementation is deliberately lightweight: it does not depend on any external
libraries, performs a very naive tokenisation, and uses a small hard‑coded word list.
"""

from pathlib import Path
from typing import List

POSITIVE_WORDS = {
    "happy",
    "joy",
    "love",
    "excellent",
    "good",
    "great",
    "wonderful",
    "fantastic",
    "amazing",
    "pleased",
}

NEGATIVE_WORDS = {
    "sad",
    "angry",
    "hate",
    "terrible",
    "bad",
    "awful",
    "horrible",
    "upset",
    "depressed",
    "miserable",
}


def _tokenize(text: str) -> List[str]:
    """Very naive tokenisation: lower‑case split on alphabetic characters.

    This keeps the implementation self‑contained and deterministic.
    """
    import re

    return re.findall(r"[a-z]+", text.lower())


def analyze_mood(text: str) -> str:
    """Return an emoji representing the overall mood of *text*.

    The algorithm counts occurrences of words from the positive and negative sets
    and maps the resulting score to an emoji.
    """
    tokens = _tokenize(text)
    pos = sum(1 for t in tokens if t in POSITIVE_WORDS)
    neg = sum(1 for t in tokens if t in NEGATIVE_WORDS)
    score = pos - neg
    if score > 0:
        return "😊"
    if score < 0:
        return "😞"
    return "😐"


def load_text_from_path(path: str) -> str:
    """Read the entire file at *path* and return its contents.

    The helper exists so that callers can keep file I/O separate from the analysis
    logic, which simplifies testing (the file read can be mocked).
    """
    return Path(path).read_text(encoding="utf-8")
