# Nightly Scavenger Manifest Generator

## Overview

In the desolate wastes, every scrap of data is precious. The Nightly Scavenger Manifest Generator is your trusty companion for cataloging the digital debris you unearth. This utility scans a specified directory, categorizes files by their extensions, and compiles a comprehensive manifest. It provides a quick overview of file types, total sizes, and can even highlight recently modified files, helping you prioritize your digital salvage operations.

## Features

*   **File Categorization**: Automatically groups files by their extension (e.g., `.txt`, `.log`, `.json`).
*   **Size Aggregation**: Calculates the total size for each file type and the overall directory.
*   **Recent Activity Tracking**: Optionally identifies files modified within a specified number of days, perfect for spotting fresh intel or critical updates.
*   **JSON Output**: Generates a structured JSON manifest for easy parsing and integration with other systems.

## Usage

The `manifest_generator.py` script can be run directly from the command line.

```bash
python src/manifest_generator.py <directory_path> [--recent-days <number_of_days>]
```

### Arguments:

*   `<directory_path>`: The absolute or relative path to the directory you wish to scan.
*   `--recent-days <number_of_days>`: (Optional) An integer specifying the number of days back to consider a file "recent". If provided, the manifest will include a list of files modified within this period.

### Example:

To generate a manifest for the current directory, including files modified in the last 7 days:

```bash
python src/manifest_generator.py . --recent-days 7
```

### Output Example:

```json
{
    "scanned_directory": "/path/to/your/directory",
    "total_files": 10,
    "total_size_bytes": 102400,
    "summary_by_extension": {
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
    },
    "recent_files": [
        {
            "path": "/path/to/your/directory/new_data.json",
            "size_bytes": 10240,
            "modified_timestamp": 1678886400.0
        },
        {
            "path": "/path/to/your/directory/report.txt",
            "size_bytes": 5000,
            "modified_timestamp": 1678880000.0
        }
    ]
}
```

## Development

The utility is written in Python 3.11 and uses only standard library modules (`os`, `json`, `datetime`).
