"""emoji_commit_message_generator.generator

Core logic for turning a plain description into an emoji‑prefixed commit message.

The mapping is deliberately simple and deterministic – perfect for offline unit tests.
"""

from __future__ import annotations

import re
from typing import Dict

# Simple keyword → emoji map. Extendable but deterministic.
_EMOJI_MAP: Dict[str, str] = {
    "fix": "🐛",
    "bug": "🐛",
    "feature": "✨",
    "add": "✨",
    "docs": "📝",
    "doc": "📝",
    "refactor": "🔧",
    "rework": "🔧",
    "test": "✅",
    "tests": "✅",
    "chore": "🔨",
    "perf": "⚡",
    "performance": "⚡",
    "ci": "🤖",
    "build": "🏗️",
}

_DEFAULT_EMOJI = "🔖"


def _extract_keywords(description: str) -> list[str]:
    """Return a list of lower‑cased words from the description.

    Non‑alphabetic characters are stripped and the text is split on whitespace.
    """
    # Remove punctuation, keep only letters and spaces
    cleaned = re.sub(r"[^A-Za-z\s]", "", description)
    return [word.lower() for word in cleaned.split() if word]


def _choose_emoji(keywords: list[str]) -> str:
    """Pick the first matching emoji based on the keyword list.

    If none match, return the default emoji.
    """
    for kw in keywords:
        if kw in _EMOJI_MAP:
            return _EMOJI_MAP[kw]
    return _DEFAULT_EMOJI


def generate_message(description: str) -> str:
    """Generate an emoji‑prefixed commit message.

    Parameters
    ----------
    description: str
        Human‑readable description of the change (e.g., "fix crash on empty input").

    Returns
    -------
    str
        Emoji followed by a capitalised description.
    """
    if not description or not description.strip():
        raise ValueError("Description must be a non‑empty string")

    keywords = _extract_keywords(description)
    emoji = _choose_emoji(keywords)
    # Capitalise first character of the description, keep the rest as‑is
    formatted_desc = description.strip()
    formatted_desc = formatted_desc[0].upper() + formatted_desc[1:]
    return f"{emoji} {formatted_desc}"


def main() -> None:
    """CLI entry point.

    Usage: ``python -m emoji_commit_message_generator "your description"``
    """
    import argparse
    parser = argparse.ArgumentParser(description="Generate an emoji‑prefixed commit message")
    parser.add_argument("description", help="Plain commit description")
    args = parser.parse_args()
    try:
        msg = generate_message(args.description)
        print(msg)
    except Exception as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
