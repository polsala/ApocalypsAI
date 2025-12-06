# Scavenger's Manifest Generator

## Overview

The `Scavenger's Manifest Generator` is a utility designed to help you catalog your digital 'scavenged' assets. It scans a specified directory (and optionally its subdirectories) and generates a comprehensive JSON manifest file. This manifest includes details for each file such as its path, name, size, last modification timestamp, and a SHA256 checksum, providing a reliable inventory of your data.

Whether you're tracking critical survival documents, code fragments, or just curious about the contents of a forgotten data hoard, this tool ensures you have a clear, machine-readable record.

## Usage

```bash
python src/manifest_generator.py <directory_path> [--output <filename>] [--recursive] [--exclude <pattern1,pattern2,...>]
```

### Arguments:

*   `<directory_path>`: The path to the directory you want to scan.
*   `--output <filename>`: (Optional) The name of the output JSON file. Defaults to `manifest.json`.
*   `--recursive`: (Optional) Scan subdirectories recursively. If not provided, only the top-level directory is scanned.
*   `--exclude <pattern1,pattern2,...>`: (Optional) A comma-separated list of glob patterns (e.g., `*.log`, `temp/*`) to exclude files or directories from the scan. Patterns are matched against the full relative path.

### Example:

```bash
# Scan current directory, output to manifest.json
python src/manifest_generator.py .

# Scan 'my_data' directory recursively, output to data_inventory.json
python src/manifest_generator.py my_data --recursive --output data_inventory.json

# Scan 'project_files' recursively, excluding '.git' directory and '*.pyc' files
python src/manifest_generator.py project_files --recursive --exclude '.git/*,*.pyc'
```

## Output Format

The generated manifest file will be a JSON object with the following structure:

```json
{
  "manifest_version": "1.0",
  "scan_timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "scanned_directory": "/absolute/path/to/scanned/dir",
  "files": [
    {
      "path": "relative/path/to/file.ext",
      "name": "file.ext",
      "size_bytes": 12345,
      "last_modified_utc": "YYYY-MM-DDTHH:MM:SSZ",
      "sha256_checksum": "a1b2c3d4e5f6..."
    },
    // ... more files
  ]
}
```

## Development

This utility is written in Python 3.11+ and uses standard library modules only. No external dependencies are required.

To run tests:

```bash
python -m unittest tests/test_manifest_generator.py
```
