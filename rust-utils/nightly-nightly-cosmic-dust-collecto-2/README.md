# Nightly Cosmic Dust Collector

A high-performance CLI tool crafted in Rust to help you tidy up your digital cosmos by identifying and optionally archiving 'cosmic dust' – small, old, and potentially unused files – from specified directories.

## Features

*   **Efficient Scanning**: Recursively scans directories for files.
*   **Size Filtering**: Filters files based on a maximum size threshold.
*   **Age Filtering**: Filters files based on a minimum age (last modified time).
*   **Dry Run Mode**: Preview which files would be affected without making any changes.
*   **Archiving**: Move identified 'cosmic dust' to a specified 'void archive' directory.

## Installation

To install the `nightly-cosmic-dust-collector` CLI tool, you need to have Rust and Cargo installed. If you don't, visit [rustup.rs](https://rustup.rs/) for instructions.

```bash
cargo install nightly-cosmic-dust-collector
```

Alternatively, you can clone the repository and build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-cosmic-dust-collector
cargo build --release
# The executable will be found at target/release/nightly-cosmic-dust-collector
```

## Usage

```bash
nightly-cosmic-dust-collector --help
```

### Basic Scan (Dry Run)

Scan your current directory for files smaller than 100KB and older than 30 days, just listing them:

```bash
nightly-cosmic-dust-collector --path . --max-size 100 --min-age 30 --dry-run
```

### Scan and Archive

Scan a specific directory (`/var/log/old`) for files smaller than 50KB and older than 90 days, and move them to an archive directory (`~/void_archive`):

```bash
mkdir -p ~/void_archive
nightly-cosmic-dust-collector --path /var/log/old --max-size 50 --min-age 90 --archive-to ~/void_archive
```

### Arguments

*   `-p, --path <PATH>`: **(Required)** The root directory to start scanning from.
*   `-s, --max-size <KB>`: Maximum file size in kilobytes (KB). Files larger than this will be ignored. **Default: 100**.
*   `-a, --min-age <DAYS>`: Minimum age in days. Files modified more recently than this will be ignored. **Default: 30**.
*   `-o, --archive-to <DIR>`: Directory to move identified 'cosmic dust' files to. If not specified, files will only be listed.
*   `-d, --dry-run`: Perform a dry run. Files will be identified and listed, but no changes will be made to the file system. **Default: false**.

## Examples

1.  **Find all tiny, ancient files in your home directory (dry run):**
    ```bash
    nightly-cosmic-dust-collector --path ~/ --max-size 10 --min-age 365 --dry-run
    ```

2.  **Archive old temporary files from `/tmp` to a dedicated archive:**
    ```bash
    mkdir -p /var/void/tmp_archive
    nightly-cosmic-dust-collector --path /tmp --max-size 500 --min-age 7 --archive-to /var/void/tmp_archive
    ```

## Development

To run tests:

```bash
cargo test
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
