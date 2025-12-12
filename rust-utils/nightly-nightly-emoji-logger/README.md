# nightly-emoji-logger

A whimsical CLI that prefixes each input line with a random emoji, turning plain logs into a colorful stream.

## Usage

```bash
# Read from a file
nightly-emoji-logger log.txt

# Read from stdin
cat log.txt | nightly-emoji-logger
```

## Options

- `-h, --help` Show help.

## Example

```bash
$ echo -e "INFO: Starting\nWARN: Low disk space\nERROR: Failed to connect" | nightly-emoji-logger
🚀 INFO: Starting
🌟 WARN: Low disk space
💥 ERROR: Failed to connect
```

## Installation

Compile with Cargo:

```bash
cargo build --release
```

Copy the binary to your PATH.

## License

MIT
