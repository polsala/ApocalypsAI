# nightly-emoji-mood-tracker

A tiny, whimsical command‑line utility written in Node.js that lets you record your mood using emojis and later view a quick statistical summary.

## Features

- **Add a mood**: `nmt add <emoji>` stores the current date and the emoji you provide.
- **Show stats**: `nmt stats` prints how many times each emoji has been logged.
- Zero‑dependency runtime (only built‑in Node modules).
- Works on any platform that has Node >=14.

## Installation

```bash
# Clone the repository (or copy the folder into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-emoji-mood-tracker

# Install the tiny test runner (Jest) locally
npm install
```

## Usage

```bash
# Add a mood (e.g., happy face)
node src/index.js add "😊"

# Add another mood (e.g., tired face)
node src/index.js add "😴"

# Show statistics
node src/index.js stats
```

The data is stored in a hidden JSON file in your home directory: `~/.emoji_mood_log.json`.

## Testing

```bash
npm test
```

The test suite uses Jest with mocked `fs` and `console` objects, so it runs completely offline.

## License

MIT © ApocalypsAI community
