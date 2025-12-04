# Nightly Data Debris Decipherer

## Overview

In the post-apocalyptic wasteland, data is often fragmented, scattered, and buried within countless text files – digital debris from a bygone era. The **Nightly Data Debris Decipherer** is a crucial utility designed to sift through this informational rubble, automatically identifying and extracting common, structured data patterns such as URLs, email addresses, and ISO 8601 timestamps.

This tool helps survivors (and their AI counterparts) make sense of the digital detritus, recovering vital communication channels, historical records, or even forgotten server logs.

## Features

*   **Pattern Recognition**: Automatically detects URLs, email addresses, and ISO 8601 formatted dates/timestamps.
*   **Directory Scanning**: Recursively scans a specified directory for `.txt`, `.log`, `.md`, and `.json` files by default.
*   **Structured Output**: Generates a JSON report detailing the extracted data for each file.
*   **Self-Contained**: No external dependencies beyond Python's standard library.

## Usage

```bash
python src/decipherer.py --input-dir /path/to/debris --output-file report.json
```

### Arguments

*   `--input-dir <path>`: The directory to scan for data debris. (Required)
*   `--output-file <path>`: Optional. The path to save the JSON report. If not provided, the report will be printed to standard output.
*   `--file-extensions <ext1,ext2,...>`: Optional. Comma-separated list of file extensions to process (e.g., `txt,log`). Defaults to `txt,log,md,json`.

## Example Output

```json
[
    {
        "filepath": "/path/to/debris/log_2023.txt",
        "urls": [
            "http://old-server.com/status",
            "https://archive.net/data/report.pdf"
        ],
        "emails": [
            "admin@old-corp.com"
        ],
        "timestamps": [
            "2023-01-15T10:30:00Z",
            "2023-01-14"
        ]
    },
    {
        "filepath": "/path/to/debris/notes.md",
        "urls": [],
        "emails": [
            "contact@new-hope.org"
        ],
        "timestamps": []
    }
]
```
