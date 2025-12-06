# Nightly Scavenger Scrutiny Scanner

## Overview
The `nightly-scavenger-scrutiny-scanner` is a whimsical-yet-useful command-line utility designed to help you sift through digital "rubble" – messy directories, recovered drives, or forgotten archives – to identify potentially valuable files. It scans a specified directory for files matching predefined criteria like file extensions and keywords in their names. Think of it as your digital metal detector for the post-apocalyptic data landscape.

## Features
*   Scans a target directory recursively.
*   Filters files by a list of desired file extensions (e.g., `.txt`, `.md`, `.json`).
*   Filters files by keywords present in their filenames (e.g., `backup`, `notes`, `config`).
*   Outputs a list of all matching files.

## Installation
This utility is self-contained and requires no special installation beyond a Python 3.11+ environment.

## Usage

```bash
python src/scanner.py --path /path/to/scan --extensions .txt .md .json --keywords config backup notes
```

### Arguments:
*   `--path <directory>` (required): The root directory to start scanning from.
*   `--extensions <ext1> <ext2> ...` (optional): A space-separated list of file extensions to look for (e.g., `.txt`, `.log`). Case-insensitive.
*   `--keywords <kw1> <kw2> ...` (optional): A space-separated list of keywords to look for in filenames (e.g., `report`, `data`). Case-insensitive.

If neither `--extensions` nor `--keywords` are provided, the scanner will list all files in the directory.

### Examples:

1.  **Find all Python scripts and Markdown files in your current directory:**
    ```bash
    python src/scanner.py --path . --extensions .py .md
    ```

2.  **Locate any files with "config" or "backup" in their name, regardless of extension:**
    ```bash
    python src/scanner.py --path /var/log --keywords config backup
    ```

3.  **Find important text files (notes, logs) in a recovered drive:**
    ```bash
    python src/scanner.py --path /mnt/recovered_drive --extensions .txt .log --keywords notes important
    ```

4.  **List all files in a directory (no filters):**
    ```bash
    python src/scanner.py --path ~/documents
    ```
