"""emoji-annotator – add simple emojis to sentences based on keyword detection.

Public API
----------
- ``annotate(text: str) -> str`` – Return a new string with emojis inserted.
- ``main()`` – CLI entry point used when the module is executed as a script.
"""

import argparse
import re
from typing import Dict, List

# ---------------------------------------------------------------------------
# Keyword → Emoji mapping (deterministic, offline)
# ---------------------------------------------------------------------------
KEYWORD_EMOJI_MAP: Dict[str, str] = {
    "love": "❤️",
    "happy": "😊",
    "sad": "😢",
    "fire": "🔥",
    "star": "⭐",
    "question": "❓",
    "exclamation": "❗",
}


def _pick_emoji(sentence: str) -> str:
    """Return the first matching emoji for *sentence* or an empty string.

    Matching is case‑insensitive and looks for whole‑word occurrences.
    """
    lowered = sentence.lower()
    for keyword, emoji in KEYWORD_EMOJI_MAP.items():
        # ``\b`` ensures we match whole words only.
        if re.search(r"\b" + re.escape(keyword) + r"\b", lowered):
            return f" {emoji}"  # prepend a space for readability
    return ""


def annotate(text: str) -> str:
    """Insert emojis after each sentence that contains a known keyword.

    The function respects the original punctuation (``.``, ``!``, ``?``) and
    leaves whitespace untouched.
    """
    # Split while keeping delimiters (sentence‑ending punctuation).
    parts: List[str] = re.split(r"([.!?])", text)
    # ``parts`` will be like [sentence, delim, sentence, delim, ...]
    result_parts: List[str] = []
    for i in range(0, len(parts) - 1, 2):
        sentence = parts[i]
        delim = parts[i + 1]
        emoji = _pick_emoji(sentence)
        result_parts.append(sentence + emoji + delim)
    # If the original text ended without punctuation, ``parts`` has a trailing
    # element that is not a delimiter – we simply append it.
    if len(parts) % 2 == 1:
        result_parts.append(parts[-1])
    return "".join(result_parts)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Add emojis to text based on simple keywords.")
    parser.add_argument("text", help="The text to annotate. Enclose in quotes if it contains spaces.")
    return parser


def main() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()
    annotated = annotate(args.text)
    print(annotated)


if __name__ == "__main__":
    main()
