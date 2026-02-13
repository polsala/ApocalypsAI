# Nightly Emoji Clock

## Overview

`nightly-emoji-clock` is a tiny Node.js utility that converts a time into the nearest clock‑face emoji (🕐‑🕛).  It can be used in scripts, terminals, or anywhere you want a whimsical visual representation of a timestamp.

## Features

- Accepts an optional `HH:MM` argument (24‑hour format). If omitted, the current system time is used.
- Rounds to the nearest hour (minutes >= 30 round up).
- Works on any platform with Node.js (no external dependencies).

## Installation

```bash
# Clone the repository (or copy the utility folder) and install Node.js 14+.
# No npm packages are required.
```

## Usage

```bash
# Directly run the script
node src/index.js          # uses current time
node src/index.js 14:27    # => 🕑
node src/index.js 23:45    # => 🕛
```

The script prints the emoji to stdout.  Errors are printed to stderr and cause a non‑zero exit code.

## API

The module exports two functions for programmatic use:

- `parseTime(timeString)` – parses a `HH:MM` string into `{hour, minute}` and validates the input.
- `nearestClockEmoji(timeString?)` – returns the appropriate clock emoji.  If `timeString` is omitted, the current time is used.

```javascript
const {nearestClockEmoji} = require('./src/index');
console.log(nearestClockEmoji('09:30')); // 🕙
```

## Testing

Run the tests with Node (no test runner required):

```bash
node tests/test_index.js
```

All assertions must pass; the script exits with code 0 on success.

## License

MIT © ApocalypsAI
