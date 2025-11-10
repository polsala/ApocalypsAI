"""emoji_commit_helper.py

A tiny utility that suggests an emoji prefix for Git commit messages based on simple keyword heuristics.

The module provides:
- `suggest_emoji(message: str) -> str`: Returns the original message prefixed with an appropriate emoji.
- CLI entry‑point when executed as a module.

The implementation is deliberately lightweight and contains no external dependencies.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Tuple

# Mapping of keyword tuples to emojis. Order matters – first match wins.
_EMOJI_MAP: List[Tuple[Tuple[str, ...], str]] = [
    (("add", "create", "implement", "feature", "new"), "🚀"),
    (("fix", "bug", "patch", "resolve", "hotfix"), "🐛"),
    (("docs", "readme", "documentation", "doc"), "📚"),
    (("refactor", "clean", "restructure", "reformat"), "🛠️"),
    (("test", "tests", "coverage", "spec"), "✅"),
    (("chore", "ci", "build", "release"), "⚙️"),
]

_DEFAULT_EMOJI = "✨"


def _normalize(text: str) -> List[str]:
    """Return a list of lower‑cased words stripped of punctuation.

    Simple tokenisation sufficient for our heuristic matching.
    """
    # Replace common punctuation with spaces, then split.
    for ch in ",.;:!?")
        text = text.replace(ch, " ")
    return [word.lower() for word in text.split() if word]


def _find_emoji(words: List[str]) -> str:
    """Return the first matching emoji based on _EMOJI_MAP.

    If no keyword matches, return the default emoji.
    """
    for keywords, emoji in _EMOJI_MAP:
        if any(word in keywords for word in words):
            return emoji
    return _DEFAULT_EMOJI


def suggest_emoji(message: str) -> str:
    """Return *message* prefixed with an appropriate emoji.

    Parameters
    ----------
    message: str
        The raw commit message.

    Returns
    -------
    str
        Emoji‑prefixed commit message.
    """
    words = _normalize(message)
    emoji = _find_emoji(words)
    return f"{emoji} {message.strip()}"


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Suggest an emoji prefix for a Git commit message."
    )
    parser.add_argument(
        "message",
        nargs="+",
        help="The commit message (provide as a single quoted string or multiple words).",
    )
    args = parser.parse_args()
    raw_message = " ".join(args.message)
    result = suggest_emoji(raw_message)
    print(result)


if __name__ == "__main__":
    # When executed via `python -m emoji_commit_helper`.
    _cli()
