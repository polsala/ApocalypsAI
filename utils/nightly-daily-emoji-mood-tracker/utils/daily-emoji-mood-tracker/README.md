# Daily Emoji Mood Tracker

A whimsical yet practical CLI utility that lets you record your daily mood with an emoji and retrieve a summary of the past week.

## Features

- `log <emoji> <optional note>` – Append today's mood.
- `summary` – Show count of each emoji for the last 7 days.
- Stores data in a local JSON file (`~/.emoji_mood_log.json`).

## Usage

```bash
python -m emoji_mood_tracker.tracker log 😊 "Feeling great"
python -m emoji_mood_tracker.tracker summary
```

## Installation

Just run the script; no external dependencies.
