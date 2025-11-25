"""emoji_annotator – sprinkle emojis onto text based on simple keyword rules.

The module provides:
- ``EMOJI_MAP`` – a static dictionary of keyword → emoji.
- ``annotate(text: str) -> str`` – returns the input string with emojis appended after each matching word.
- ``main()`` – CLI entry point using ``argparse``.

The implementation is deliberately pure‑Python and has **no external dependencies**.
"""

from __future__ import annotations

import argparse
import re
from typing import Dict

# ---------------------------------------------------------------------------
# Static keyword → emoji mapping (deterministic, no external look‑ups)
# ---------------------------------------------------------------------------
EMOJI_MAP: Dict[str, str] = {
    "happy": "😊",
    "sad": "😢",
    "fire": "🔥",
    "love": "❤️",
    "warning": "⚠️",
    "error": "❌",
    "success": "✅",
    "fail": "💥",
    "bug": "🐛",
    "rocket": "🚀",
}

# Pre‑compile a regex that matches any of the keys as whole words, case‑insensitive.
_KEYWORDS_PATTERN = re.compile(r"\\b(" + "|".join(map(re.escape, EMOJI_MAP.keys())) + r")\\b", re.IGNORECASE)


def _replace_match(match: re.Match) -> str:
    """Helper for ``re.sub`` – returns the matched word plus its emoji.

    The original casing of the word is preserved; the emoji is looked up using
    the lower‑cased key.
    """
    word = match.group(0)
    emoji = EMOJI_MAP[word.lower()]
    return f"{word} {emoji}"


def annotate(text: str) -> str:
    """Return *text* with emojis appended after each recognised keyword.

    Example
    -------
    >>> annotate("I am happy but also sad")
    'I am happy 😊 but also sad 😢'
    """
    # ``re.sub`` will call ``_replace_match`` for each occurrence.
    return _KEYWORDS_PATTERN.sub(_replace_match, text)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="emoji-annotator",
        description="Append context‑aware emojis to a line of text.",
    )
    parser.add_argument(
        "text",
        nargs="+",
        help="The text to annotate (multiple words are joined with spaces).",
    )
    return parser


def main() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()
    input_text = " ".join(args.text)
    annotated = annotate(input_text)
    print(annotated)


if __name__ == "__main__":
    main()
