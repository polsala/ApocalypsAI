import argparse
from typing import Dict

# Mapping of uppercase letters to emojis (chosen arbitrarily but deterministically)
LETTER_TO_EMOJI: Dict[str, str] = {
    "A": "😀",
    "B": "😁",
    "C": "😂",
    "D": "😃",
    "E": "😄",
    "F": "😅",
    "G": "😆",
    "H": "😉",
    "I": "😊",
    "J": "😋",
    "K": "😎",
    "L": "😍",
    "M": "😘",
    "N": "🥰",
    "O": "😗",
    "P": "😙",
    "Q": "😚",
    "R": "🙂",
    "S": "🤗",
    "T": "🤩",
    "U": "🤔",
    "V": "🤨",
    "W": "😐",
    "X": "😑",
    "Y": "😶",
    "Z": "🙄",
}

EMOJI_TO_LETTER = {v: k for k, v in LETTER_TO_EMOJI.items()}


def encode(text: str) -> str:
    """Encode an uppercase ASCII string into emojis.

    Args:
        text: The string to encode. Must contain only A‑Z characters.
    Returns:
        A string of concatenated emojis.
    Raises:
        ValueError: If any character is not an uppercase A‑Z letter.
    """
    encoded_parts = []
    for ch in text:
        if ch not in LETTER_TO_EMOJI:
            raise ValueError(f"Unsupported character for encoding: {ch!r}")
        encoded_parts.append(LETTER_TO_EMOJI[ch])
    return "".join(encoded_parts)


def decode(emoji_str: str) -> str:
    """Decode an emoji string back to the original uppercase text.

    Args:
        emoji_str: The concatenated emojis produced by ``encode``.
    Returns:
        The original uppercase string.
    Raises:
        ValueError: If any emoji in the sequence is not recognized.
    """
    decoded_chars = []
    # Emojis are single Unicode codepoints in our mapping, so we can iterate by character.
    for em in emoji_str:
        if em not in EMOJI_TO_LETTER:
            raise ValueError(f"Unsupported emoji for decoding: {em!r}")
        decoded_chars.append(EMOJI_TO_LETTER[em])
    return "".join(decoded_chars)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Encode or decode strings using emoji mapping.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    enc_parser = subparsers.add_parser("encode", help="Encode uppercase text to emojis")
    enc_parser.add_argument("text", type=str, help="Uppercase text to encode (A-Z only)")

    dec_parser = subparsers.add_parser("decode", help="Decode emojis back to text")
    dec_parser.add_argument("emoji", type=str, help="Emoji string to decode")

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    try:
        if args.command == "encode":
            result = encode(args.text)
        else:  # decode
            result = decode(args.emoji)
        print(result)
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
