import sys
import pathlib
from typing import Dict, List, Tuple

# Mapping of ASCII emoticons to (emoji, mood_category)
EMOTICON_MAP: Dict[str, Tuple[str, str]] = {
    ":)": ("😄", "happy"),
    ":-)": ("😄", "happy"),
    ":D": ("😁", "happy"),
    ":-D": ("😁", "happy"),
    ":(": ("😞", "sad"),
    ":-(": ("😞", "sad"),
    ":'(": ("😢", "sad"),
    ":'-)": ("😂", "happy"),
    ":o": ("😲", "surprised"),
    ":-o": ("😲", "surprised"),
    ":O": ("😲", "surprised"),
    ":-O": ("😲", "surprised"),
}

def replace_emoticons(text: str) -> Tuple[str, Dict[str, int]]:
    """Replace known emoticons with emojis and count moods.

    Returns a tuple of the transformed text and a dict mapping mood categories
    ("happy", "sad", "surprised") to their occurrence counts.
    """
    mood_counts = {"happy": 0, "sad": 0, "surprised": 0}
    transformed = text
    for emoticon, (emoji, mood) in EMOTICON_MAP.items():
        if emoticon in transformed:
            occurrences = transformed.count(emoticon)
            mood_counts[mood] += occurrences
            transformed = transformed.replace(emoticon, emoji)
    return transformed, mood_counts

def format_report(mood_counts: Dict[str, int]) -> str:
    lines = ["Mood Summary:"]
    for mood in ["happy", "sad", "surprised"]:
        lines.append(f"  {mood.capitalize():<9}: {mood_counts[mood]}")
    return "\n".join(lines)

def main(argv: List[str] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: python -m utils.nightly-emoji-mood-analyzer.src.analyzer <path-to-text-file>")
        return 2
    file_path = pathlib.Path(argv[0])
    if not file_path.is_file():
        print(f"Error: '{file_path}' does not exist or is not a file.")
        return 1
    try:
        raw_text = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Failed to read file: {e}")
        return 1
    transformed, mood_counts = replace_emoticons(raw_text)
    print("Transformed Text:")
    print(transformed)
    print()
    print(format_report(mood_counts))
    return 0

if __name__ == "__main__":
    sys.exit(main())
