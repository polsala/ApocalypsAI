# Digital Dust Bunny Sweeper

## Overview

Ever feel like your digital workspace is accumulating forgotten files and directories, like dust bunnies under the bed? The `digital-dust-bunny-sweeper` is here to help! This whimsical-yet-useful Python utility scans a specified directory for files and folders that haven't been modified in a long time, helping you identify and clean up your 'digital dust bunnies'.

It's perfect for decluttering development environments, project folders, or any directory that tends to accumulate cruft over time.

## Features

*   Scans a target directory recursively.
*   Identifies files and directories older than a specified age threshold.
*   Supports ignoring specific file/directory patterns.
*   Outputs a clear list of potential 'dust bunnies'.

## Usage

```bash
python src/dust_bunny_sweeper.py <path_to_scan> [--age <days>] [--ignore <pattern>]...
```

### Arguments

*   `<path_to_scan>`: The root directory to start scanning from. (Required)
*   `--age <days>`: The age threshold in days. Files/directories not modified within this many days will be considered 'dust bunnies'. Defaults to 90 days. (Optional)
*   `--ignore <pattern>`: A glob-style pattern to ignore files or directories. Can be specified multiple times. E.g., `--ignore "*.log"` or `--ignore "node_modules"`. (Optional)

### Examples

1.  **Scan current directory for items older than 30 days:**
    ```bash
    python src/dust_bunny_sweeper.py . --age 30
    ```

2.  **Scan a project directory, ignoring `node_modules` and `.git` folders, for items older than a year:**
    ```bash
    python src/dust_bunny_sweeper.py /path/to/my/project --age 365 --ignore "node_modules" --ignore ".git"
    ```

3.  **Scan for default 90-day old items, ignoring all `.tmp` files:**
    ```bash
    python src/dust_bunny_sweeper.py /home/user/downloads --ignore "*.tmp"
    ```

## Installation

No special installation is required beyond having Python 3.6+ installed. Simply place the `digital-dust-bunny-sweeper` folder in your `utils/` directory and run the script directly.
