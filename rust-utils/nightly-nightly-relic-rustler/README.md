# Nightly Relic Rustler

A high-performance Rust CLI tool designed to help you identify and manage "digital relics" – old, unused files lurking in your file system. In the post-apocalyptic digital landscape, every byte counts! This tool scans specified directories, identifies files that haven't been modified in a long time, and lists them, allowing you to decide their fate.

## Features

*   **Fast Scanning**: Leverages Rust's performance for quick traversal of large directories.
*   **Configurable Age Threshold**: Define what constitutes an "old" file in days.
*   **Recursive Scan**: Automatically explores subdirectories to uncover hidden relics.
*   **Clear Output**: Provides a list of identified relics with their last modification dates.

## Installation

To install `nightly-relic-rustler`, you need to have Rust and Cargo installed. If you don't, visit [rust-lang.org](https://www.rust-lang.org/tools/install).

Once Rust is set up, you can install the utility directly from the source:

```bash
cargo install --path .
```

This will compile the tool and place the `nightly-relic-rustler` executable in your Cargo bin directory (usually `~/.cargo/bin`), making it available globally.

## Usage

Run the `nightly-relic-rustler` command with the target directory and an age threshold.

```bash
nightly-relic-rustler [OPTIONS]
```

### Options

*   `-p`, `--path <PATH>`: The directory to scan for relics. Defaults to the current directory (`.`).
*   `-a`, `--age-days <DAYS>`: The age threshold in days. Files older than this will be considered relics. Defaults to `90` days.

### Examples

1.  **Scan the current directory for files older than 90 days (default):**
    ```bash
    nightly-relic-rustler
    ```

2.  **Scan a specific directory (`/home/user/documents`) for files older than 180 days:**
    ```bash
    nightly-relic-rustler -p /home/user/documents -a 180
    ```

3.  **Scan a different directory (`/var/log/old_logs`) for files older than 30 days:**
    ```bash
    nightly-relic-rustler --path /var/log/old_logs --age-days 30
    ```

## Development

To build and run the project from source:

```bash
# Build the project
cargo build

# Run the project (e.g., scan current directory for files older than 60 days)
cargo run -- -p . -a 60

# Run tests
cargo test
```
