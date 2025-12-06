# Nightly Scavenger's Manifest Generator

## Overview

In the digital wasteland, valuable data can be scattered like precious rubble. The `Nightly Scavenger's Manifest Generator` is your trusty tool for inventorying these scattered bits. It scans a specified directory, identifies files based on their extensions, and compiles a comprehensive JSON manifest detailing their paths, sizes, and a total summary. Think of it as your digital metal detector, helping you find and catalog your digital "loot."

## Features

*   **Directory Scanning**: Recursively scans a target directory.
*   **Extension Filtering**: Include only files with specific extensions (e.g., `.txt`, `.log`, `.json`).
*   **Detailed Manifest**: Generates a JSON output with file paths (relative to the scanned directory), sizes in bytes, and a human-readable total size.
*   **Summary Statistics**: Provides a total count of scanned files and their cumulative size.
*   **Self-contained**: Pure Python, no external dependencies beyond standard library.

## Usage

The utility is a command-line tool.

### Basic Scan

To scan a directory and print the manifest to standard output:

```bash
python src/manifest_generator.py /path/to/your/wasteland
```

Example output:

```json
{
    "scan_directory": "/path/to/your/wasteland",
    "included_extensions": ["*"],
    "files": [
        {
            "path": "data/log_001.txt",
            "size_bytes": 12345
        },
        {
            "path": "reports/summary.json",
            "size_bytes": 6789
        }
    ],
    "summary": {
        "total_files_scanned": 2,
        "total_size_bytes": 19134,
        "total_size_human_readable": "18.69 KB"
    }
}
```

### Filtering by Extensions

To include only files with specific extensions (e.g., `.txt` and `.log`):

```bash
python src/manifest_generator.py /path/to/your/wasteland -e .txt .log
```

### Saving to a File

To save the manifest directly to a JSON file:

```bash
python src/manifest_generator.py /path/to/your/wasteland -o manifest.json
```

### Arguments

*   `<directory>` (required): The path to the directory you want to scan.
*   `-e`, `--extensions` (optional): A list of file extensions to include. If not specified, all files will be included. Example: `-e .txt .log .md`.
*   `-o`, `--output` (optional): The path to an output JSON file. If not specified, the manifest will be printed to `stdout`.

## Development

### Running Tests

To ensure the scavenger's tools are sharp, run the tests:

```bash
python -m unittest tests/test_manifest_generator.py
```
