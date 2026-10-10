# nightly-ansi-gradient

A tiny Rust CLI that prints given text with a rainbow ANSI color gradient. Useful for spicing up terminal output, logs, or commit messages.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
ansi-gradient "Hello, world!"
```

The command prints the supplied text with a smooth rainbow gradient using ANSI escape codes.

## How it works

The program cycles through a predefined list of ANSI color codes (red, yellow, green, blue, magenta) and wraps each character in the appropriate code. The final reset code (`\x1b[0m`) restores the terminal's default colors.

## License

MIT
