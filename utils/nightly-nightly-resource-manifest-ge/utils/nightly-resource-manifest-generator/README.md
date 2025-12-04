# Nightly Resource Manifest Generator

## Overview
The `nightly-resource-manifest-generator` is a crucial utility for cataloging the digital remnants of the old world. It meticulously scans a specified directory, calculates the size, SHA256 hash, and last modification timestamp for each file, and compiles this information into a structured manifest (JSON or YAML format). This manifest serves as a vital inventory for resource tracking, integrity verification, and post-apocalyptic data management.

## Features
- **Directory Scanning**: Recursively traverses a given directory.
- **File Metadata Extraction**: Gathers file size, SHA256 hash, and last modification timestamp.
- **Flexible Output**: Generates manifests in either JSON or YAML format.
- **Integrity Checks**: Provides hashes for verifying file integrity over time.

## Usage

```bash
python src/manifest_generator.py --path <directory_to_scan> --output-format <json|yaml> [--output-file <filename>]
```

### Arguments:
- `--path <directory_to_scan>`: The root directory to scan for resources. (Required)
- `--output-format <json|yaml>`: The desired output format for the manifest. (Required)
- `--output-file <filename>`: Optional. If provided, the manifest will be written to this file. Otherwise, it prints to stdout.

### Examples:

**Generate a JSON manifest and print to console:**
```bash
python src/manifest_generator.py --path ./my_wasteland_data --output-format json
```

**Generate a YAML manifest and save to a file:**
```bash
python src/manifest_generator.py --path ./my_vault --output-format yaml --output-file vault_manifest.yaml
```

## Manifest Structure Example (JSON)

```json
{
  "scan_root": "/path/to/my_wasteland_data",
  "scan_timestamp": "2023-10-27T10:30:00Z",
  "files": [
    {
      "path": "data/document.txt",
      "size_bytes": 1234,
      "sha256_hash": "a1b2c3d4e5f6...",
      "last_modified_timestamp": "2023-10-26T08:15:30Z"
    },
    {
      "path": "images/photo.jpg",
      "size_bytes": 56789,
      "sha256_hash": "f6e5d4c3b2a1...",
      "last_modified_timestamp": "2023-10-25T14:00:00Z"
    }
  ]
}
```
