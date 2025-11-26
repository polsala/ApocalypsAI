# Nightly Resource Scavenger

## Overview

The Nightly Resource Scavenger is a vigilant utility designed to comb through your repository's documentation and text files, identifying and reporting any broken external links. In the ever-shifting digital landscape, links can decay, leading to outdated information and frustrating user experiences. This tool helps ensure your project's external references remain robust and reliable, keeping your documentation pristine for future generations of survivors.

## Features

*   **Link Discovery**: Scans specified file types (e.g., Markdown, plain text) for HTTP/HTTPS URLs.
*   **Broken Link Detection**: Attempts to connect to discovered URLs and reports non-2xx HTTP status codes or connection errors.
*   **Configurable**: Allows specifying target directories and file extensions.

## Usage

```bash
python src/scavenger.py --path <directory_to_scan> --extensions md txt
```

### Arguments

*   `--path <directory>`: The root directory to start scanning from. Defaults to the current directory.
*   `--extensions <ext1> <ext2> ...`: A space-separated list of file extensions to check (e.g., `md txt`). Defaults to `md`.
*   `--timeout <seconds>`: Connection timeout for HTTP requests in seconds. Defaults to 5.
*   `--ignore-patterns <pattern1> <pattern2> ...`: A space-separated list of regex patterns for URLs to ignore.

## Example

To check all Markdown and text files in the current directory and its subdirectories:

```bash
python src/scavenger.py --path . --extensions md txt
```

To check only Markdown files in a specific `docs` folder, ignoring GitHub-internal links:

```bash
python src/scavenger.py --path docs --extensions md --ignore-patterns "https://github.com/polsala/ApocalypsAI/issues"
```

## Installation

This utility is self-contained. Ensure you have Python 3.11+ and `requests` installed.

```bash
pip install requests
```

## Development

To run tests:

```bash
python -m unittest tests/test_scavenger.py
```
