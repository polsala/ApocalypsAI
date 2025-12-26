# Nightly Digital Dust Bunny Sweeper

## Overview
In the post-apocalyptic digital landscape, clutter accumulates like radioactive dust. The `nightly-dust-bunny-sweeper` is your trusty companion, a whimsical Node.js CLI utility designed to help you declutter your file system by identifying and sweeping away old, unused files – your 'digital dust bunnies' – into a designated archive.

Keep your digital bunker tidy and efficient, ensuring only the most vital data remains readily accessible.

## Features
-   Scans specified directories for files.
-   Filters files based on their age (last modified date).
-   Filters files by specific file extensions.
-   Supports a 'dry run' mode to preview changes without moving any files.
-   Moves identified files to a user-defined archive directory or a default `.dustbunnies` folder.

## Installation
1.  **Clone the repository (or copy the utility folder):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-dust-bunny-sweeper
    ```
2.  **Ensure Node.js is installed:** This utility requires Node.js (v14 or higher).

## Usage
Run the `sweeper.js` script using Node.js, providing the necessary command-line arguments.

```bash
node src/sweeper.js --path <directory_to_sweep> [options]
```

### Arguments & Options
-   `--path <directory>` (Required): The root directory to start sweeping from. The utility will scan this directory and its subdirectories.
-   `--age <days>` (Optional): Files older than this many days (based on last modified date) will be considered dust bunnies. Default: `30` days.
-   `--extensions <ext1,ext2,...>` (Optional): A comma-separated list of file extensions (e.g., `log,tmp,bak`) to target. If not specified, all file types older than `--age` will be considered.
-   `--archive-dir <directory>` (Optional): The path to the directory where swept files will be moved. If not specified, a `.dustbunnies` folder will be created within the `--path` directory.
-   `--dry-run` (Optional): If present, the utility will only report which files *would* be swept, without actually moving them.

### Examples

1.  **Dry run: See what files older than 60 days would be swept from your 'downloads' folder:**
    ```bash
    node src/sweeper.js --path ~/Downloads --age 60 --dry-run
    ```

2.  **Sweep `.log` and `.tmp` files older than 7 days from your 'temp' directory into a specific archive:**
    ```bash
    node src/sweeper.js --path /var/log/old --age 7 --extensions log,tmp --archive-dir ~/DigitalVoid/ArchivedLogs
    ```

3.  **Sweep all files older than 90 days from your 'documents' folder into the default `.dustbunnies` archive:**
    ```bash
    node src/sweeper.js --path ~/Documents --age 90
    ```

## Tests
To run the tests, navigate to the utility's directory and execute:
```bash
node tests/sweeper.test.js
```

*(Note: This utility uses built-in Node.js modules and a simple test runner for self-containment.)*
