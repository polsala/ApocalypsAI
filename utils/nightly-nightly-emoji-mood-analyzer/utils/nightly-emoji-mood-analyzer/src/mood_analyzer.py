#!/usr/bin/env python3
"""Emoji Mood Analyzer

Scans a text file for emojis and reports the dominant mood category.
"""
import sys
import re
from collections import Counter
from typing import Dict, List

# Mapping emojis to mood categories
EMOJI_MOOD_MAP: Dict[str, str] = {
    "😀": "happy",
    "😃": "happy",
    "😄": "happy",
    "😁": "happy",
    "😂": "happy",
    "😊": "happy",
    "😍": "love",
    "🥰": "love",
    "❤️": "love",
    "💖": "love",
    "😢": "sad",
    "😭": "sad",
    "😞": "sad",
    "☹️": "sad",
    "😠": "angry",
    "😡": "angry",
    "🤬": "angry",
}

# Build a regex that matches any of the emojis in the map
EMOJI_PATTERN = re.compile(
    "[" + "".join(re.escape(e) for e in EMOJI_MOOD_MAP.keys()) + "]"
)


def extract_emojis(text: str) -> List[str]:
    """Return a list of emojis found in the text."""
    return EMOJI_PATTERN.findall(text)


def categorize_emojis(emojis: List[str]) -> str:
    """Return the dominant mood category or 'neutral'."""
    if not emojis:
        return "neutral"
    moods = [EMOJI_MOOD_MAP[e] for e in emojis if e in EMOJI_MOOD_MAP]
    if not moods:
        return "neutral"
    counter = Counter(moods)
    most_common = counter.most_common(1)[0][0]
    return most_common


def analyze_file(path: str) -> str:
    """Read file and return dominant mood."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    emojis = extract_emojis(content)
    return categorize_emojis(emojis)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m emoji_mood_analyzer <path-to-text-file>")
        sys.exit(1)
    path = sys.argv[1]
    try:
        mood = analyze_file(path)
        print(mood)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
