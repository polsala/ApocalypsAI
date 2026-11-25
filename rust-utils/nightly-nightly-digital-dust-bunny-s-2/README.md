# Nightly Digital Dust Bunny Sweeper

## Summary

This high-performance CLI tool, crafted in Rust, helps you identify and optionally sweep away 'digital dust bunnies' – files that haven't been modified in a specified number of days. It can list these forgotten files or move them to a designated 'void archive' directory, helping you declutter your digital spaces with a touch of whimsy.

## Features

*   **Fast Scanning**: Leverages Rust's performance for quick directory traversal and metadata retrieval.
*   **Age-Based Identification**: Finds files older than a configurable number of days.
*   **Dry Run Mode**: Preview which files would be affected without making any changes.
*   **Void Archiving**: Optionally moves identified files to a specified archive directory.
*   **Whimsical Output**: Adds a bit of fun to the mundane task of file cleanup.

## Installation

To install the `nightly-digital-dust-bunny-sweeper`, you'll need Rust and Cargo installed on your system. If you don't have them, visit [rustup.rs](https://rustup.rs/) for instructions.

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-digital-dust-bunny-sweeper
    ```
2.  **Build and install:**
    ```bash
    cargo install --path .
    ```
    This will install the `nightly-digital-dust-bunny-sweeper` executable to your Cargo bin directory (usually `~/.cargo/bin`), making it available in your PATH.

## Usage

```bash
nightly-digital-dust-bunny-sweeper <PATH> --older-than <DAYS> [--archive-to <DIR>] [--dry-run]
```

### Arguments

*   `<PATH>`: The root directory to start scanning for dust bunnies.
*   `--older-than <DAYS>`: Required. Files with a last modification time older than this many days will be considered 'dust bunnies'. Must be 0 or greater.

### Options

*   `--archive-to <DIR>`: Optional. Specifies a directory where identified dust bunnies will be moved. If this option is omitted, files will only be listed, not moved.
*   `--dry-run`: Optional. If present, the tool will only list the files it *would* move, but won't actually perform any file system operations. This is highly recommended for testing your parameters before a real sweep.

## Examples

1.  **List all files in `/home/user/documents` older than 30 days (dry run):**
    ```bash
    nightly-digital-dust-bunny-sweeper /home/user/documents --older-than 30 --dry-run
    ```

2.  **Move files in `/tmp/downloads` older than 7 days to `/home/user/void-archive`:**
    ```bash
    nightly-digital-dust-bunny-sweeper /tmp/downloads --older-than 7 --archive-to /home/user/void-archive
    ```

3.  **List all files in the current directory (older than 0 days, effectively all files) without moving:**
    ```bash
    nightly-digital-dust-bunny-sweeper . --older-than 0
    ```

## Development

To run tests:

```bash
cargo test
```
