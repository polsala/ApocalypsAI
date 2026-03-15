# nightly-rot13-cli

A whimsical yet handy command‑line utility that applies the classic ROT13 cipher to text. Perfect for secret messages, puzzles, or just a bit of fun.

## Installation

```sh
npm install -g .
```

## Usage

```sh
# Encode a string
nrot13 "Hello World!"

# Or pipe input
echo "Secret Message" | nrot13
```

## How it works

The tool reads either the first command‑line argument or stdin, applies ROT13, and prints the result.

## License

MIT
