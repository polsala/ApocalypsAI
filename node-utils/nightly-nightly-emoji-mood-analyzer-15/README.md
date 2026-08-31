# nightly-emoji-mood-analyzer

A tiny Node.js utility that reads a short piece of text and returns an emoji that best matches the mood. Useful for adding a quick emotional cue to logs, chat bots, or commit messages.

## Installation

```sh
npm install -g nightly-emoji-mood-analyzer
```

## Usage

```sh
emoji-mood "I just finished the marathon!"
# => 🏃‍♂️
```

If installed locally, run with npx:

```sh
npx nightly-emoji-mood-analyzer "Feeling sad about the rain."
# => 😢
```

## How it works

The tool looks for keywords associated with a handful of moods and picks the first matching emoji. If no keywords are found, it returns a neutral face 🤔.
