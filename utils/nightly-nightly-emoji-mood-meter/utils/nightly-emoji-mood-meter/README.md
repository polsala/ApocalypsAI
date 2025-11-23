# Nightly Emoji Mood Meter

A tiny utility that maps a calendar date to a single emoji representing the "mood" of that day. The mapping is deterministic, requires no external services, and is completely offline.

## Features
- Pure Python 3.11, no third‑party dependencies.
- Deterministic output: the same date always yields the same emoji.
- Simple CLI (`python -m mood_meter <YYYY-MM-DD>`).
- Easy to embed in scripts, CI pipelines, or commit messages.

## Usage
```bash
# As a module
python -m utils.nightly-emoji-mood-meter.src.mood_meter 2025-12-31
# => 🌟

# In code
from utils.nightly-emoji-mood-meter.src.mood_meter import get_mood
print(get_mood(date.today()))
```

## Implementation Details
The mood is selected from a fixed list of emojis. The index is derived from a simple hash of the ISO‑format date string (`int(hashlib.sha256(...).hexdigest(), 16) % len(EMOJIS)`). This ensures reproducibility across platforms.

## Testing
Run the test suite with:
```bash
python -m pytest utils/nightly-emoji-mood-meter/tests
```
