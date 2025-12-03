"""emoji_replacer.py

A tiny utility that replaces common textual emoticons with Unicode emojis.

Both a library function (`replace_emoticons`) and a minimal CLI are provided.
"""

import sys
from typing import Dict

# Mapping of emoticon patterns to their emoji equivalents.
EMOTICON_MAP: Dict[str, str] = {
    ":)": "😊",
    ":-)": "😊",
    ":D": "😊",
    ":-D": "😊",
    ":(": "🙁",
    ":-(": "🙁",
    ";)": "😉",
    ";-)": "😉",
    ":P": "😛",
    ":-P": "😛",
    ":O": "😮",
    ":-O": "😮",
    ":/": "😕",
    ":-/": "😕",
    ":'(": "😢",
}

def replace_emoticons(text: str) -> str:
    """Return *text* with all known emoticons replaced by emojis.

    The replacement is performed in a single pass; longer keys are checked first
    to avoid partial matches (e.g., `:-)` before `:)`).
    """
    # Sort keys by length descending to prefer longer patterns.
    for emoticon in sorted(EMOTICON_MAP.keys(), key=len, reverse=True):
        emoji = EMOTICON_MAP[emoticon]
        text = text.replace(emoticon, emoji)
    return text

def _cli() -> None:
    """Simple command‑line interface.

    Usage:
        python emoji_replacer.py "some text :)"
    or pipe data via stdin.
    """
    if not sys.stdin.isatty():
        # Data is being piped in.
        input_text = sys.stdin.read()
    elif len(sys.argv) > 1:
        # First argument after script name is the text.
        input_text = " ".join(sys.argv[1:])
    else:
        print("Usage: python emoji_replacer.py \"text with emoticons\"")
        sys.exit(2)

    output = replace_emoticons(input_text)
    print(output)

if __name__ == "__main__":
    _cli()
