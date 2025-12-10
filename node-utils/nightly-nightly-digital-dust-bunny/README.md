# Nightly Digital Dust Bunny Sweeper

A whimsical yet practical Node.js CLI utility to help you declutter your digital spaces by identifying and optionally removing old, unused files – your "digital dust bunnies."

## Features

*   **Scan Directories**: Recursively scans specified directories for files.
*   **Age Filtering**: Filters files based on their last modified date (e.g., older than 30 days).
*   **Dry Run Mode**: See which files would be removed without actually deleting them.
*   **Interactive Deletion**: Confirm deletion for each file or all at once.

## Installation

1.  Navigate to the `node-utils/nightly-digital-dust-bunny` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  (Optional) Link the utility for global access:
    ```bash
    npm link
    ```
    Or run directly using `node src/index.js`.

## Usage

```bash
node src/index.js <directory_path> [options]
```

### Options

*   `-a, --age <days>`: Files older than this many days will be considered "dust bunnies". Default is 30 days.
*   `-d, --dry-run`: List files that would be deleted without actually deleting them.
*   `-y, --yes`: Automatically confirm deletion for all identified files (use with caution!).
*   `-h, --help`: Display help information.

### Examples

Scan the current directory for files older than 60 days (dry run):
```bash
node src/index.js . --age 60 --dry-run
```

Scan a specific directory and interactively delete files older than 90 days:
```bash
node src/index.js /path/to/my/old/files --age 90
```

Scan and automatically delete all files older than 7 days in a specific directory:
```bash
node src/index.js /path/to/temp/files --age 7 --yes
```

## Development

To run tests:
```bash
npm test
```
