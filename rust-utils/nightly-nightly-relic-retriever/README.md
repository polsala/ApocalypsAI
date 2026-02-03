# Nightly Relic Retriever

## Unearthing Temporal Echoes from the Wasteland

In the post-apocalyptic landscape of digital data, files often multiply like irradiated rodents, creating 'temporal echoes' – identical copies that clutter your precious storage. The `nightly-relic-retriever` is your trusty companion for identifying these duplicates, preserving the most pristine 'relic', and respectfully consigning its echoes to the 'void vault'.

This tool is built with Rust for blazing-fast performance, ensuring your data scavenging operations are as efficient as possible.

## Features

*   **High-Performance Scanning**: Rapidly traverses directories to find all files.
*   **SHA256 Hashing**: Uses robust cryptographic hashing to accurately identify identical file content.
*   **Duplicate Detection**: Pinpoints all 'temporal echoes' (duplicate files).
*   **Void Vault Archiving**: Moves identified duplicates (keeping the first encountered 'relic') into a designated 'void vault' directory, preventing accidental deletion while reclaiming space.
*   **Dry Run Mode**: Preview actions before committing to any changes.
*   **Whimsical Output**: Provides thematic messages to make your data cleanup a bit more enjoyable.

## Installation

To install `nightly-relic-retriever`, you'll need Rust and Cargo installed on your system. If you don't have them, visit [rust-lang.org](https://www.rust-lang.org/tools/install).

Once Rust is set up, run:

```bash
cargo install --path .
```

This will compile and install the `relic-retriever` executable to your Cargo bin directory (usually `~/.cargo/bin`). Make sure this directory is in your system's PATH.

## Usage

```bash
relic-retriever scan [OPTIONS] <PATH>
```

### Arguments

*   `<PATH>`: The directory to scan for relics (duplicate files).

### Options

*   `-a, --archive-path <ARCHIVE_PATH>`: The directory where temporal echoes will be moved. Defaults to `.void_vault` within the scanned path.
*   `-d, --dry-run`: Perform a dry run. No files will be moved, but the tool will report what it *would* do.
*   `-v, --verbose`: Enable verbose output.
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

### Examples

1.  **Scan current directory and archive duplicates to default `.void_vault` (dry run):**

    ```bash
    relic-retriever scan . --dry-run
    ```

2.  **Scan a specific directory and move duplicates to a custom archive path:**

    ```bash
    relic-retriever scan /path/to/scavenged/data --archive-path /path/to/my/temporal_archive
    ```

3.  **Scan with verbose output and commit changes:**

    ```bash
    relic-retriever scan ~/my_relics -v
    ```

## How it Works

1.  The tool recursively traverses the specified `<PATH>`.
2.  For each file encountered, it calculates its SHA256 hash.
3.  It groups files by their hash. If multiple files share the same hash, they are considered 'temporal echoes'.
4.  For each group of echoes, it designates the first file encountered as the 'primary relic' to keep.
5.  The remaining 'temporal echoes' are then moved to the specified `--archive-path` (or `.void_vault` by default). Each archived file is renamed to include its original path and a timestamp to prevent name collisions within the vault.

**Note**: The tool currently keeps the *first* encountered file as the primary relic. Future versions might offer options to keep the newest, oldest, or largest file.

## Development

To run tests:

```bash
cargo test
```

To build:

```bash
cargo build --release
```
