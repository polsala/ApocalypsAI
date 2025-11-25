# Nightly Echo Chamber Purifier

## Overview

The Nightly Echo Chamber Purifier is a utility designed to detect and report duplicate files within specified directories. By calculating content hashes, it identifies files that are exact copies, helping to declutter repositories, reduce storage usage, and improve overall data hygiene.

This tool is particularly useful for identifying redundant assets, copied code snippets, or forgotten temporary files that have accumulated over time.

## Usage

```bash
python src/purifier.py <directory_path> [--exclude <pattern>] [--min-size <bytes>]
```

- `<directory_path>`: The root directory to start scanning for duplicates.
- `--exclude <pattern>`: (Optional) A glob pattern to exclude files or directories (e.g., `*.log`, `temp/*`). Can be specified multiple times.
- `--min-size <bytes>`: (Optional) Only consider files larger than this size (default: 1 byte).

### Example

To scan your current directory, excluding `.git` and `node_modules` folders, and only considering files larger than 1KB:

```bash
python src/purifier.py . --exclude '.git/*' --exclude 'node_modules/*' --min-size 1024
```

## How it Works

The purifier recursively traverses the specified directory, calculates a SHA256 hash for each file's content, and stores these hashes along with their corresponding file paths. Files with identical hashes are considered duplicates. The tool then reports these groups of duplicate files to the console.

## Development

To run tests:

```bash
python -m unittest tests/test_purifier.py
```
