# nightly-emoji-mood-tracker

A whimsical yet practical command‑line tool that lets you record your daily mood using an emoji and later query simple statistics.

## Features

- **Add** a mood entry for today (or any date) with a single emoji.
- **Summarize** the frequency of each emoji over a date range.
- Stores data locally in a JSON file (`~/.emoji_mood_tracker.json`).
- No external network calls – fully offline.

## Installation

Copy the folder `utils/nightly-emoji-mood-tracker` into your repository and run the script with Python 3.11:

```bash
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker --help
```

## Usage

```bash
# Add today's mood (defaults to today)
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker add 😄

# Add a mood for a specific date
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker add 2023-10-31 🎃

# Show a summary between two dates (inclusive)
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker summary 2023-10-01 2023-10-31
```

The summary prints a JSON‑like mapping of emoji → count.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/nightly-emoji-mood-tracker/tests
```

All tests are deterministic and use mocks; no network access is required.
