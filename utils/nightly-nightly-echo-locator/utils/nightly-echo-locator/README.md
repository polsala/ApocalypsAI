# Nightly Echo Locator

## Overview

The Nightly Echo Locator is a utility designed to help you find duplicate files within specified directories. In the post-apocalyptic digital landscape, redundant data can consume precious storage and make navigation cumbersome. This tool acts as a sonic scanner, identifying files that are identical in content, allowing you to clean up your system and optimize your data reserves.

It works by calculating SHA256 hashes for files and grouping them by content. Only files with identical sizes are hashed to improve performance.

## Usage

```bash
python src/echo_locator.py <directory1> [directory2 ...] [--output-format <json|text>] [--min-size <bytes>]
```

### Arguments:

*   `<directory1> [directory2 ...]`: One or more paths to directories to scan for duplicates.
*   `--output-format <json|text>`: (Optional) Specify the output format. Defaults to `text`. `json` provides a structured output.
*   `--min-size <bytes>`: (Optional) Only consider files larger than or equal to this size (in bytes). Defaults to 0.

### Examples:

Scan a single directory and print text output:
```bash
python src/echo_locator.py ~/my_data
```

Scan multiple directories and output JSON:
```bash
python src/echo_locator.py /var/log /tmp/backups --output-format json
```

Scan a directory for duplicates larger than 1MB:
```bash
python src/echo_locator.py ~/downloads --min-size 1048576
```

## Output Format

### Text Output (default):

```
Found 2 sets of duplicate files:

Set 1 (SHA256: a1b2c3d4...):
  - /path/to/file1.txt
  - /path/to/another/file1.txt

Set 2 (SHA256: e5f6g7h8...):
  - /path/to/image.jpg
  - /path/to/backup/image.jpg
```

### JSON Output:

```json
[
  {
    "hash": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
    "size": 1234,
    "files": [
      "/path/to/file1.txt",
      "/path/to/another/file1.txt"
    ]
  },
  {
    "hash": "e5f6g7h8i9j0e5f6g7h8i9j0e5f6g7h8i9j0e5f6g7h8i9j0e5f6g7h8i9j0e5f6",
    "size": 56789,
    "files": [
      "/path/to/image.jpg",
      "/path/to/backup/image.jpg"
    ]
  }
]
```
