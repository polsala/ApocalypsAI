# Survival Kit Planner

A whimsical web tool to generate a postâapocalypse survival kit checklist based on your chosen environment (Desert, Tundra, Urban, Forest). Select an environment and click "Generate" to see a curated list of items.

## Usage

Open `src/index.html` in a web browser. No server is required.

## Development

The project uses **Jest** for unit testing. To run the tests:

```bash
npm install
npm test
```

## Files

- `src/index.html` â The main HTML page loading React via CDN.
- `src/kit.js` â Data module exporting environments and a helper function.
- `tests/kit.test.js` â Jest tests for the helper function.
- `package.json` â Minimal Node project definition (only Jest as a dev dependency).
