import argparse
import json
import sys
from pathlib import Path
from typing import Dict

# Mapping from mood score (0‑4) to emoji
MOOD_EMOJI_MAP = {
    0: "😞",
    1: "🙁",
    2: "😐",
    3: "🙂",
    4: "😄",
}


def mood_to_emoji(score: int) -> str:
    """Return the emoji corresponding to a mood *score*.

    Args:
        score: Integer between 0 and 4 inclusive.
    Returns:
        A single‑character emoji string.
    Raises:
        ValueError: If *score* is outside the 0‑4 range.
    """
    if score not in MOOD_EMOJI_MAP:
        raise ValueError(f"Mood score must be between 0 and 4, got {score}")
    return MOOD_EMOJI_MAP[score]


def load_mood_file(file_path: Path) -> Dict[str, int]:
    """Load a JSON file mapping dates to mood scores.

    The function validates that each value is an integer within the allowed range.
    """
    try:
        raw = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {file_path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise ValueError("Mood file must contain a JSON object mapping dates to scores")

    validated: Dict[str, int] = {}
    for date_str, score in raw.items():
        if not isinstance(score, int):
            raise ValueError(f"Score for {date_str} must be an integer, got {type(score)}")
        if score not in MOOD_EMOJI_MAP:
            raise ValueError(f"Score for {date_str} out of range (0‑4): {score}")
        validated[date_str] = score
    return validated


def print_mood_report(mood_data: Dict[str, int]) -> None:
    """Print each date with its corresponding emoji, sorted chronologically."""
    for date in sorted(mood_data):
        emoji = mood_to_emoji(mood_data[date])
        print(f"{date} {emoji}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert daily mood scores to emojis.")
    parser.add_argument("json_file", type=Path, help="Path to JSON file with date→score mapping")
    args = parser.parse_args(argv)

    try:
        mood_data = load_mood_file(args.json_file)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print_mood_report(mood_data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
