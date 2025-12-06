"""ANSI Keyword Highlighter utility.

Provides a simple function to wrap common log keywords with ANSI color codes.
"""

import re
from typing import Dict

# Mapping of keywords to ANSI color codes
_COLOR_MAP: Dict[str, str] = {
    "error": "\x1b[31m",   # Red
    "warning": "\x1b[33m", # Yellow
    "info": "\x1b[32m",    # Green
}

_RESET = "\x1b[0m"


def _replace_keyword(match: re.Match) -> str:
    word = match.group(0)
    lower = word.lower()
    color = _COLOR_MAP.get(lower, "")
    return f"{color}{word}{_RESET}" if color else word


def highlight(text: str) -> str:
    """Return *text* with log keywords colored using ANSI escape codes.

    Keywords are matched case‑insensitively as whole words.
    """
    pattern = re.compile(r"\b(error|warning|info)\b", re.IGNORECASE)
    return pattern.sub(_replace_keyword, text)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m ansi_keyword_highlighter \"<message>\"")
        sys.exit(1)
    print(highlight(sys.argv[1]))
