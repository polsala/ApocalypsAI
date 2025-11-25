# Nightly Emoji Mood Tracker

A whimsical yet practical command‑line tool for tracking your emotional weather.

## Features
- Log a mood for *today* (or any date) using a single emoji, e.g. `😊`, `😢`, `🤯`.
- Optional free‑form note attached to each entry.
- Store data locally in a tiny JSON file (`~/.emoji_mood_log.json`).
- Retrieve a human‑readable summary of the last *N* days.

## Installation
The utility is pure Python 3.11 – just copy the `src/` folder into your `$PATH` or install it as a module.
```bash
python -m pip install --user .
```
*(The repository already contains a `pyproject.toml`‑compatible layout, but the utility works without any extra dependencies.)*

## Usage
```bash
# Add today's mood (emoji required, note optional)
python -m mood_tracker add 😊 "Feeling great after the morning run"

# Add a mood for a specific date (YYYY‑MM‑DD)
python -m mood_tracker add 2025-11-20 😴 "Slept poorly"

# Show a summary of the last 7 days
python -m mood_tracker summary 7
```

## Development
Run the test suite with:
```bash
python -m pytest utils/nightly-emoji-mood-tracker/tests
```

---
*Built by the ApocalypsAI Nightly Integrator – because even the end of the world needs a mood check.*
