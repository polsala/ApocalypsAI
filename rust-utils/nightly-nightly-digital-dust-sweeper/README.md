# Nightly Digital Dust Bunny Sweeper

A high-performance CLI tool written in Rust to help you sweep away digital "dust bunnies" – stale, unused, or forgotten files – from your file system. It identifies files older than a specified number of days (based on their last modification time) and offers options for a dry run or actual deletion.

## Features

*   **Efficient Scanning**: Utilizes `walkdir` for fast and recursive directory traversal.
*   **Age-Based Filtering**: Easily target files older than a configurable number of days.
*   **Dry Run Mode**: Preview which files would be affected before making any changes.
*   **Safe Deletion**: Explicit `--delete` flag required for actual file removal, preventing accidental data loss.
*   **Performance**: Built with Rust for speed and memory safety, ideal for large file systems.

## Installation

To install `nightly-digital-dust-sweeper`, you'll need Rust and Cargo installed. If you don't have them, you can get them from [rustup.rs](https://rustup.rs/).

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    # If cloning the whole ApocalypsAI repo
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-digital-dust-sweeper
    ```
    (Assuming this utility will be placed under `rust-utils/nightly-digital-dust-sweeper`)

2.  **Build the project:**
    ```bash
    cargo build --release
    ```
    This will compile the utility and place the executable in `target/release/`.

3.  **Add to your PATH (optional, but recommended):**
    You can move the executable to a directory in your system's PATH, e.g., `/usr/local/bin` or `~/.cargo/bin`.
    ```bash
    cp target/release/nightly-digital-dust-sweeper /usr/local/bin/
    ```

## Usage

```bash
nightly-digital-dust-sweeper [OPTIONS] --path <PATH>
```

### Arguments

*   `-p`, `--path <PATH>`: **Required**. The directory to scan for dust bunnies.
*   `-a`, `--age-days <DAYS>`: Files older than this many days (based on last modification time) are considered dust bunnies. Defaults to `30`.
*   `-d`, `--dry-run`: Perform a dry run: list files that would be deleted without actually deleting them.
*   `-D`, `--delete`: **Use with caution!** Actually delete the identified dust bunnies. This flag is mutually exclusive with `--dry-run`.

### Examples

1.  **Scan your home directory for files older than 60 days (dry run):**
    ```bash
    nightly-digital-dust-sweeper -p ~/ -a 60 --dry-run
    ```

2.  **List all files older than 7 days in a specific project directory (no action):**
    ```bash
    nightly-digital-dust-sweeper --path /var/log/old_archives --age-days 7
    ```
    (This will only print what it finds, no deletion or dry-run message for each file, just a summary)

3.  **Actually delete files older than 90 days in a temporary directory:**
    ```bash
    nightly-digital-dust-sweeper -p /tmp/old_temp_files -a 90 --delete
    ```
    **WARNING**: Always use `--dry-run` first to understand what will be deleted!

## Development

### Running Tests

To run the automated tests:

```bash
cargo test
```

### Project Structure

```
.
├── Cargo.toml          # Rust project manifest and dependencies
├── README.md           # This file
├── src/
│   └── main.rs         # Main application logic
└── tests/
    └── test_main.rs    # Integration tests for the utility
```
