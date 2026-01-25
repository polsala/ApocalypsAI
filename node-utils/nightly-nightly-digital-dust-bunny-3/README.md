# Nightly Digital Dust Bunny Sweeper

## Overview

The `nightly-digital-dust-bunny` is a whimsical-yet-useful Node.js command-line utility designed to help you declutter your digital workspace. It scans specified directories for old, unused, or temporary files (your 'digital dust bunnies') based on criteria like age, size, and filename patterns. Once identified, you can choose to list them, move them to a quarantine zone, or delete them, keeping your file system tidy and efficient.

## Features

*   **Flexible Scanning**: Define target directories and recursive scanning.
*   **Customizable Criteria**: Identify dust bunnies by:
    *   **Age**: Files older than a specified number of days.
    *   **Size**: Files larger or smaller than a specified size (in bytes).
    *   **Pattern**: Files matching a regular expression in their name.
*   **Actionable Results**: Choose to:
    *   **List**: Simply report the identified dust bunnies.
    *   **Quarantine**: Move them to a specified directory for review.
    *   **Delete**: Permanently remove them.
*   **Whimsical Reporting**: Get a 'Digital Lint Trap Report' summarizing your findings.

## Installation

1.  Ensure you have Node.js (v14 or higher) installed.
2.  Clone the `polsala/ApocalypsAI` repository.
3.  Navigate to the utility's directory:
    ```bash
    cd node-utils/nightly-digital-dust-bunny
    ```
4.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

Run the utility from its directory using `node src/index.js` followed by options.

```bash
node src/index.js <directory_to_scan> [options]
```

### Arguments

*   `<directory_to_scan>`: The root directory to start scanning from. Required.

### Options

*   `-a, --age <days>`: Files older than `<days>` will be considered dust bunnies. (e.g., `--age 30` for files older than 30 days).
*   `-s, --size-gt <bytes>`: Files larger than `<bytes>` will be considered dust bunnies. (e.g., `--size-gt 1048576` for files larger than 1MB).
*   `-p, --pattern <regex>`: Files whose names match the `<regex>` will be considered dust bunnies. (e.g., `--pattern "\\.log$"` for log files).
*   `-q, --quarantine <path>`: Move identified dust bunnies to the specified `<path>` instead of deleting. The path must exist.
*   `-d, --delete`: Permanently delete identified dust bunnies. **Use with caution!**
*   `-r, --recursive`: Scan directories recursively. (Default: true)
*   `-h, --help`: Display help information.

### Examples

1.  **List all `.tmp` files older than 7 days in the current directory (recursively):**
    ```bash
    node src/index.js . --age 7 --pattern "\\.tmp$"
    ```

2.  **Move all `.log` files older than 90 days from `/var/log` to `/tmp/dust-bunnies`:**
    ```bash
    mkdir -p /tmp/dust-bunnies # Ensure quarantine directory exists
    node src/index.js /var/log --age 90 --pattern "\\.log$" --quarantine /tmp/dust-bunnies
    ```

3.  **Delete all files larger than 500MB and older than 180 days in your downloads folder:**
    ```bash
    node src/index.js ~/Downloads --size-gt 524288000 --age 180 --delete
    ```

## Development

### Running Tests

```bash
npm test
```

This will execute the Jest test suite, which uses mocked file system operations for deterministic and safe testing.
