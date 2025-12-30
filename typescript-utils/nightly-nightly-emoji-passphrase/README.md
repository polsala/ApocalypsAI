# nightly-emoji-passphrase

Generate memorable passphrases mixing words and emojis for extra security and fun.

## Installation

```sh
npm install -g nightly-emoji-passphrase
```

Or run without installing:

```sh
npx nightly-emoji-passphrase
```

## Usage

```sh
npx nightly-emoji-passphrase [options]
```

### Options

- `-l, --length <number>` – Number of words (default: 4)
- `-d, --delimiter <string>` – Delimiter between tokens (default: space)
- `-e, --emoji` – Replace words with their emoji equivalents

## Example

```sh
npx nightly-emoji-passphrase -l 3 -d - -e
# Output: 🅰️-🥦-🐱
```
