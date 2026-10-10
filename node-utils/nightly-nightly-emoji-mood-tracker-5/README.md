# nightly-emoji-mood-tracker

A whimsical CLI utility to log your daily mood with an emoji and view simple statistics.

## Installation

```sh
npm install -g .
```

## Usage

Add a mood:

```sh
node src/index.js add happy
```

Show stats:

```sh
node src/index.js stats
```

Supported moods: happy, sad, angry, excited, neutral.

## How it works

Entries are stored in a JSON file in your home directory (`~/.emoji_mood_log.json`). Each entry contains a timestamp, the mood string, and its corresponding emoji.
