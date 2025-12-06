# Nightly Digital Echo Locator

## Overview

The Nightly Digital Echo Locator is a whimsical-yet-useful utility designed to ensure the integrity of your digital pathways. In the post-apocalyptic digital landscape, links can decay, leading to broken connections and lost information. This tool acts as a sonar, scanning specified files for URLs and pinging them to verify their reachability.

It's perfect for maintaining documentation, code comments, or any text files where external links are crucial. By running this nightly, you can proactively identify and fix broken links before they become a problem.

## Features

*   **URL Extraction**: Automatically finds URLs within various text-based files.
*   **Reachability Check**: Pings identified URLs to determine if they are active and accessible.
*   **Configurable Paths**: Specify directories or individual files to scan.
*   **File Type Filtering**: Limit scans to specific file extensions (e.g., `.md`, `.py`, `.txt`).
*   **Detailed Reporting**: Outputs a clear list of broken links found.

## Installation

This utility is self-contained and requires Python 3.8+.

```bash
# Navigate to the utility directory
cd utils/nightly-digital-echo-locator

# Install dependencies (if any, currently only requests)
pip install -r requirements.txt
```

## Usage

Run the `echo_locator.py` script from the command line.

```bash
python src/echo_locator.py --path <path_to_scan> [--extensions <ext1,ext2,...>] [--timeout <seconds>] [--verbose]
```

### Arguments

*   `--path <path>`: **Required**. The file or directory to scan. If a directory, it will be scanned recursively.
*   `--extensions <ext1,ext2,...>`: Optional. A comma-separated list of file extensions to include in the scan (e.g., `md,py,txt`). If not provided, all files will be scanned.
*   `--timeout <seconds>`: Optional. The maximum time in seconds to wait for a URL to respond. Default is 5 seconds.
*   `--verbose`: Optional. Print more detailed output during the scan.

### Examples

Scan a single Markdown file:

```bash
python src/echo_locator.py --path docs/README.md
```

Scan an entire `src` directory for Python and Markdown files:

```bash
python src/echo_locator.py --path src/ --extensions py,md
```

Scan a directory with a shorter timeout and verbose output:

```bash
python src/echo_locator.py --path my_project/ --timeout 3 --verbose
```

## Development

### Running Tests

To ensure the Echo Locator is functioning correctly, run the provided tests:

```bash
cd utils/nightly-digital-echo-locator
python -m unittest tests/test_echo_locator.py
```
