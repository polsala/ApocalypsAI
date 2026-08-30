# Nightly Digital Relic Hunt

Unearth the forgotten treasures and digital detritus lurking in your filesystem with the `nightly-digital-relic-hunt` tool! This high-performance Rust CLI helps you identify large, old, or potentially duplicate files, allowing you to reclaim precious storage space and declutter your digital catacombs.

## Features

*   **Fast Scanning**: Leverages Rust's performance for quick directory traversal.
*   **Size Filtering**: Find files larger than a specified threshold (e.g., 100MB, 1GB).
*   **Age Filtering**: Discover files older than a certain duration (e.g., 30 days, 1 year).
*   **Human-Readable Output**: Displays file sizes and modification times in an easy-to-understand format.

## Installation

To install `nightly-digital-relic-hunt`, you'll need [Rust and Cargo](https://www.rust-lang.org/tools/install) installed on your system.

```bash
cargo install --git https://github.com/polsala/ApocalypsAI --bin nightly-digital-relic-hunt
# Or, if you have the source locally:
cargo install --path . --bin nightly-digital-relic-hunt
```

This will compile and install the `nightly-digital-relic-hunt` executable to your Cargo bin directory (usually `~/.cargo/bin`). Make sure this directory is in your system's PATH.

## Usage

```bash
nightly-digital-relic-hunt [OPTIONS]
```

### Arguments

*   `-p, --path <PATH>`: Directory to scan for relics (default: current directory `.`)
*   `-s, --min-size <SIZE>`: Minimum size for a file to be considered a relic (e.g., `100M`, `1G`). Default is `0` (no minimum size).
*   `-a, --max-age <DURATION>`: Maximum age for a file to be considered a relic. Files *older* than this duration will be listed (e.g., `30d`, `1w`, `1y`).

### Examples

1.  **Find all files larger than 500MB in the current directory:**
    ```bash
    nightly-digital-relic-hunt --min-size 500M
    ```

2.  **Find all files older than 6 months in your documents folder:**
    ```bash
    nightly-digital-relic-hunt --path ~/Documents --max-age 180d
    ```

3.  **Find large, ancient relics (files older than 2 years and larger than 1GB) in a specific archive:**
    ```bash
    nightly-digital-relic-hunt --path /mnt/archive/old_projects --min-size 1G --max-age 2y
    ```

4.  **Scan your entire home directory for any file larger than 10GB:**
    ```bash
    nightly-digital-relic-hunt --path ~ --min-size 10G
    ```

## Contributing

Feel free to contribute to the ongoing digital archaeology efforts! Report bugs, suggest features, or submit pull requests to enhance the relic hunting capabilities.
