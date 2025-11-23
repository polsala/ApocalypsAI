# Nightly Emoji Mood Tracker

## Overview

`nightly-emoji-mood-tracker` is a tiny, self‑contained Python utility that maps any calendar date to a **mood emoji**. The mapping is **deterministic** – the same date always yields the same emoji – and requires no external services or network access.

## Why?

* Add a whimsical touch to daily stand‑up notes.
* Keep a lightweight personal journal with a visual mood indicator.
* Use in CI logs to give each run a unique, friendly symbol.

## Installation & Usage

```bash
# Clone the repository (or copy the folder) and install the utility's dependencies (none beyond the stdlib).
python -m venv .venv && source .venv/bin/activate
pip install -e utils/nightly-emoji-mood-tracker
```

```bash
# Get today's mood emoji
python -m nightly_emoji_mood_tracker

# Or ask for a specific date (ISO format)
python -m nightly_emoji_mood_tracker 2025-12-01
```

## API

```python
from nightly_emoji_mood_tracker import get_mood_emoji

emoji = get_mood_emoji(date)  # `date` is a datetime.date instance
```

## Testing

Run the bundled tests with:

```bash
pytest utils/nightly-emoji-mood-tracker/tests
```

## License

MIT – see the root `LICENSE` file.
