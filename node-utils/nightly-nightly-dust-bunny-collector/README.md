# Nightly Digital Dust Bunny Collector

A whimsical Node.js utility to help you tidy up your digital space by identifying and managing 'digital dust bunnies' – old, forgotten files that accumulate in your directories.

## Features

*   **Find Old Files**: Scans specified directories for files older than a given age threshold.
*   **List**: Simply lists the identified 'dust bunnies' with their age.
*   **Archive**: Moves identified 'dust bunnies' to a dedicated `.dust-bunnies-archive` subfolder within the scanned directory, keeping your main workspace clean without permanent deletion.
*   **Cross-Platform**: Built with Node.js, it runs seamlessly on Windows, macOS, and Linux.

## Installation

1.  **Clone the repository (or just this utility)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-dust-bunny-collector
    ```

2.  **Install dependencies (if any, though this utility aims for minimal built-in deps)**:
    ```bash
    # No external npm dependencies for this version.
    # If you were to add more complex CLI parsing (e.g., 'commander'), you'd run:
    # npm install
    ```

## Usage

Run the utility using `node` from its directory. You can specify the target path, age threshold, and action.

```bash
node src/index.js [options]
```

### Options

*   `--path <directory>`: The directory to scan. Defaults to the current directory (`.`).
*   `--age <days>`: The minimum age in days for a file to be considered a 'dust bunny'. Defaults to `90` days.
*   `--action <list|archive>`: The action to perform on found dust bunnies.
    *   `list` (default): Only list the files found.
    *   `archive`: Move the files to a `.dust-bunnies-archive` subfolder within the target directory.

### Examples

1.  **List all files older than 60 days in the current directory**:
    ```bash
    node src/index.js --age 60
    ```

2.  **List all files older than 180 days in a specific folder**:
    ```bash
    node src/index.js --path /path/to/my/documents --age 180
    ```

3.  **Archive files older than 30 days in your downloads folder**:
    ```bash
    node src/index.js --path ~/Downloads --age 30 --action archive
    ```

4.  **Run with default settings (list files older than 90 days in current directory)**:
    ```bash
    node src/index.js
    ```

## Development

### Running Tests

This utility uses `jest` for testing. To run the tests, you'll need `jest` installed globally or locally.

1.  **Install Jest (if you haven't already)**:
    ```bash
    npm install --save-dev jest
    # or globally: npm install -g jest
    ```

2.  **Run the tests**:
    ```bash
    jest tests/test.js
    ```
