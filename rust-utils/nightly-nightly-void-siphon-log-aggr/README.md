# nightly-void-siphon-log-aggregator

A terminal-based log aggregator that siphons logs from multiple sources, filters them by severity, and displays them with ANSI colorization.

## Features

- Aggregate logs from multiple files or stdin
- Filter by log level (ERROR, WARN, INFO, DEBUG)
- Colorized terminal output
- Whimsical void-themed styling

## Usage

```sh
void-siphon [OPTIONS] [FILES]...
```

### Examples

```sh
# Read from multiple files
void-siphon app.log error.log

# Read from stdin
cat app.log | void-siphon

# Filter by log level
void-siphon --level ERROR app.log
```

## Options

- `-l, --level <LEVEL>`: Filter logs by level (ERROR, WARN, INFO, DEBUG)
- `-h, --help`: Display help information

## Installation

```sh
cargo build --release
./target/release/void-siphon
```
