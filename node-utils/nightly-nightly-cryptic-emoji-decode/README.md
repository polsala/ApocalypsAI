# nightly-cryptic-emoji-decoder

A whimsical CLI utility that encodes and decodes messages using a secret emoji alphabet. Useful for adding a dash of mystery to notes, creating fun puzzles, or just impressing friends.

## Installation

```sh
# Clone the repository (or copy the utility into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-cryptic-emoji-decoder
npm install
```

> **Note**: This utility has no external runtime dependencies beyond the Node.js standard library.

## Usage

```sh
# Encode a plain‑text message into emojis
node src/index.js encode "HELLO"
# => 🐧🦁🐔🐔🦁

# Decode an emoji string back to plain text
node src/index.js decode "🐧🦁🐔🐔🦁"
# => HELLO
```

## Emoji Alphabet

| Emoji | Letter |
|-------|--------|
| 🐱   | C |
| 🐶   | D |
| 🦊   | F |
| 🐰   | R |
| 🐼   | P |
| 🦁   | L |
| 🐸   | A |
| 🐵   | M |
| 🐔   | E |
| 🐧   | N |

Only the letters shown above have emoji equivalents. All other characters are left unchanged during encoding/decoding.

## Running the Tests

```sh
node tests/test_index.js
```

If everything is correct you will see:

```
All tests passed
```
