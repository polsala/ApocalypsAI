import sys
import re
from typing import Dict

# Mapping of lower‑case keywords to emojis
_SENTIMENT_MAP: Dict[str, str] = {
    "happy": "😊",
    "joy": "😊",
    "glad": "😊",
    "sad": "😢",
    "unhappy": "😢",
    "down": "😢",
    "angry": "😠",
    "mad": "😠",
    "furious": "😠",
}

def _annotate_word(word: str) -> str:
    """Return the word with an emoji appended if a sentiment keyword is found.

    The original casing of the word is preserved; the lookup is case‑insensitive.
    """
    lowered = word.lower()
    emoji = _SENTIMENT_MAP.get(lowered)
    if emoji:
        return f"{word} {emoji}"
    return word

def annotate(text: str) -> str:
    """Annotate *text* with emojis based on simple sentiment keywords.

    Splits the input on whitespace, checks each token against the sentiment map,
    and joins the tokens back together. Punctuation attached to a word is kept
    intact because the lookup is performed on the raw token (including punctuation).
    """
    # Preserve original whitespace by using regex split that keeps delimiters
    tokens = re.split(r"(\s+)", text)
    annotated_tokens = [
        _annotate_word(tok) if not tok.isspace() else tok for tok in tokens
    ]
    return "".join(annotated_tokens)

def _cli() -> None:
    if len(sys.argv) > 1:
        input_text = " ".join(sys.argv[1:])
    else:
        input_text = sys.stdin.read().strip()
    print(annotate(input_text))

if __name__ == "__main__":
    _cli()
