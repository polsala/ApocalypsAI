# Nightly Resource Scavenger

`nightly-resource-scavenger` is a whimsical-yet-useful command-line utility designed to help you reclaim digital wasteland by identifying forgotten, dusty, or ephemeral files on your file system. It scans specified directories and generates a 'Scavenger Report' categorizing files based on their age, size, and type, offering insights for potential cleanup or archiving.

## Features

*   **Directory Scanning**: Recursively scans a target directory for files.
*   **Age-based Classification**: Identifies 'Forgotten Relics' (files older than a specified number of days).
*   **Size-based Classification**: Flags 'Significant' files (larger than a specified size).
*   **Type-based Classification**: Recognizes 'Ephemeral Scraps' (common temporary or log files).
*   **Whimsical Report**: Presents findings in a themed, easy-to-read format.
*   **Safe**: Only reports findings; never deletes or modifies files.

## Installation

To install `nightly-resource-scavenger`, you'll need the Rust toolchain installed. If you don't have it, you can get it from [rustup.rs](https://rustup.rs/).

1.  Clone the `polsala/ApocalypsAI` repository (or navigate to this utility's directory).
2.  Build and install using Cargo:

    ```bash
    cargo install --path .
    ```

    This will make the `nightly-resource-scavenger` command available in your shell.

## Usage

Run the scavenger with the target directory and optional criteria:

```bash
nightly-resource-scavenger [OPTIONS]
```

### Arguments

*   `-p, --path <PATH>`: Directory to scavenge. Defaults to the current directory (`.`).
*   `-m, --max-age-days <DAYS>`: Maximum age in days for a file to be considered 'forgotten'. Default is `30` days.
*   `-s, --min-size-bytes <BYTES>`: Minimum size in bytes for a file to be considered 'significant'. Default is `1048576` bytes (1MB).
*   `-r, --recursive`: Include subdirectories in the scan. If omitted, only the top-level directory is scanned.

### Examples

1.  **Scan the current directory for files older than 60 days or larger than 5MB (non-recursive):**

    ```bash
    nightly-resource-scavenger -m 60 -s 5242880
    ```

2.  **Recursively scan your home directory for any file older than 7 days:**

    ```bash
    nightly-resource-scavenger -p ~/ -m 7 -r
    ```

3.  **Find all large files (over 10MB) in a specific project directory, regardless of age:**

    ```bash
    nightly-resource-scavenger -p /path/to/my/project -s 10485760 -m 0 -r
    ```
    (Setting `-m 0` means any file is considered 'old' if it exists, effectively focusing on size.)

## Scavenger Report Categories

*   `Forgotten Relic`: Files older than `--max-age-days`.
*   `Dusty Archive`: Files larger than `--min-size-bytes`.
*   `Ephemeral Scrap`: Files with common temporary extensions (e.g., `.log`, `.tmp`, `.bak`).
*   Combinations like `Forgotten Relic & Significant` or `Forgotten Relic (Ephemeral Scrap)` will appear for files matching multiple criteria.

Reclaim your digital territory, one forgotten file at a time!
