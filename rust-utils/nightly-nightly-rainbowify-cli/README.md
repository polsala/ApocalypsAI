# nightly-rainbowify-cli

Utility that prints text with a rainbow ANSI color gradient, similar to `lolcat`. Useful for adding flair to terminal output.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
# From a pipe
echo "Hello, world!" | nightly-rainbowify-cli

# Direct argument
nightly-rainbowify-cli "Apocalypse is near!"
```

## How it works

The tool cycles through six ANSI colors (red, yellow, green, cyan, blue, magenta) and wraps each character in the appropriate escape sequence.
