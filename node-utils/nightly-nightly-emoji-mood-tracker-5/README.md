# nightly-emoji-mood-tracker

A whimsical CLI utility to log your mood with an emoji and view simple statistics.

## Installation

```sh
npm install -g .
```

## Usage

Add a mood entry:

```sh
node src/index.js add "happy" 😊
```

List all entries:

```sh
node src/index.js list
```

Show statistics (most common mood, total entries):

```sh
node src/index.js stats
```

The data is stored in a JSON file at `~/.emoji_mood_log.json` (or the path set by the `EMOJI_MOOD_LOG_PATH` environment variable).

## License

MIT
