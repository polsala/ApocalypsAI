# nightly-ruin-decoder

Utility that translates a string of ancient runes (Unicode symbols) into plain English letters using a fixed substitution cipher. Handy for decoding secret messages in post‑apocalyptic notes.

## Installation

```sh
git clone <repo> && cd utils/nightly-ruin-decoder
node src/index.js --help
```

## Usage

```sh
node src/index.js "☀☁☂☃★✖✿♞♣♠"
# => abcdefghij
```

You can also pipe input:

```sh
echo "☀☁☂" | node src/index.js
```

## How it works

The tool maps ten rune symbols to the letters a‑j:

| Rune | Letter |
|------|--------|
| ☀   | a |
| ☁   | b |
| ☂   | c |
| ☃   | d |
| ★   | e |
| ✖   | f |
| ✿   | g |
| ♞   | h |
| ♣   | i |
| ♠   | j |

Any unknown character is left unchanged.

## Testing

```sh
npm test
```

(Tests are in `tests/test_index.js` and use Node's built‑in `assert`.)
