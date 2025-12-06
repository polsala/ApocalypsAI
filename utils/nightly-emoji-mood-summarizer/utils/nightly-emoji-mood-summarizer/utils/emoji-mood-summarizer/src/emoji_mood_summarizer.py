"""emoji_mood_summarizer
~~~~~~~~~~~~~~~~~~~~~~~~

Provides a single public function :func:`summarize_moods` that maps a list of textual mood entries to a representative emoji.

The mapping is deliberately simple and deterministic:

- ``happy``   → ``😊``
- ``sad``     → ``😢``
- ``angry``   → ``😠``
- ``neutral`` → ``😐``
- any other   → ``🤔`` (fallback)

If multiple moods tie for the highest count, the one that appears first in the predefined order is chosen.
"""

from collections import Counter
from typing import Iterable, List

# Mapping from normalized mood string to emoji
MOOD_EMOJI_MAP = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "neutral": "😐",
}

# Order of precedence when ties occur
MOOD_ORDER = ["happy", "sad", "angry", "neutral"]


def _normalize(mood: str) -> str:
    """Return a lowercase stripped version of *mood*.

    Mock rationale: Normalization keeps the function robust to user input variations
    without requiring external libraries.
    """
    return mood.strip().lower()


def summarize_moods(moods: Iterable[str]) -> str:
    """Return an emoji representing the dominant mood.

    Parameters
    ----------
    moods:
        An iterable of mood strings (e.g., ``["happy", "sad"]``).

    Returns
    -------
    str
        The emoji that best represents the most frequent mood.
        Unknown moods fall back to the thinking face ``🤔``.
    """
    # Convert to list to allow multiple passes
    mood_list: List[str] = [_normalize(m) for m in moods if m]
    if not mood_list:
        return "🤔"

    counts = Counter(mood_list)
    # Determine the highest frequency
    max_count = max(counts.values())
    # Gather all moods that share the max count
    candidates = [m for m, c in counts.items() if c == max_count]

    # Resolve ties using predefined order
    for mood in MOOD_ORDER:
        if mood in candidates:
            return MOOD_EMOJI_MAP[mood]

    # If none of the ordered moods are present, pick the first candidate and fallback emoji
    return "🤔"


def _cli() -> None:
    """Simple command‑line interface.

    Usage example:
        python -m emoji_mood_summarizer happy sad happy
    """
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m emoji_mood_summarizer <mood1> [<mood2> ...]")
        sys.exit(2)
    result = summarize_moods(sys.argv[1:])
    print(result)


if __name__ == "__main__":
    _cli()
