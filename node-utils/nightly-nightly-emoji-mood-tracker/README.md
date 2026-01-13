# nightly-emoji-mood-tracker

A tiny, whimsical commandâline utility that lets you record your mood as an emoji (with an optional note) and later view simple statistics.

## Install

```bash
# Clone the repo and install globally
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-emoji-mood-tracker
npm install -g .
```

## Usage

```bash
# Record a mood
emoji-mood log ð "Feeling great after lunch"

# List all entries
emoji-mood list

# Show statistics
emoji-mood stats
```

## Commands

- `log <emoji> [note]` â Append a new mood entry with the current timestamp.
- `list` â Print all recorded entries in chronological order.
- `stats` â Show how many times each emoji has been used.

All data is stored in a JSON file. By default it lives at `~/.emoji_mood_tracker.json`. You can override the location with the environment variable `EMOJI_MOOD_FILE`.

## Development

Run the test suite with:

```bash
npm test
```

The project uses only the Node standard library â no external dependencies.

