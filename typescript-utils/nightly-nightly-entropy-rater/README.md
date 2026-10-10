# nightly-entropy-rater

Utility to estimate Shannon entropy of a given string and provide a whimsical rating with emojis.

## Installation

```sh
npm install -g nightly-entropy-rater
```

## Usage

```sh
npx nightly-entropy-rater "your secret"
# or
echo "your secret" | npx nightly-entropy-rater
```

Outputs something like:

```
Entropy: 3.21 bits/char
Rating: 🔥 (High)
```

## Rating scale

- 🟢 Low (≤1.5 bits/char)
- 🟡 Medium (1.5–3.0 bits/char)
- 🔥 High (>3.0 bits/char)

## Development

Run tests:

```sh
npm test
```
