# nightly-emoji-mood-tracker

A tiny Node.js command‑line utility that lets you record your mood using emojis, add optional notes, and view quick statistics.

## Features

- **Add an entry** – store an emoji, an optional note, and a timestamp.
- **View stats** – see how many times each emoji has been logged.
- **List recent entries** – display the latest mood logs.
- Zero external dependencies – only built‑in Node modules.

## Installation

```bash
# Clone the repository (or copy the files into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-emoji-mood-tracker

# Install (optional, for global use)
npm install -g .
```

If you prefer not to install globally, you can run the script directly with Node:

```bash
node src/index.js <command> [options]
```

## Usage

### Add a mood entry

```bash
node src/index.js add 😊 "Feeling great after a walk"
```

The emoji is mandatory; the note is optional.

### Show statistics

```bash
node src/index.js stats
```

Outputs a count of each emoji logged.

### List recent entries

```bash
node src/index.js list 5
```

Shows the most recent 5 entries (default is 10 if no number is supplied).

## Data storage

Entries are stored in a JSON file located at `~/.emoji_mood_tracker.json`. The file is created automatically on the first run.

## Testing

Run the test suite with:

```bash
npm test
```

The tests use a temporary directory to avoid touching your real data file.

---

Enjoy tracking your emotional weather, one emoji at a time! 🌦️😊
