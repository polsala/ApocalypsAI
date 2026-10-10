# Nightly Passphrase Generator

A whimsical utility that creates memorable passphrases by combining emojis, words, and numbers. Perfect for adding a touch of fun to passwords, seed phrases, or secret codes.

## Installation

```sh
npm install -g nightly-passphrase-gen
```

## Usage

Run the command with no arguments to print a random passphrase:

```sh
npx nightly-passphrase-gen
# Example output: 🌞-sun-42-fox
```

You can also import the function in your TypeScript/JavaScript projects:

```ts
import { generatePassphrase } from 'nightly-passphrase-gen';
console.log(generatePassphrase());
```

## How it works

- Picks a random emoji from a curated list.
- Chooses two random lowercase words.
- Inserts a random number between 0 and 99.
- Joins them with hyphens.

The result is easy to read, type, and remember while still offering decent entropy for low‑risk scenarios.

## License

MIT
