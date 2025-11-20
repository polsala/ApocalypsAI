# Nightly Resource Scavenger

## Overview

The Nightly Resource Scavenger is a vigilant utility designed to comb through your repository's Markdown files (like `README.md`, documentation, etc.) and identify any broken or unreachable external links. In the post-apocalyptic digital landscape, ensuring your pathways to information remain intact is crucial. This tool helps maintain the integrity of your documentation, preventing dead ends and frustrating detours.

## Features

*   **Markdown Link Extraction**: Automatically finds all `[text](url)` style links within `.md` files.
*   **HTTP Status Checking**: Performs lightweight HEAD requests to verify the accessibility of each URL.
*   **Comprehensive Reporting**: Outputs a clear list of all broken links, including their source file and approximate line number.

## Usage

To run the scavenger, navigate to the `utils/nightly-resource-scavenger` directory and execute the `scavenger.py` script with the target directory as an argument.

```bash
python3 src/scavenger.py --path /path/to/your/repo
```

### Arguments

*   `--path <directory>`: The root directory to start scanning for Markdown files. Defaults to the current directory (`.`) if not provided.

## Example Output

```
Scanning directory: /path/to/your/repo
Found 2 Markdown files.

Checking links in file: docs/guide.md
  [Broken Link] https://example.com/non-existent (Status: 404) - Line 10
  [Broken Link] https://bad-domain.com (Status: Connection Error) - Line 15

Checking links in file: README.md
  All links are healthy.

Scan complete. Found 2 broken links.
```

## Development

### Dependencies

This utility requires `requests` and `markdown-it-py`.

```bash
pip install requests markdown-it-py
```

### Running Tests

Tests are located in the `tests/` directory. To run them, ensure you have `pytest` installed (or use `python -m unittest`):

```bash
pip install pytest
pytest tests/
```
