# Nightly Chrono-Sweep

A high-performance Rust CLI tool designed to help the ApocalypsAI community manage digital temporal debris. This utility identifies and optionally purges files that haven't been modified or accessed within a specified 'temporal epoch', ensuring your systems remain lean and free from forgotten data.

## Features

*   **Temporal Debris Identification**: Quickly scan directories for files older than a user-defined duration (e.g., 30 days, 2 weeks).
*   **High Performance**: Built with Rust for speed and efficiency, suitable for large file systems.
*   **Dry Run Mode**: Preview which files would be affected before any deletion occurs, preventing accidental purges.
*   **Recursive Scanning**: Traverses subdirectories to find all hidden temporal anomalies.
*   **Configurable Epochs**: Define durations using simple units like days (`d`), weeks (`w`), months (`m`), or years (`y`).

## Installation

To install `nightly-chrono-sweep`, you need to have Rust and Cargo installed. If you don't, visit [rustup.rs](https://rustup.rs/) for instructions.

Once Rust is set up, you can install the utility directly from crates.io (or build from source):

```bash
cargo install nightly-chrono-sweep
```

Alternatively, if you have the source code:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-chrono-sweep
cargo build --release
# The executable will be in target/release/nightly-chrono-sweep
# You might want to add it to your PATH or move it to a bin directory.
```

## Usage

```bash
nightly-chrono-sweep --help
```

### Basic Dry Run (Recommended First Step)

To see files in the current directory (and its subdirectories) that are older than 30 days, without deleting anything:

```bash
nightly-chrono-sweep -d 30d
```

To check a specific path, e.g., `/var/log/old_archives`, for files older than 2 weeks:

```bash
nightly-chrono-sweep -p /var/log/old_archives -d 2w
```

### Deleting Temporal Debris

**Use with extreme caution! Always perform a dry run first.**

To delete files older than 1 month in the current directory:

```bash
nightly-chrono-sweep -d 1m --delete
```

The tool will prompt for confirmation before proceeding with deletion. To bypass this prompt (e.g., for automation scripts), use the `--force` flag:

```bash
nightly-chrono-sweep -p /tmp/cache -d 1y --delete --force
```

### Duration Examples

*   `30d`: 30 days
*   `2w`: 2 weeks
*   `1m`: 1 month (approximately 30 days)
*   `1y`: 1 year (approximately 365 days)

## Development

To run tests:

```bash
cargo test
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
