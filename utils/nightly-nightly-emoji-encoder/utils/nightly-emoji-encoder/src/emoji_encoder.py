"""
Emoji Encoder utility.

Provides `encode(text: str) -> str` and `decode(emojis: str) -> str`.

Only lowercase a-z are supported.
"""

import argparse
import sys

# Mapping of letters to emojis (26 unique emojis)
LETTER_TO_EMOJI = {
    'a': '😀', 'b': '😁', 'c': '😂', 'd': '🤣', 'e': '😃',
    'f': '😄', 'g': '😅', 'h': '😆', 'i': '😉', 'j': '😊',
    'k': '😋', 'l': '😎', 'm': '😍', 'n': '😘', 'o': '🥰',
    'p': '😗', 'q': '😙', 'r': '😚', 's': '☺️', 't': '🙂',
    'u': '🤗', 'v': '🤩', 'w': '🤔', 'x': '🤨', 'y': '😐',
    'z': '😑',
}
EMOJI_TO_LETTER = {v: k for k, v in LETTER_TO_EMOJI.items()}


def encode(text: str) -> str:
    """Encode a lowercase alphabetic string to emojis."""
    result = []
    for ch in text:
        if ch not in LETTER_TO_EMOJI:
            raise ValueError(f"Unsupported character for encoding: {ch!r}")
        result.append(LETTER_TO_EMOJI[ch])
    return ''.join(result)


def decode(emojis: str) -> str:
    """Decode an emoji sequence back to the original string.

    Emojis may be multi‑codepoint (e.g., ☺️). We greedily match the longest known emoji.
    """
    i = 0
    decoded = []
    emojis_len = len(emojis)
    # Sort emojis by length descending for greedy matching
    sorted_emojis = sorted(EMOJI_TO_LETTER.keys(), key=len, reverse=True)
    while i < emojis_len:
        match = None
        for emo in sorted_emojis:
            if emojis.startswith(emo, i):
                match = emo
                break
        if not match:
            raise ValueError(f"Unsupported emoji sequence at position {i}")
        decoded.append(EMOJI_TO_LETTER[match])
        i += len(match)
    return ''.join(decoded)


def _main(argv=None):
    parser = argparse.ArgumentParser(description="Encode or decode strings to emojis.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    enc = subparsers.add_parser("encode", help="Encode text to emojis")
    enc.add_argument("text", help="Lowercase alphabetic text to encode")

    dec = subparsers.add_parser("decode", help="Decode emojis to text")
    dec.add_argument("emojis", help="Emoji sequence to decode")

    args = parser.parse_args(argv)

    try:
        if args.command == "encode":
            out = encode(args.text)
        else:
            out = decode(args.emojis)
        print(out)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    _main()
