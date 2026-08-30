# nightly-random-ansi-colorizer

A whimsical Bash utility that prints given text in a random ANSI color. Perfect for adding a splash of color to your terminal output.

## Usage

```sh
# Pipe input
echo "Hello, world!" | ./colorize.sh

# Or pass as argument
./colorize.sh "Hello, world!"
```

Each execution wraps the text in a random color from red, green, yellow, blue, magenta, cyan.

## Installation

Copy `src/colorize.sh` to a directory in your PATH and make it executable:

```sh
chmod +x src/colorize.sh
sudo mv src/colorize.sh /usr/local/bin/colorize
```

## How it works

The script selects a random color code using Bash's `$RANDOM` and wraps the input with ANSI escape sequences.

## License

MIT
