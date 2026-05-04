# Nightly Digital Decay Detector

## Summary

The `nightly-digital-decay-detector` is a whimsical-yet-useful command-line interface (CLI) tool crafted in Rust. It helps you unearth "digital dust bunnies" and "temporal echoes" by scanning specified directories for files that haven't been modified in a long, long time. Think of it as an archaeological dig for your file system, revealing the forgotten relics of your digital past.

## Usage

```bash
nightly-digital-decay-detector <PATH> --age <DURATION>
```

- `<PATH>`: The directory to scan recursively for decaying files.
- `--age <DURATION>`: The minimum age a file must be (since last modification) to be considered "decaying".

### Duration Formats

The `DURATION` can be specified using a number followed by a unit:
- `s`: seconds (e.g., `60s` for 60 seconds)
- `m`: minutes (e.g., `30m` for 30 minutes)
- `h`: hours (e.g., `24h` for 24 hours)
- `d`: days (e.g., `7d` for 7 days)
- `w`: weeks (e.g., `2w` for 2 weeks)

### Examples

Scan the current directory for files older than 30 days:
```bash
nightly-digital-decay-detector . --age 30d
```

Scan a specific project directory for files older than 1 year (52 weeks):
```bash
nightly-digital-decay-detector /path/to/my/old/project --age 52w
```

## Installation

To install the `nightly-digital-decay-detector`, ensure you have Rust and Cargo installed. Then, navigate to the utility's directory and run:

```bash
cargo install --path .
```

This will install the `nightly-digital-decay-detector` executable to your Cargo bin directory, usually `~/.cargo/bin`.

## Development

To build and run from source:

```bash
cargo build
cargo run -- /path/to/scan --age 30d
```

## Tests

To run the automated tests:

```bash
cargo test
```

The tests are deterministic and offline, using temporary files with controlled modification times to simulate various scenarios.
