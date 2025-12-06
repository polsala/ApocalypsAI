# Nightly Data Scavenger Manifest Generator

## Overview
The `nightly-data-scavenger-manifest-generator` is a crucial utility for cataloging the digital remnants of the old world. It scans a specified directory for files matching a given set of extensions and compiles a structured manifest in JSON format. This manifest includes the relative path, size in bytes, and last modification timestamp (UTC) for each discovered file.

Think of it as your personal data scavenger, meticulously documenting every valuable byte found in the digital rubble.

## Usage
```bash
python src/manifest_generator.py --path <directory_to_scan> --extensions <comma_separated_extensions>
```

### Arguments:
*   `--path`: The base directory to start scanning from.
*   `--extensions`: A comma-separated list of file extensions (e.g., `py,md,json`) to include in the manifest. Do not include the leading dot.

## Example
```bash
python src/manifest_generator.py --path . --extensions py,md
```

### Example Output (JSON):
```json
[
  {
    "path": "README.md",
    "size_bytes": 1234,
    "last_modified_utc": "2023-10-27T10:00:00Z"
  },
  {
    "path": "src/manifest_generator.py",
    "size_bytes": 5678,
    "last_modified_utc": "2023-10-27T11:30:00Z"
  }
]
```
