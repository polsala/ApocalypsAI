# Nightly Echo Chamber Monitor

## Purpose

The Nightly Echo Chamber Monitor is a whimsical-yet-useful utility designed to detect and report duplicate files within a specified directory. In the post-apocalyptic landscape, redundant data can clog precious storage and obscure vital information. This monitor helps you identify and address these "echoes" of files, ensuring your data repository remains lean and efficient.

It works by calculating SHA256 hashes for all files and grouping paths that share the same hash, providing a clear report of where your data is repeating itself.

## Usage

```bash
python src/monitor.py --path /path/to/your/directory
```

### Arguments

*   `--path <directory_path>`: **Required**. The root directory to scan for duplicate files.

## Example Output

```
Scanning /path/to/your/directory for echoes...

Found 2 sets of duplicate files:

--- Duplicate Set 1 ---
Hash: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2
  - /path/to/your/directory/docs/report_v1.txt
  - /path/to/your/directory/archive/old_report.txt

--- Duplicate Set 2 ---
Hash: f0e1d2c3b4a5f6e7d8c9b0a1f2e3d4c5b6a7f8e9d0c1b2a3f4e5d5c6b7a8f9e0
  - /path/to/your/directory/images/logo.png
  - /path/to/your/directory/assets/branding/logo_copy.png

Scan complete. No more echoes detected.
```

## How it Works

1.  **Traversal**: Recursively walks through the specified directory.
2.  **Hashing**: For each regular file, it reads its content in chunks and computes a SHA256 hash.
3.  **Comparison**: Stores file paths grouped by their hash.
4.  **Reporting**: Outputs a formatted list of all hash groups containing more than one file path, indicating duplicates.

## Development

To run tests:

```bash
python -m unittest tests/test_monitor.py
```
