# nightly-emoji-mood-tracker

A tiny, whimsical command‑line utility that lets you record your mood as an emoji and later see simple stats.

## Features

- Log a mood with a single emoji (`node src/index.js add 😊`).
- Store entries locally in a JSON file (`mood_data.json`).
- Show total entries and the most common emoji (`node src/index.js stats`).
- Pure Node.js, no external dependencies.

## Installation

```bash
# Clone the repository (or copy the utility folder) and install (optional)
npm install
```

> The utility works out‑of‑the‑box; the `npm install` step is only needed if you want to add it to a larger project.

## Usage

```bash
# Add a mood entry (replace the emoji with whatever you feel)
node src/index.js add 😊

# View statistics
node src/index.js stats
```

The data is stored in `mood_data.json` next to the utility.  You can also provide a custom path when using the library functions (see the API section).

## API (for developers)

```js
const { addEntry, getStats } = require('./src/index');

// Add an entry – you can pass a Date object and an optional custom data file path
addEntry('😎', new Date(), '/tmp/my_mood.json');

// Retrieve stats
const stats = getStats('/tmp/my_mood.json');
console.log(stats); // { total: 1, topEmoji: '😎' }
```

## Testing

```bash
node tests/test_index.js
```

All tests should pass and output `All tests passed`.
