import re
from typing import Dict

# Mapping of keywords to emojis
_EMOJI_MAP: Dict[str, str] = {
    "coffee": "☕",
    "sunshine": "🌞",
    "pizza": "🍕",
    "cat": "🐱",
    "dog": "🐶",
    "love": "❤️",
    "fire": "🔥",
    "star": "⭐",
    "music": "🎵",
    "book": "📚",
}

def annotate(text: str) -> str:
    """
    Return a new string where each keyword found in the text is followed by its emoji.
    Matching is case‑insensitive and respects word boundaries.
    """
    def replacer(match: re.Match) -> str:
        word = match.group(0)
        emoji = _EMOJI_MAP[word.lower()]
        return f"{word} {emoji}"

    # Build a regex that matches any of the keywords, case‑insensitive
    pattern = re.compile(r"\b(" + "|".join(map(re.escape, _EMOJI_MAP.keys())) + r")\b", re.IGNORECASE)
    return pattern.sub(replacer, text)
