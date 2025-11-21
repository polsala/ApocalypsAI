import argparse
import sys
from pathlib import Path
from collections import Counter
from typing import Dict, List

# Mapping of supported mood keywords to their emoji representation
MOOD_EMOJI: Dict[str, str] = {
    "happy": "😊",
    "sad": "😢",
    "excited": "🤩",
    "angry": "😠",
    "neutral": "😐",
    "tired": "😴",
}


def parse_mood_log(file_path: Path) -> Counter:
    """Read a mood log file and count occurrences of each supported mood.

    Args:
        file_path: Path to the mood log file.

    Returns:
        Counter mapping mood keywords to their frequencies.
    """
    if not file_path.is_file():
        raise FileNotFoundError(f"Mood log file not found: {file_path}")

    counts = Counter()
    for line in file_path.read_text(encoding="utf-8").splitlines():
        mood = line.strip().lower()
        if not mood:
            continue  # skip empty lines
        if mood not in MOOD_EMOJI:
            # Unknown moods are ignored but could be logged in a real tool
            continue
        counts[mood] += 1
    return counts


def emoji_summary(counts: Counter) -> str:
    """Convert mood counts into a concatenated emoji string.

    The order follows the definition order in ``MOOD_EMOJI``.
    """
    emojis: List[str] = []
    for mood, emoji in MOOD_EMOJI.items():
        emojis.extend([emoji] * counts.get(mood, 0))
    return "".join(emojis)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read a mood log file and output an emoji summary."
    )
    parser.add_argument(
        "log_path",
        type=Path,
        help="Path to the mood log file (one mood keyword per line).",
    )
    args = parser.parse_args(argv)

    try:
        counts = parse_mood_log(args.log_path)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1

    summary = emoji_summary(counts)
    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
