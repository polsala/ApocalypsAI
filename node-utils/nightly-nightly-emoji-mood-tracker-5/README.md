# nightly-emoji-mood-tracker

A tiny, whimsical command‑line utility for tracking your mood with emojis.

## Features

- **Log a mood** – store an emoji, a short note, and a timestamp.
- **View stats** – see how many times each emoji has been logged.
- **Zero dependencies** – pure Node.js (requires Node 14+).

## Installation

```bash
# Clone the repository (or copy the utility folder into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-emoji-mood-tracker

# Make the script executable (optional)
chmod +x src/index.js
```

You can also install it globally if you wish:

```bash
npm install -g .
```

## Usage

```bash
# Add a mood entry
node src/index.js add "😊" "Feeling great after a coffee"

# Add a mood entry with a custom timestamp (useful for testing)
node src/index.js add "😔" "Rainy day" --timestamp 1609459200000

# Show statistics
node src/index.js stats
```

### Environment variable

- `DATA_FILE` – Path to the JSON file where entries are stored. Defaults to `mood_data.json` in the current working directory.

## Example

```bash
$ node src/index.js add "😊" "Good morning"
Logged mood.

$ node src/index.js add "😢" "Lost my keys"
Logged mood.

$ node src/index.js stats
😊: 1
😢: 1
```

## Testing

Run the test suite with:

```bash
npm test
```

The tests are deterministic and do not require network access.
