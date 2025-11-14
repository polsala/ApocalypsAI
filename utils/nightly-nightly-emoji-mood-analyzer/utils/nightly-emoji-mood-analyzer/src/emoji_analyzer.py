import sys
import json
import argparse
from collections import Counter
from typing import List, Dict

# Unicode emoji ranges (simplified). This covers most common emojis.
_EMOJI_RANGES = [
    (0x1F600, 0x1F64F),  # Emoticons
    (0x1F300, 0x1F5FF),  # Misc Symbols and Pictographs
    (0x1F680, 0x1F6FF),  # Transport & Map
    (0x2600, 0x26FF),    # Misc symbols
    (0x2700, 0x27BF),    # Dingbats
    (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
    (0x1FA70, 0x1FAFF),  # Symbols and Pictographs Extended-A
]

def _is_emoji(char: str) -> bool:
    """Return True if *char* is an emoji based on the simplified ranges.

    This function is deliberately lightweight; it does not aim for 100 % coverage
    but works well for the majority of everyday emojis.
    """
    cp = ord(char)
    return any(start <= cp <= end for start, end in _EMOJI_RANGES)

def extract_emojis(text: str) -> List[str]:
    """Extract all emoji characters from *text*.

    Multi‑code‑point emojis (e.g., skin‑tone modifiers) are treated as separate
    characters for simplicity. The downstream frequency count will still be
    meaningful for most use‑cases.
    """
    return [ch for ch in text if _is_emoji(ch)]

def analyze_emojis(messages: List[str]) -> Dict[str, int]:
    """Return a dictionary mapping each emoji to its occurrence count.

    The result is sorted in descending order of frequency.
    """
    counter = Counter()
    for msg in messages:
        emojis = extract_emojis(msg)
        counter.update(emojis)
    # Sort by count descending, then emoji lexicographically for stability
    return dict(sorted(counter.items(), key=lambda item: (-item[1], item[0])))

def _load_messages_from_file(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]

def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze emoji frequencies in a text file.")
    parser.add_argument("filepath", help="Path to a file containing one message per line.")
    args = parser.parse_args()
    messages = _load_messages_from_file(args.filepath)
    freq = analyze_emojis(messages)
    json.dump(freq, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")

if __name__ == "__main__":
    main()
