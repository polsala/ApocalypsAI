'''emoji_generator.py

Provides functions to map commit message text to an emoji prefix.
'''

from __future__ import annotations

from typing import List, Tuple

# Simple keyword‑to‑emoji mapping
KEYWORD_EMOJI_MAP: List[Tuple[List[str], str]] = [
    (['add', 'create', 'init', 'implement'], '✨'),
    (['fix', 'bug', 'patch', 'resolve'], '🐛'),
    (['remove', 'delete', 'rm'], '🗑️'),
    (['docs', 'readme', 'documentation'], '📝'),
    (['test', 'testing', 'unittest'], '✅'),
    (['refactor', 'restructure', 'clean'], '🧹'),
    (['performance', 'speed', 'optimize'], '⚡'),
    (['ci', 'cd', 'pipeline'], '🤖'),
    (['security', 'vuln', 'audit'], '🔒'),
]

DEFAULT_EMOJI = '🔧'


def suggest_emoji(message: str) -> str:
    """Return an emoji based on the first matching keyword in *message*.

    The search is case‑insensitive and looks for substring matches.
    """
    lowered = message.lower()
    for keywords, emoji in KEYWORD_EMOJI_MAP:
        for kw in keywords:
            if kw in lowered:
                return emoji
    return DEFAULT_EMOJI


def format_commit(message: str) -> str:
    """Prepend the suggested emoji to *message* and return the formatted string."""
    emoji = suggest_emoji(message)
    return f"{emoji} {message.strip()}"
