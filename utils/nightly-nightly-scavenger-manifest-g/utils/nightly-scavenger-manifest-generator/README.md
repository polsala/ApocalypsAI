# Nightly Scavenger's Manifest Generator

## Overview

The Nightly Scavenger's Manifest Generator is a utility designed to help you take inventory of your digital hoard. In the post-apocalyptic data landscape, knowing what you have and where it is can be crucial. This tool scans a specified directory, identifies files, categorizes them by their extensions, and compiles a comprehensive manifest.

It provides:
- A count of files per extension type.
- The total size of files per extension type.
- The total number of files scanned.
- The total cumulative size of all scanned files.
- The most recent modification timestamp across all scanned files.

## Usage

Run the utility from the command line, providing the path to the directory you wish to scan.

```bash
python src/manifest_generator.py --path /path/to/your/data/hoard
```

The output will be a JSON string printed to standard output, summarizing the findings.

### Arguments

*   `--path <directory_path>`: (Required) The absolute or relative path to the directory to scan.
*   `--output <file_path>`: (Optional) Path to a file where the JSON output should be written. If not provided, output goes to stdout.

## Example Output

```json
{
  "scan_path": "/path/to/your/data/hoard",
  "total_files_scanned": 10,
  "total_size_bytes": 102400,
  "most_recent_modification_utc": "2023-10-27T14:30:00Z",
  "file_types": {
    ".txt": {
      "count": 5,
      "total_size_bytes": 50000
    },
    ".log": {
      "count": 3,
      "total_size_bytes": 30000
    },
    ".json": {
      "count": 2,
      "total_size_bytes": 22400
    }
  }
}
```

## Development

The utility is written in Python 3.11 and uses only standard library modules (`os`, `datetime`, `json`, `argparse`).
Tests are located in `tests/test_manifest_generator.py` and are designed to be deterministic and offline using mocks.
