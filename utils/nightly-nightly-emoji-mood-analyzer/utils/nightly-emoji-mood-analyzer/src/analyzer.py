import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import List, Tuple, Dict

# Regex covering a broad set of emoji code points.
_EMOJI_PATTERN = re.compile(
    r"[\U0001F600-\U0001F64F"  # Emoticons
    r"\U0001F300-\U0001F5FF"   # Misc Symbols and Pictographs
    r"\U0001F680-\U0001F6FF"   # Transport & Map Symbols
    r"\U0001FA00-\U0001FA6F"   # Chess Symbols etc.
    r"\U0001FA70-\U0001FAFF"   # Symbols & Pictographs Extended-A
    r"\U00002702-\U000027B0"   # Dingbats
    r"\U000024C2-\U0001F251]"   # Enclosed characters
)


def extract_emojis(text: str) -> List[str]:
    """Return a list of all emoji characters found in *text*.

    The function uses a compiled regular expression that matches the most
    common emoji ranges. It deliberately avoids complex grapheme‑cluster
    handling to stay lightweight and deterministic.
    """
    return _EMOJI_PATTERN.findall(text)


def most_common_emojis(text: str) -> Tuple[List[str], Dict[str, int]]:
    """Return the emoji(s) with the highest frequency.

    Returns a tuple ``(most_common, counts)`` where ``most_common`` is a list of
    emoji characters that share the top count, and ``counts`` maps each of those
    emoji to its occurrence count.
    """
    emojis = extract_emojis(text)
    if not emojis:
        return [], {}
    counter = Counter(emojis)
    max_count = max(counter.values())
    most_common = [e for e, c in counter.items() if c == max_count]
    return most_common, {e: counter[e] for e in most_common}


def _run_cli() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze a text file and report the most frequent emoji(s)."
    )
    parser.add_argument(
        "filepath",
        type=Path,
        help="Path to a UTF‑8 encoded text file to analyze."
    )
    args = parser.parse_args()

    try:
        content = args.filepath.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"Error reading file: {exc}", file=sys.stderr)
        sys.exit(1)

    most_common, counts = most_common_emojis(content)
    result = {
        "most_common": most_common,
        "counts": counts,
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    _run_cli()
