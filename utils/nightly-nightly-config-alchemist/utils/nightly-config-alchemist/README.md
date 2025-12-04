# Nightly Config Alchemist

## Overview

In the ever-shifting digital wasteland, configuration files can easily drift into chaotic disarray, leading to subtle errors and maintenance headaches. The `Nightly Config Alchemist` is a whimsical yet crucial utility designed to bring order to this chaos.

It scans specified directories for YAML and JSON configuration files, validates their syntax, and optionally normalizes their formatting (e.g., consistent indentation, sorted keys for JSON). This ensures that all your critical configurations are not only syntactically correct but also consistently formatted, making them easier to read, compare, and manage.

## Features

*   **Syntax Validation**: Automatically checks if YAML and JSON files are well-formed.
*   **Format Normalization**: Optionally re-writes files with a standardized format (e.g., 2-space indentation, sorted JSON keys).
*   **Recursive Scanning**: Traverses directories to find all relevant configuration files.
*   **Report Generation**: Provides a summary of files processed, errors found, and changes made.
*   **Dry Run Mode**: By default, it only reports issues and suggested changes without modifying files.

## Usage

```bash
python src/alchemist.py --path <directory_or_file> [--extensions .json .yml .yaml] [--apply] [--indent 2]
```

### Arguments:

*   `--path <directory_or_file>`: The path to a file or directory to process. If a directory, it will be scanned recursively.
*   `--extensions <ext1> <ext2> ...`: A space-separated list of file extensions to process (e.g., `.json`, `.yml`, `.yaml`). Defaults to `.json` and `.yaml`.
*   `--apply`: If present, the utility will modify files to apply normalization. By default, it runs in 'check' mode and only reports potential changes.
*   `--indent <int>`: The number of spaces to use for indentation during normalization. Defaults to `2`.

### Examples:

*   **Check all config files in the current directory and subdirectories:**
    ```bash
    python src/alchemist.py --path .
    ```
*   **Normalize a specific YAML file with 4-space indentation:**
    ```bash
    python src/alchemist.py --path config/settings.yml --apply --indent 4
    ```
*   **Check only JSON files in a 'data' directory:**
    ```bash
    python src/alchemist.py --path data/ --extensions .json
    ```

## Installation

This utility requires `PyYAML`. You can install it using pip:

```bash
pip install PyYAML
```
