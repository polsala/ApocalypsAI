# Apocalypse Moodboard

A tiny React web app that displays a daily "survival mood" with a whimsical phrase and matching background color. Refresh to get a new mood, or wait for the next day. Perfect for adding a splash of postâapocalyptic optimism to your browser.

## Usage

```bash
npm install
npm start
```

## How it works

The app selects a mood based on the current date (YYYYâMMâDD) using a deterministic hash, ensuring the same mood is shown throughout the day for all users. The mood list is defined in `src/moodData.js`.

## Testing

```bash
npm test
```

## License

MIT
