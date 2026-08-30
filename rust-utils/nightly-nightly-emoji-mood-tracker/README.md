# nightly-emoji-mood-tracker

A whimsical command‑line utility to record your daily mood using emojis and retrieve simple statistics.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
# Add a mood entry
nightly-emoji-mood-tracker add 😊 "Feeling great after coffee"

# Show statistics
nightly-emoji-mood-tracker stats
```

The tool stores entries in `$HOME/.emoji_mood_tracker.json`.
