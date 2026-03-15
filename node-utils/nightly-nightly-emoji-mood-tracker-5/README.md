# nightly-emoji-mood-tracker

A whimsical CLI tool to record your mood with an emoji and a short note. It stores entries locally and can show a summary of how many times each emoji was used.

## Installation

```sh
npm install -g .
```

## Usage

```sh
# Add a mood entry
emoji-mood add 😊 "Feeling great after lunch"

# List all entries
emoji-mood list

# Show summary
emoji-mood summary
```

## How it works

The tool stores data in a JSON file (default `~/.emoji_mood_tracker.json`). You can override the location with the `EMOJI_MOOD_FILE` environment variable.
