import argparse
import sys
from pathlib import Path
from typing import List

# Mapping from lower‑cased keywords to emojis
MOOD_EMOJI_MAP = {
    "happy": "😄",
    "great": "😄",
    "awesome": "😄",
    "sad": "😢",
    "down": "😢",
    "gloomy": "😢",
    "angry": "😠",
    "mad": "😠",
    "furious": "😠",
    "love": "❤️",
    "loved": "❤️",
    "heart": "❤️",
    "confused": "🤔",
    "unsure": "🤔",
    "meh": "🤔",
}

DEFAULT_EMOJI = "❓"


def mood_to_emoji(mood: str) -> str:
    """Return the emoji that best matches *mood*.

    The function looks for any keyword present in the lower‑cased mood string.
    If multiple keywords match, the first encountered in the mapping order wins.
    If none match, a default ❓ is returned.
    """
    lowered = mood.lower()
    for keyword, emoji in MOOD_EMOJI_MAP.items():
        if keyword in lowered:
            return emoji
    return DEFAULT_EMOJI


def parse_moods_from_args(args: argparse.Namespace) -> List[str]:
    """Collect mood strings from CLI arguments.

    - If ``--file`` is provided, read each line as a mood.
    - Remaining positional arguments are treated as moods.
    """
    moods: List[str] = []
    if args.file:
        # Mock rationale: reading a local file is safe and deterministic.
        file_path = Path(args.file)
        if file_path.is_file():
            moods.extend([line.rstrip("\n") for line in file_path.read_text().splitlines() if line.strip()])
    if args.moods:
        moods.extend(args.moods)
    return moods


def main() -> None:
    parser = argparse.ArgumentParser(description="Translate mood descriptions to emojis.")
    parser.add_argument("moods", nargs="*", help="Mood strings to translate.")
    parser.add_argument("--file", "-f", type=str, help="Path to a file containing one mood per line.")
    args = parser.parse_args()

    moods = parse_moods_from_args(args)
    if not moods:
        # If no moods supplied, read from stdin line‑by‑line.
        # Mock rationale: stdin is provided by the caller; reading it is deterministic in tests.
        moods = [line.rstrip("\n") for line in sys.stdin if line.strip()]

    for mood in moods:
        emoji = mood_to_emoji(mood)
        print(f"{mood} → {emoji}")


if __name__ == "__main__":
    main()
