# Nightly Resource Scavenger

## Overview

The `Nightly Resource Scavenger` is a vigilant utility designed to keep your repository's documentation in top shape. Like a digital scavenger, it meticulously combs through Markdown files (`.md`, `.markdown`) to unearth any broken or unreachable HTTP/HTTPS links. In a world of constant change, ensuring your external references are valid is crucial for maintaining reliable and helpful documentation.

This tool helps prevent the frustration of clicking dead links, making your project's resources more robust and user-friendly.

## How it Works

1.  **Scans Directories**: Recursively searches a specified directory (e.g., the entire repository) for all Markdown files.
2.  **Extracts Links**: Parses each Markdown file to identify all HTTP and HTTPS URLs.
3.  **Checks Reachability**: Performs a lightweight `HEAD` request for each extracted URL to verify its status.
4.  **Reports Findings**: Compiles a list of all broken links (e.g., 4xx/5xx errors, connection issues) and prints them to the console.

## Usage

To run the scavenger, simply execute the `scavenger.py` script with the path to the directory you wish to scan:

```bash
python3 src/scavenger.py --path ../../
```

Replace `../../` with the actual path to your repository root or any subdirectory you want to scan.

### Example Output (with broken links)

```
Scanning for broken links in: /path/to/your/repo

Found 2 Markdown files.

--- Broken Links Found ---

File: /path/to/your/repo/docs/guide.md
  - https://example.com/non-existent-page (Status: 404 Not Found)
  - https://broken-domain.invalid (Error: Connection Error)

File: /path/to/your/repo/README.md
  - https://another-broken-link.org/old-doc (Status: 500 Internal Server Error)

--- Scan Complete ---
```

### Example Output (no broken links)

```
Scanning for broken links in: /path/to/your/repo

Found 1 Markdown files.

--- Scan Complete ---
No broken links found. All clear!
---
```

## Development

### Dependencies

*   `requests` (for making HTTP requests)

Install them using pip:

```bash
pip install requests
```

### Running Tests

Tests are located in the `tests/` directory. You can run them using `unittest`:

```bash
python3 -m unittest tests/test_scavenger.py
```
