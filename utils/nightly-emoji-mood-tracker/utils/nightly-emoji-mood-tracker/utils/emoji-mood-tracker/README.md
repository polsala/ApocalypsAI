# Emoji Mood Tracker

A tiny CLI utility to log your daily mood using emojis and view a summary chart. Stores data in a local JSON file (`~/.emoji_mood_tracker.json`). Useful for personal reflection.

## Features

- `add <emoji>` – Record today's mood.
- `summary` – Show how many times each emoji was used.
- `chart` – Display a simple text bar chart of mood frequencies.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install .
```

## Usage

```bash
python -m src.mood_tracker add 😊
python -m src.mood_tracker summary
python -m src.mood_tracker chart
```

## Data location

The utility stores data in `~/.emoji_mood_tracker.json`. The file is created on first use.
