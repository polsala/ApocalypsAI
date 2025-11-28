# Nightly Broken Link Beacon

## Overview

The Nightly Broken Link Beacon is a vigilant utility designed to scour your project directories for any HTTP/HTTPS links that have gone astray. It scans common documentation and content files (Markdown, HTML, reStructuredText) and attempts to verify the accessibility of every URL found. By identifying broken links, it helps maintain the integrity and reliability of your project's documentation and external references.

## Features

*   **Multi-file Type Support**: Scans `.md`, `.html`, and `.rst` files.
*   **Deep Directory Scan**: Recursively searches through specified directories.
*   **HTTP/HTTPS Verification**: Checks the status of found links using HEAD requests (with GET fallback).
*   **Clear Reporting**: Outputs a list of broken links with their respective files and error messages.

## Usage

```bash
python src/beacon.py --path <directory_to_scan> [--file-types md html rst] [--timeout 5]
```

### Arguments:

*   `--path <directory_to_scan>`: The root directory to start scanning from. **Required**.
*   `--file-types <type1> <type2> ...`: Space-separated list of file extensions to scan (e.g., `md html`). Defaults to `md html rst`.
*   `--timeout <seconds>`: Timeout for each HTTP request in seconds. Defaults to `5`.

## Example

```bash
python src/beacon.py --path ./docs --file-types md
```

This command will scan the `./docs` directory for Markdown files and check all links within them.

## Installation

This utility is self-contained. Ensure you have Python 3.8+ and `requests` installed.

```bash
pip install requests
```

## Development & Testing

To run tests:

```bash
python -m unittest tests/test_beacon.py
```
