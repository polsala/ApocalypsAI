"""emoji_lookup.py

A tiny, self‑contained module that maps human‑readable keywords to Unicode emoji.

The public API consists of a single function:

    get_emoji(keyword: str) -> str | None

If the keyword is present in the internal dictionary (case‑insensitive), the corresponding emoji string is returned; otherwise ``None`` is returned.

The module also provides a small CLI for quick ad‑hoc lookups.
"""

from __future__ import annotations

from typing import Dict, Optional

# ---------------------------------------------------------------------------
# Internal static mapping. Feel free to extend.
# ---------------------------------------------------------------------------
_EMOJI_MAP: Dict[str, str] = {
    "rocket": "🚀",
    "coffee": "☕",
    "fire": "🔥",
    "thumbs up": "👍",
    "party": "🥳",
    "bug": "🐛",
    "heart": "❤️",
    "star": "⭐",
    "clap": "👏",
    "tada": "🎉",
    "book": "📚",
    "computer": "💻",
    "light bulb": "💡",
    "warning": "⚠️",
    "question": "❓",
    "exclamation": "❗",
}


def _normalize(keyword: str) -> str:
    """Return a lower‑cased, stripped version of *keyword* for lookup.

    This helper exists to keep the public ``get_emoji`` function tidy.
    """
    return keyword.strip().lower()


def get_emoji(keyword: str) -> Optional[str]:
    """Return the emoji matching *keyword* or ``None`` if not found.

    Parameters
    ----------
    keyword: str
        Human‑readable description, e.g. ``"rocket"`` or ``"thumbs up"``.

    Returns
    -------
    str | None
        The Unicode emoji string or ``None`` when the keyword is unknown.
    """
    normalized = _normalize(keyword)
    return _EMOJI_MAP.get(normalized)


def _cli() -> None:
    """Simple command‑line interface.

    Usage: ``python -m utils.nightly-emoji-lookup.src.emoji_lookup <keyword>``
    """
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Lookup an emoji by keyword.")
    parser.add_argument("keyword", help="Keyword to look up, e.g. 'rocket'")
    args = parser.parse_args()

    emoji = get_emoji(args.keyword)
    if emoji:
        print(emoji)
    else:
        # Print nothing but exit with code 1 to signal "not found"
        sys.exit(1)


if __name__ == "__main__":
    _cli()
