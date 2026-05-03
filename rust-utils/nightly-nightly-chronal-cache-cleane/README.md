# Nightly Chronal Cache Cleaner

A whimsical Rust CLI tool that 'archives' old files from specified directories into a 'temporal void' instead of permanently deleting them.

## Purpose
In the digital wasteland, temporary files and forgotten caches accumulate like cosmic dust. The `nightly-chronal-cache-cleaner` doesn't just delete these echoes of the past; it gracefully escorts them to a designated 'temporal void' directory. This allows for a clean primary directory while keeping a historical archive, just in case you need to retrieve a forgotten artifact from the void.

## Features
*   **Whimsical Archiving**: Moves old files to a special 'temporal void' directory.
*   **Age-Based Cleaning**: Configurable age threshold (in days) for files to be considered 'old'.
*   **Custom Void Location**: Specify where your temporal void should reside, or let it default to `~/.chronal_void/`.
*   **Rust Performance**: Built with Rust for speed and reliability, ensuring your cache cleaning is swift and safe.

## Installation

To install `nightly-chronal-cache-cleaner`, you'll need Rust and Cargo installed. If you don't have them, visit [rustup.rs](https://rustup.rs/).

1.  Clone the repository (or navigate to this utility's directory):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-chronal-cache-cleaner
    ```
2.  Build and install:
    ```bash
    cargo install --path .
    ```
    This will install `chronal-cache-cleaner` to your Cargo bin directory (usually `~/.cargo/bin`), making it available in your PATH.

## Usage

Run the `chronal-cache-cleaner` command with the target directory and the age threshold.

```bash
chronal-cache-cleaner --target-dir <PATH_TO_SCAN> --age <DAYS_OLD> [--void-dir <PATH_TO_VOID>]
```

### Arguments:
*   `-t`, `--target-dir <PATH_TO_SCAN>`: **Required**. The directory to scan for old files.
*   `-a`, `--age <DAYS_OLD>`: **Required**. Files older than this many days will be moved to the temporal void.
*   `-v`, `--void-dir <PATH_TO_VOID>`: **Optional**. The directory where old files will be 'archived'. Defaults to `~/.chronal_void/`.

### Examples:

1.  Clean files older than 7 days from `/tmp/my_cache`, sending them to the default temporal void:
    ```bash
    chronal-cache-cleaner --target-dir /tmp/my_cache --age 7
    ```

2.  Archive files older than 30 days from `~/documents/old_projects` to a custom void location:
    ```bash
    chronal-cache-cleaner --target-dir ~/documents/old_projects --age 30 --void-dir /var/log/temporal_archive
    ```

## Development

To run tests:

```bash
cd ApocalypsAI/rust-utils/nightly-chronal-cache-cleaner
cargo test
```
