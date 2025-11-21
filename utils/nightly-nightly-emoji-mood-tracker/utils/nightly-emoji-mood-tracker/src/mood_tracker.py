"""emoji_mood_tracker – map textual moods to emojis.

The module provides a simple CLI (`python -m emoji_mood_tracker <mood>`) and a programmatic API:

```python
from emoji_mood_tracker import mood_to_emoji
emoji = mood_to_emoji("tired")
```

The default mapping is deterministic and offline. Custom mappings can be supplied via a JSON file
(`{"happy": "😊", ...}`) using the `--custom` flag.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict

# Default mood‑to‑emoji mapping – whimsical yet useful
DEFAULT_MAPPING: Dict[str, str] = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "excited": "🤩",
    "productive": "🚀",
    "tired": "😴",
    "confused": "🤔",
    "love": "❤️",
    "celebrate": "🥳",
    "bored": "😐",
}

def load_custom_mapping(path: Path) -> Dict[str, str]:
    """Load a JSON mapping file.

    The JSON must be an object where keys are lower‑cased mood strings and values are single‑character emojis.
    """
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("Custom mapping JSON must be an object")
        # Normalise keys to lower case
        return {k.lower(): v for k, v in data.items()}
    except Exception as exc:
        raise ValueError(f"Failed to load custom mapping from {path}: {exc}") from exc

def merge_mappings(base: Dict[str, str], custom: Dict[str, str]) -> Dict[str, str]:
    """Merge custom mapping over the base mapping, preferring custom entries."""
    merged = base.copy()
    merged.update(custom)
    return merged

def mood_to_emoji(mood: str, mapping: Dict[str, str] | None = None) -> str:
    """Return the emoji for *mood*.

    Parameters
    ----------
    mood: str
        Human‑readable mood description (case‑insensitive).
    mapping: optional dict
        Custom mapping to use instead of the default.
    """
    if mapping is None:
        mapping = DEFAULT_MAPPING
    key = mood.strip().lower()
    return mapping.get(key, "❓")  # Unknown moods get a question‑mark emoji

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Translate a mood into an emoji.")
    parser.add_argument("mood", help="Textual mood description, e.g. 'happy' or 'productive'.")
    parser.add_argument(
        "--custom",
        type=Path,
        help="Path to a JSON file with custom mood→emoji mappings.",
    )
    return parser

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    mapping = DEFAULT_MAPPING
    if args.custom:
        # Mock rationale: loading custom mapping is deterministic because the file is local.
        try:
            custom = load_custom_mapping(args.custom)
            mapping = merge_mappings(DEFAULT_MAPPING, custom)
        except ValueError as e:
            print(e, file=sys.stderr)
            return 1

    emoji = mood_to_emoji(args.mood, mapping)
    print(emoji)
    return 0

if __name__ == "__main__":
    sys.exit(main())
