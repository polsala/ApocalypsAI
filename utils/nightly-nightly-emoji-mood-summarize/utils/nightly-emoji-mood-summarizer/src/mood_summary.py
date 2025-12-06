import csv
import sys
from pathlib import Path
from typing import List

MOOD_EMOJI = {
    5: "😄",
    4: "😊",
    3: "😐",
    2: "🙁",
    1: "😞",
}

def read_mood_csv(csv_path: Path) -> List[int]:
    """Read mood scores from a CSV file and return them in order."""
    moods = []
    with csv_path.open(newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                mood = int(row["mood"])
                if mood not in MOOD_EMOJI:
                    raise ValueError(f"Invalid mood value: {mood}")
                moods.append(mood)
            except KeyError as e:
                raise KeyError(f"Missing column in CSV: {e}")
    return moods

def moods_to_emoji(moods: List[int]) -> str:
    """Convert a list of mood integers to an emoji string."""
    return "".join(MOOD_EMOJI[m] for m in moods)

def summarize(csv_path: str) -> str:
    """Read CSV and return emoji summary."""
    path = Path(csv_path)
    moods = read_mood_csv(path)
    return moods_to_emoji(moods)

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m src.mood_summary <path-to-csv>")
        sys.exit(1)
    try:
        result = summarize(sys.argv[1])
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
