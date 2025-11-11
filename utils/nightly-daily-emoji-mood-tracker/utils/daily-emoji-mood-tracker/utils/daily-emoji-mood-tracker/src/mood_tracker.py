import argparse
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List

# Mapping of supported moods to emojis
MOOD_EMOJI_MAP: Dict[str, str] = {
    "happy": "😄",
    "sad": "😢",
    "angry": "😠",
    "excited": "🤩",
    "neutral": "😐",
    "confused": "🤔",
    "love": "❤️",
    "tired": "😴",
}


def parse_line(line: str) -> str:
    """Extract the mood keyword from a log line.

    Expected format: ``YYYY-MM-DD: mood`` (mood may contain spaces, we take the first word).
    Returns the mood in lower‑case if recognised, otherwise ``"unknown"``.
    """
    try:
        _, mood_part = line.split(":", 1)
        mood = mood_part.strip().split()[0].lower()
        return mood if mood in MOOD_EMOJI_MAP else "unknown"
    except ValueError:
        return "unknown"


def load_moods(file_path: Path) -> List[str]:
    """Read the file and return a list of recognised mood keys.

    Lines that cannot be parsed are ignored.
    """
    moods: List[str] = []
    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        mood = parse_line(raw_line)
        if mood != "unknown":
            moods.append(mood)
    return moods


def build_histogram(moods: List[str]) -> Counter:
    """Count occurrences of each mood.
    """
    return Counter(moods)


def format_histogram(counter: Counter) -> str:
    """Create a printable one‑line histogram using emojis.
    """
    parts = [f"{MOOD_EMOJI_MAP[mood]} {count}" for mood, count in counter.most_common()]
    return " | ".join(parts)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Parse a daily mood log and output an emoji histogram."
    )
    parser.add_argument(
        "log_file",
        type=Path,
        help="Path to the mood log file (plain text).",
    )
    args = parser.parse_args(argv)

    if not args.log_file.is_file():
        print(f"Error: file not found – {args.log_file}", file=sys.stderr)
        return 1

    moods = load_moods(args.log_file)
    if not moods:
        print("No recognizable moods found.")
        return 0

    histogram = build_histogram(moods)
    print(format_histogram(histogram))
    return 0


if __name__ == "__main__":
    sys.exit(main())
