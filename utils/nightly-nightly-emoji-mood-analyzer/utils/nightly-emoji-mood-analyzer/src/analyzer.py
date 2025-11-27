import sys
import json
from collections import Counter
from typing import Dict, List

# Mapping of emojis to their corresponding mood labels
EMOJI_MOOD_MAP: Dict[str, str] = {
    "😀": "happy",
    "😃": "happy",
    "😂": "joy",
    "😢": "sad",
    "😭": "sad",
    "😡": "angry",
    "🤔": "thinking",
    "👍": "approval",
    "👎": "disapproval",
    "❤️": "love",
    "💔": "heartbreak",
    "🤯": "mindblown",
    "🥳": "celebration",
}

def _extract_emojis(text: str) -> List[str]:
    """Return a list of emojis found in *text* that are present in ``EMOJI_MOOD_MAP``.

    Characters not in the map are ignored – this keeps the function deterministic
    and offline.
    """
    return [ch for ch in text if ch in EMOJI_MOOD_MAP]

def analyze_emojis(text: str) -> Dict[str, int]:
    """Analyze *text* and return a ``{mood: count}`` dictionary.

    The function is pure and has no side‑effects, making it trivial to test.
    """
    emojis = _extract_emojis(text)
    moods = [EMOJI_MOOD_MAP[e] for e in emojis]
    return dict(Counter(moods))

def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m utils/nightly-emoji-mood-analyzer/src/analyzer \"<emoji string>\"")
        sys.exit(1)
    input_text = sys.argv[1]
    result = analyze_emojis(input_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    _cli()
