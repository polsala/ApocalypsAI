import codecs
from typing import Dict

# 🎉 26 distinct emojis, one per alphabet letter (a‑z).
_EMOJI_MAP: Dict[str, str] = {
    "a": "😀",
    "b": "😁",
    "c": "😂",
    "d": "😃",
    "e": "😄",
    "f": "😅",
    "g": "😆",
    "h": "😇",
    "i": "😈",
    "j": "😉",
    "k": "😊",
    "l": "😋",
    "m": "😌",
    "n": "😍",
    "o": "🥰",
    "p": "😘",
    "q": "😗",
    "r": "😙",
    "s": "😚",
    "t": "☺️",
    "u": "🙂",
    "v": "🤗",
    "w": "🤩",
    "x": "🤔",
    "y": "🤨",
    "z": "😐",
}

# Reverse lookup for decoding.
_EMOJI_REVERSE: Dict[str, str] = {v: k for k, v in _EMOJI_MAP.items()}


def _rot13_char(ch: str) -> str:
    """Apply ROT13 to a single alphabetic character (lowercase)."""
    return codecs.encode(ch, "rot_13")


def encode(text: str) -> str:
    """Encode *text* by applying ROT13 and then substituting each letter with an emoji.

    Non‑alphabetic characters are preserved unchanged.
    """
    result = []
    for ch in text:
        if ch.isalpha():
            lower = ch.lower()
            rot = _rot13_char(lower)
            emoji = _EMOJI_MAP[rot]
            result.append(emoji)
        else:
            result.append(ch)
    return "".join(result)


def decode(emoji_text: str) -> str:
    """Reverse *emoji_text* back to the original plain‑text.

    The function assumes the input was produced by :func:`encode`.
    """
    result = []
    for ch in emoji_text:
        if ch in _EMOJI_REVERSE:
            letter = _EMOJI_REVERSE[ch]
            original = _rot13_char(letter)
            result.append(original)
        else:
            result.append(ch)
    return "".join(result)


if __name__ == "__main__":
    # Simple demo when run directly.
    sample = "Apocalypse Nightly"
    enc = encode(sample)
    dec = decode(enc)
    print(f"Original: {sample}\nEncoded : {enc}\nDecoded : {dec}")
