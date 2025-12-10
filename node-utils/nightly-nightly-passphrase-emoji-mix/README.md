# nightly-passphrase-emoji-mixer

Generate a whimsical yet memorable passphrase composed of random words and emojis. Useful for creating memorable passwords or secret codes.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/main.js
# or after global install:
passphrase-emoji-mixer
```

Outputs something like:

```
sunny river mountain coffee 🌟🚀
```

## How it works

- Picks 4 random words from an internal list.
- Picks 2 random emojis from an emoji list.
- Uses `crypto.randomInt` for randomness; can be overridden with the `FAKE_RANDOM` environment variable for testing.

## Testing

```sh
npm test
```
