# Daily Emoji Mood Tracker

A lightweight, zero‑dependency Python utility that lets you record your daily mood with an emoji (and an optional note) and then view a quick statistical summary.

## Features

- **Add** today’s mood with a single command.
- Stores data locally in a JSON file (`~/.emoji_mood_log.json` by default).
- **Stats** command prints how often each emoji was used and the total days logged.
- Fully self‑contained – no external services required.

## Installation

```bash
# Clone the repository (or copy the folder) and install the utility in a venv
python -m venv .venv
source .venv/bin/activate
pip install -e utils/daily-emoji-mood-tracker
```

The entry point is the `emoji-mood` script.

## Usage

```bash
# Add today’s mood (emoji) with an optional note
emoji-mood add 😊 -n "Feeling great!"

# Show statistics
emoji-mood stats
```

You can also specify a custom JSON file with `-f /path/to/file.json`.

## Testing

```bash
cd utils/daily-emoji-mood-tracker
python -m unittest discover -v
```

All tests run offline and use temporary files, so they are deterministic.
