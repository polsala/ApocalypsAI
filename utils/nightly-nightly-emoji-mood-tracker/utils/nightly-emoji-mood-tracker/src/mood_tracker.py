import argparse
import sys
from pathlib import Path
from typing import Dict

# Mapping of mood keywords to emojis
MOOD_MAP = {
    "happy": "😊",
    "joyful": "😊",
    "excited": "😊",
    "glad": "😊",
    "sad": "😞",
    "down": "😞",
    "depressed": "😞",
    "unhappy": "😞",
    "angry": "😡",
    "mad": "😡",
    "furious": "😡",
    "tired": "😴",
    "exhausted": "😴",
    "sleepy": "😴",
    "love": "❤️",
    "loved": "❤️",
    "affection": "❤️",
}

DEFAULT_EMOJI = "🤔"


def _extract_emoji(text: str) -> str:
    """Return the first matching emoji for the given text.

    The function lower‑cases the text and checks for any keyword present in
    ``MOOD_MAP``. If multiple keywords match, the first encountered in the
    iteration order of ``MOOD_MAP`` wins.
    """
    lowered = text.lower()
    for keyword, emoji in MOOD_MAP.items():
        if keyword in lowered:
            return emoji
    return DEFAULT_EMOJI


def parse_journal(file_path: str) -> Dict[str, str]:
    """Parse a journal file and return a mapping of date → emoji.

    Expected line format::

        YYYY-MM-DD <free‑form description>

    Blank lines and lines that do not start with a valid date are ignored.
    """
    result: Dict[str, str] = {}
    path = Path(file_path)
    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Split on first whitespace to separate date from description
                parts = line.split(maxsplit=1)
                if len(parts) != 2:
                    continue  # malformed line
                date_part, description = parts
                # Very light validation of date format (YYYY‑MM‑DD)
                if len(date_part) != 10 or date_part[4] != "-" or date_part[7] != "-":
                    continue
                emoji = _extract_emoji(description)
                result[date_part] = emoji
    except FileNotFoundError:
        print(f"Error: file not found – {file_path}", file=sys.stderr)
        raise
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an emoji mood summary from a journal file.")
    parser.add_argument("journal", type=str, help="Path to the journal text file")
    args = parser.parse_args()
    summary = parse_journal(args.journal)
    for date, emoji in sorted(summary.items()):
        print(f"{date} {emoji}")


if __name__ == "__main__":
    main()
