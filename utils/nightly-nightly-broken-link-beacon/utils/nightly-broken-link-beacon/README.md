# Nightly Broken Link Beacon

## Overview

The 'Nightly Broken Link Beacon' is a whimsical yet essential utility designed to keep your repository's documentation pristine. It scans markdown files (`.md`) within a specified directory for external HTTP/HTTPS links and reports on their accessibility. Think of it as a vigilant lighthouse, signaling any broken connections in your documentation's vast ocean.

Broken links can degrade user experience and make documentation unreliable. This tool helps you proactively identify and fix them, ensuring your project's guides, references, and external resources are always up-to-date and reachable.

## Features

*   Scans all `.md` files in a given directory (and its subdirectories).
*   Extracts HTTP/HTTPS links from markdown `[text](url)` syntax.
*   Checks the HTTP status code for each external link.
*   Reports on successful (2xx), redirected (3xx), client error (4xx), server error (5xx), and connection error statuses.
*   Ignores local file paths and relative links.

## Usage

To run the beacon, navigate to the `nightly-broken-link-beacon` directory and execute the `link_checker.py` script. You can specify a target directory, or it will default to the current directory.

```bash
python src/link_checker.py --path /path/to/your/repo
```

**Example Output:**

```
Scanning directory: /path/to/your/repo

--- Checking links in README.md ---
[SUCCESS] https://example.com/valid-link (200 OK)
[BROKEN ] https://example.com/broken-link (404 Not Found)
[ERROR  ] https://nonexistent-domain.com/ (Connection Error)
[REDIRECT] https://old-site.com/ (301 Moved Permanently -> https://new-site.com/)

--- Checking links in docs/CONTRIBUTING.md ---
[SUCCESS] https://github.com/polsala/ApocalypsAI (200 OK)

Scan complete. Found 1 broken link(s) and 1 error(s).
```

## Installation

This utility requires `requests`.

```bash
pip install requests
```

## Development & Testing

Tests are located in the `tests/` directory and can be run using `pytest` (recommended) or `unittest`.

```bash
cd tests/
python -m unittest test_link_checker.py
```
