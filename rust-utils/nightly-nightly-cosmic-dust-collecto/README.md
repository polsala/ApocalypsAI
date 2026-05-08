# Nightly Cosmic Dust Collector

## Summary
`nightly-cosmic-dust-collector` is a whimsical-yet-useful high-performance CLI tool designed to help you manage the ephemeral files that accumulate on your system. It identifies old or large temporary files, cache entries, and logs – affectionately termed 'cosmic dust' – and allows you to either scan them or collect them into a compressed 'stardust archive' for later review or eventual disintegration.

Keep your digital cosmos tidy and prevent the accumulation of digital debris!

## Features
*   **Scan for Dust**: Quickly identify files matching age and size criteria.
*   **Collect Dust**: Archive identified 'cosmic dust' into a `.tar.gz` stardust archive.
*   **High Performance**: Built with Rust for speed and efficiency.

## Installation

To install `nightly-cosmic-dust-collector`, you need to have Rust and Cargo installed. If you don't, please visit [rustup.rs](https://rustup.rs/) for instructions.

Once Rust is set up, you can install the utility directly from source:

```bash
cargo install --path .
```

This will compile the `dust-collector` binary and place it in your Cargo bin directory (usually `~/.cargo/bin`), making it available in your PATH.

## Usage

The `dust-collector` command provides two main subcommands: `scan` and `collect`.

### `scan` - Identify Cosmic Dust

Use the `scan` subcommand to list files that meet your criteria for 'cosmic dust' without making any changes.

```bash
dust-collector scan [OPTIONS]
```

**Options:**
*   `-p, --path <PATH>`: The directory to scan. Defaults to the current directory (`.`).
*   `-a, --age <DAYS>`: Files older than this many days are considered dust. Defaults to `30` days.
*   `-s, --size-mb <MB>`: Files larger than this many megabytes are considered dust. Defaults to `10` MB.

**Example:**
Scan your home directory for files older than 60 days and larger than 50MB:
```bash
dust-collector scan -p ~/ -a 60 -s 50
```

### `collect` - Archive Stardust

Use the `collect` subcommand to gather the identified 'cosmic dust' into a compressed `.tar.gz` archive.

```bash
dust-collector collect [OPTIONS] --output <ARCHIVE_PATH>
```

**Options:**
*   `-p, --path <PATH>`: The directory to scan. Defaults to the current directory (`.`).
*   `-a, --age <DAYS>`: Files older than this many days are considered dust. Defaults to `30` days.
*   `-s, --size-mb <MB>`: Files larger than this many megabytes are considered dust. Defaults to `10` MB.
*   `-o, --output <ARCHIVE_PATH>`: **Required**. The path where the stardust archive (`.tar.gz`) will be created.

**Example:**
Collect all dust (older than 30 days, larger than 10MB) from `/var/log` into `~/stardust_archive.tar.gz`:
```bash
dust-collector collect -p /var/log -o ~/stardust_archive.tar.gz
```

## Development

To run tests:
```bash
cargo test
```

To build the project:
```bash
cargo build --release
```

## Contributing

Feel free to contribute to the Cosmic Dust Collector! Open issues for bugs or feature requests, or submit pull requests with improvements.
