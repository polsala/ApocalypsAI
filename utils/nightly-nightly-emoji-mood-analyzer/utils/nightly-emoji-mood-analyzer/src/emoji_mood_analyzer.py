import argparse
import sys
from collections import Counter
from typing import Dict, List

# Mapping of emojis to mood categories
EMOJI_MOOD_MAP: Dict[str, str] = {
    "😄": "happy",
    "😊": "happy",
    "😁": "happy",
    "😢": "sad",
    "😞": "sad",
    "😔": "sad",
    "😡": "angry",
    "🤬": "angry",
    "😠": "angry",
}

def _extract_emojis(text: str) -> List[str]:
    """Return a list of emojis found in *text* that are present in EMOJI_MOOD_MAP.

    The function simply iterates over each character; this is sufficient because the
    emojis we care about are single Unicode code points.
    """
    return [ch for ch in text if ch in EMOJI_MOOD_MAP]

def analyze_mood(text: str) -> str:
    """Analyze *text* and return the dominant mood.

    - If no known emojis are present, returns ``"neutral"``.
    - If there is a tie, the first mood in alphabetical order wins (deterministic).
    """
    emojis = _extract_emojis(text)
    if not emojis:
        return "neutral"
    mood_counts = Counter(EMOJI_MOOD_MAP[e] for e in emojis)
    # Find the highest count; ``most_common`` already sorts by count then key order.
    most_common = mood_counts.most_common()
    top_count = most_common[0][1]
    # Gather all moods with the top count to resolve ties deterministically.
    tied_moods = [mood for mood, cnt in most_common if cnt == top_count]
    return sorted(tied_moods)[0]

def _read_file(path: str) -> str:
    """Read the entire file as UTF‑8 text.

    # Mock rationale: In tests we replace this function with a mock that returns a
    # predetermined string, ensuring offline deterministic behaviour.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Detect the dominant emoji‑based mood in a string or file."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("text", nargs="?", help="Raw text to analyze.")
    group.add_argument("--file", dest="file_path", help="Path to a UTF‑8 text file.")
    args = parser.parse_args(argv)

    if args.file_path:
        try:
            text = _read_file(args.file_path)
        except Exception as exc:
            print(f"Error reading file: {exc}", file=sys.stderr)
            return 1
    else:
        text = args.text or ""

    mood = analyze_mood(text)
    print(mood)
    return 0

if __name__ == "__main__":
    sys.exit(main())
