# Nightly Resource Scavenger

## Overview

The Nightly Resource Scavenger is a utility designed to help maintain the health and integrity of your repository's documentation. It automatically scans Markdown files (like `README.md`, `AGENTS.md`, etc.) for external URLs and checks if these links are still active and accessible. Broken links can lead to frustration for users and contributors, and this tool helps identify them proactively.

## Features

*   **Markdown Link Extraction**: Identifies URLs embedded in standard Markdown link syntax (`[text](url)`) and raw URLs (`<url>`).
*   **HTTP Status Checking**: Performs HEAD requests to check the status of each identified URL.
*   **Configurable Exclusions**: Allows specifying patterns to exclude certain files or directories from the scan.
*   **Clear Reporting**: Outputs a list of broken links, indicating the file, the URL, and the HTTP status code or error.

## Usage

To run the scavenger, navigate to the `utils/nightly-resource-scavenger/src` directory and execute the `scavenger.py` script:

```bash
python scavenger.py --path ../../ --exclude-patterns "node_modules" ".git" "docs/legacy"
```

### Arguments:

*   `--path <directory>`: The root directory to start scanning from. Defaults to the current directory.
*   `--exclude-patterns <pattern1> <pattern2> ...`: A space-separated list of directory or file name patterns to exclude from the scan. For example, `"node_modules" ".git"`.
*   `--timeout <seconds>`: Timeout for HTTP requests in seconds. Defaults to 5.

## Example Output

```
Scanning for broken links in ../../...

Found broken links:

File: README.md
  - https://example.com/non-existent-page (Status: 404)
  - https://broken-domain.invalid (Error: ConnectionError)

File: agents/AGENTS.md
  - https://another-broken-link.org/old-spec (Status: 500)

Scan complete. Please review and fix the broken links.
```

## Development

### Dependencies

This utility requires `requests`.

```bash
pip install requests
```

### Running Tests

Navigate to the `utils/nightly-resource-scavenger/tests` directory and run `pytest` (or `python -m unittest`):

```bash
python -m unittest test_scavenger.py
```
