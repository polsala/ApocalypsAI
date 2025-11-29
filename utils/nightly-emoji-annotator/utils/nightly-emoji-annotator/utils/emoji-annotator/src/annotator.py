"""emoji-annotator – simple keyword‑to‑emoji replacer.

The module provides a single public function ``annotate`` that scans a string for known
keywords and appends the matching emoji after each occurrence. The matching is case‑
insensitive and respects word boundaries.

Example
-------
>>> annotate("I love coffee and cats")
'I love coffee ☕ and cats 🐱'
"""

import re
from typing import Dict

# Mock rationale: a tiny, deterministic mapping – no external data sources.
KEYWORD_EMOJI_MAP: Dict[str, str] = {
    "coffee": "☕",
    "cat": "🐱",
    "dog": "🐶",
    "pizza": "🍕",
    "birthday": "🎂",
    "love": "❤️",
    "happy": "😊",
    "sun": "☀️",
    "star": "⭐",
    "music": "🎵",
}

# Pre‑compile a regex that matches any of the keywords as whole words, case‑insensitive.
_PATTERN = re.compile(r"\\b(" + "|".join(map(re.escape, KEYWORD_EMOJI_MAP.keys())) + r")\\b", re.IGNORECASE)


def _replace(match: re.Match) -> str:
    """Internal helper for ``re.sub``.

    It receives a match object, looks up the lower‑cased keyword in the map, and returns
    the original text followed by a space and the emoji.
    """
    word = match.group(0)
    emoji = KEYWORD_EMOJI_MAP[word.lower()]
    return f"{word} {emoji}"


def annotate(text: str) -> str:
    """Return *text* with emojis appended after known keywords.

    Parameters
    ----------
    text: str
        Input string to process.

    Returns
    -------
    str
        The annotated string.
    """
    # ``re.sub`` will call ``_replace`` for each match.
    return _PATTERN.sub(_replace, text)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Annotate a string with emojis based on keywords.")
    parser.add_argument("text", help="The text to annotate.")
    args = parser.parse_args()
    print(annotate(args.text))
