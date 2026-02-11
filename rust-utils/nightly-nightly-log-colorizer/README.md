# Nightly Log Colorizer

A tiny Rust command‑line tool that reads a log file (or standard input) and prints the same lines with ANSI colours based on common severity keywords.

## Features

- Detects `ERROR`, `WARN`, and `INFO` tokens in each line.
- Colours:
  - **ERROR** → bright red
  - **WARN**  → bright yellow
  - **INFO**  → bright green
- Pass a file path as an argument or pipe data via stdin.
- No external runtime dependencies – just a single binary.

## Installation

```bash
# Clone the repository (or let the ApocalypsAI bot add it)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/rust-utils/nightly-log-colorizer

# Build the binary
cargo build --release
```

The compiled binary will be located at `target/release/nightly-log-colorizer`.

## Usage

```bash
# Colourise a file
cargo run --quiet -- path/to/log.txt

# Or pipe data
cat log.txt | cargo run --quiet
```

## Example

```text
$ echo -e "INFO Starting\nWARN Low disk\nERROR Crash\nNormal line" | cargo run --quiet
\x1b[32mINFO Starting\x1b[0m
\x1b[33mWARN Low disk\x1b[0m
\x1b[31mERROR Crash\x1b[0m
Normal line
```

The escape sequences (`\x1b[31m`, etc.) are interpreted by most terminals to display coloured text.

## Testing

Run the test suite with:

```bash
cargo test
```

The tests verify that the correct ANSI codes are emitted for each severity level.
