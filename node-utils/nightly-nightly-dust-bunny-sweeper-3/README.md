# Nightly Dust Bunny Sweeper

## Overview

Ever feel like your project directories are accumulating digital fluff? The `nightly-dust-bunny-sweeper` is here to help! This whimsical Node.js utility scans your specified directories for common digital clutter – think `node_modules`, `dist` folders, log files, and empty directories – and helps you identify or even sweep them away, making your workspace feel lighter and tidier.

It's like a tiny, automated Roomba for your file system, but instead of actual dust, it tackles the digital kind!

## Features

*   **Clutter Detection**: Identifies common build artifacts, temporary files, and empty directories.
*   **Dry Run Mode**: See what would be swept without actually deleting anything.
*   **Selective Deletion**: Choose to delete the identified clutter.
*   **Cross-Platform**: Works wherever Node.js runs.
*   **Whimsical Output**: Enjoy playful messages as your digital space gets tidied.

## Installation

1.  Navigate to the `node-utils/nightly-dust-bunny-sweeper` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

Run the utility from your terminal. You can specify a target path and choose between a dry run or actual deletion.

```bash
node src/index.js [options]
```

### Options

*   `-p, --path <path>`: The directory to scan. Defaults to the current working directory (`.`).
*   `-d, --delete`: Enable deletion of identified dust bunnies. **Use with caution!**
*   `-r, --dry-run`: Perform a dry run, reporting what *would* be deleted without actually deleting anything. (Default: `true` if `--delete` is not specified).
*   `-h, --help`: Display help for command.

### Examples

1.  **Perform a dry run in the current directory (default behavior):**
    ```bash
    node src/index.js
    ```
    or
    ```bash
    node src/index.js --dry-run
    ```

2.  **Perform a dry run in a specific directory:**
    ```bash
    node src/index.js --path /path/to/your/project
    ```

3.  **Sweep away dust bunnies in the current directory (be careful!):**
    ```bash
    node src/index.js --delete
    ```

4.  **Sweep away dust bunnies in a specific directory:**
    ```bash
    node src/index.js --path /path/to/your/project --delete
    ```

## Configuration

The utility uses a predefined list of common clutter patterns. Future versions might allow custom configuration.

## Development

To run tests:

```bash
npm test
```
