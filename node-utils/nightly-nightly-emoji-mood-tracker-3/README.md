# nightly-emoji-mood-tracker

A tiny, whimsical CLI utility for tracking your mood with emojis.

## Features

- Log a mood entry with an emoji and an optional note.
- Store entries locally in a JSON file (default: `./mood.json`).
- Retrieve a summary that counts how many times each emoji was used.

## Installation

```bash
# Clone the repository (or copy the utility folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-emoji-mood-tracker

# Install (no external deps required)
npm install
```

## Usage

The utility can be invoked via Node:

```bash
# Log a mood
node src/index.js log "ð" "Feeling great after a coffee"

# Log another mood (no note)
node src/index.js log "ð"

# Show summary
node src/index.js summary
```

### Environment variable

You can override the storage file by setting `MOOD_FILE`:

```bash
MOOD_FILE=/tmp/my_mood.json node src/index.js log "ð¤"
```

## API (for developers)

The module exports two async functions you can require in your own code:

- `logMood(emoji, note)` â adds a new entry.
- `getSummary()` â returns an object mapping emojis to counts.

Both functions return Promises.

## Testing

Run the test suite with Node (no test runner required):

```bash
node tests/test_index.js
```

The tests are deterministic and use a temporary file via the `MOOD_FILE` env var.

## License

MIT â see LICENSE file in the repository root.

