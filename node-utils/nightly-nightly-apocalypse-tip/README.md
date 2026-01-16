# nightly-apocalypse-tip

A whimsical CLI that delivers a random apocalypse survival tip, optionally fetched from an online advice API, with caching support.

## Features

- Random tip from a curated list of survival wisdom.
- Optional online tip via https://api.adviceslip.com/advice.
- Caches the last fetched tip for 24 hours to avoid excessive API calls.
- Cross‑platform (Windows, macOS, Linux).

## Usage

```bash
# Show a random local tip
node src/main.js

# Fetch a tip from the online API
node src/main.js --api

# Force refresh the cache even if it is still fresh
node src/main.js --api --force
```

## Installation

No installation required. Just run the script with Node 18+.

## License

MIT
