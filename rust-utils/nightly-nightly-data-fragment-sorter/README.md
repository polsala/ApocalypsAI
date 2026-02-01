# Nightly Data Fragment Sorter

A high-performance Rust CLI tool designed for the ApocalypsAI community to scan directories, categorize data fragments, and identify duplicates for post-apocalyptic data recovery and organization. Think of it as your digital dust bunny sweeper, tidying up the scattered remnants of information.

## Features

*   **Recursive Directory Scanning**: Efficiently traverses specified directories.
*   **Fragment Categorization**: Sorts files into logical "survival caches" based on:
    *   `large_files`: Files exceeding a configurable size threshold.
    *   `recent_files`: Files modified within a configurable number of days.
    *   `empty_files`: Files with zero bytes.
    *   `duplicate_files`: Identifies exact duplicates using SHA256 hashing.
    *   `other_fragments`: Files that don't fit other categories.
    *   `error_fragments`: Files that couldn't be processed (e.g., permission issues).
*   **Duplicate Detection**: Uses SHA256 hashes to reliably find identical files, reporting the path to the original.
*   **Move or Copy**: Option to either move files to their categorized directories or copy them, leaving originals intact.
*   **Performance**: Written in Rust for speed and efficiency, ideal for large datasets.

## Installation

Ensure you have Rust and Cargo installed. If not, follow the instructions at [rustup.rs](https://rustup.rs/).

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    # Assuming you are in the root of the ApocalypsAI repository
    cd rust-utils/nightly-data-fragment-sorter
    ```
2.  **Build and install:**
    ```bash
    cargo install --path .
    ```
    This will install `nightly-data-fragment-sorter` as a command-line tool available in your path.

## Usage

```bash
nightly-data-fragment-sorter --help
```

```
Scans directories for data fragments, categorizes them, and identifies duplicates.

Usage: nightly-data-fragment-sorter [OPTIONS] --source-dir <PATH> --output-dir <PATH>

Options:
  -s, --source-dir <PATH>
          The directory to scan for data fragments.
  -o, --output-dir <PATH>
          The directory where categorized fragments will be moved/copied.
      --min-large-size <MIN_LARGE_SIZE>
          Minimum file size (bytes) to be considered 'large'. [default: 1048576]
      --recent-days <RECENT_DAYS>
          Number of days for a file to be considered 'recent'. [default: 7]
  -m, --mv
          If true, files will be moved; otherwise, they will be copied.
  -h, --help
          Print help (see a summary with '-h')
  -V, --version
          Print version
```

### Examples

1.  **Scan a directory and copy files to a new output structure:**
    ```bash
    nightly-data-fragment-sorter -s /path/to/your/wasteland_data -o /path/to/your/survival_cache
    ```
    This will create subdirectories like `/path/to/your/survival_cache/large_files`, `/path/to/your/survival_cache/recent_files`, etc., and copy files into them.

2.  **Scan and move files, considering files over 5MB as large and files from the last 30 days as recent:**
    ```bash
    nightly-data-fragment-sorter -s /path/to/old_archives -o /path/to/sorted_archives --min-large-size 5242880 --recent-days 30 -m
    ```

3.  **Just scan and report without moving/copying (default behavior if `-m` is not used):**
    The tool will still create the output directories and attempt to copy files by default. If you want to *only* scan and report without any file operations, you would need to modify the tool to have a dry-run option. For now, it performs the copy operation by default.

## Output Structure

The `output_dir` will contain subdirectories for each category:

```
survival_cache/
├── large_files/
│   ├── huge_log.txt
│   └── old_backup.zip
├── recent_files/
│   ├── today_report.csv
│   └── new_config.json
├── empty_files/
│   └── placeholder.txt
├── duplicate_files/
│   # Note: Duplicates are logged but not moved/copied by default to avoid redundant storage.
│   # The log will indicate which file is a duplicate and its original.
├── other_fragments/
│   ├── small_image.jpg
│   └── old_document.pdf
└── error_fragments/
    └── unreadable_file.bin
```

## Development

To run tests:

```bash
cargo test
```

To run the linter and formatter:

```bash
cargo fmt --check
cargo clippy -- -D warnings
```
