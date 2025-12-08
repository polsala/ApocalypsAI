# Nightly Digital Hoard Herder

## Summary

The `nightly-digital-hoard-herder` is a whimsical Node.js utility designed to help you tame your ever-growing digital collection. It scans a specified directory for "Forgotten Relics" (files older than a certain age) and "Space Gobblers" (files larger than a certain size), providing a playful report and suggesting whimsical renaming strategies for old files.

Think of it as a friendly digital archaeologist, unearthing long-lost treasures and politely nudging oversized artifacts into their proper place.

## Features

*   **Hoard Analysis**: Scans directories recursively to identify files based on age and size.
*   **Forgotten Relics**: Reports files older than a configurable threshold.
*   **Space Gobblers**: Reports files larger than a configurable threshold.
*   **Whimsical Renaming (Suggestion)**: For old files, it suggests appending a fun, random suffix (e.g., `document_of_yore.pdf`) to their filenames. *Note: This utility currently only reports suggested renames; it does not perform the actual file system operation for safety.*

## Usage

To run the Digital Hoard Herder, navigate to the utility's directory and execute the `index.js` script with Node.js.

```bash
node src/index.js [directory_to_scan] [age_threshold_days] [size_threshold_mb] [--whimsical-rename]
```

### Arguments:

*   `directory_to_scan` (optional): The path to the directory you want to analyze. Defaults to the current directory (`.`).
*   `age_threshold_days` (optional): Files older than this many days will be considered "Forgotten Relics". Defaults to `365` (1 year).
*   `size_threshold_mb` (optional): Files larger than this many megabytes will be considered "Space Gobblers". Defaults to `100` MB.
*   `--whimsical-rename` (optional flag): If present, the utility will suggest whimsical renames for "Forgotten Relics".

### Examples:

1.  **Analyze current directory with default settings:**
    ```bash
    node src/index.js
    ```

2.  **Analyze a specific folder, looking for files older than 90 days or larger than 500MB:**
    ```bash
    node src/index.js /path/to/my/downloads 90 500
    ```

3.  **Analyze a folder and get whimsical rename suggestions for old files:**
    ```bash
    node src/index.js ~/Documents 730 20 --whimsical-rename
    ```

## Development

### Prerequisites

*   Node.js (v14 or higher)

### Running Tests

Tests are written using Jest. To run them, you'll need to have Jest installed (globally or locally).

1.  Install Jest (if you haven't already):
    ```bash
    npm install --save-dev jest
    # or yarn add --dev jest
    ```
2.  Run the tests:
    ```bash
    npx jest tests/index.test.js
    ```
