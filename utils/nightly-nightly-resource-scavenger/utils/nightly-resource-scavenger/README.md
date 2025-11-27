# Nightly Resource Scavenger

## Overview

The Nightly Resource Scavenger is a vigilant utility designed to maintain the integrity of your repository's documentation. It recursively scans Markdown files (`.md`) within a specified directory, extracts all external HTTP/HTTPS links, and then checks their availability. Broken links (those returning 4xx or 5xx HTTP status codes, or network errors) are reported, helping to ensure that your documentation remains accurate and reliable in the face of digital decay.

Think of it as a digital archaeologist, unearthing the forgotten paths and ensuring all connections still lead somewhere useful.

## Usage

To run the scavenger, provide the path to the directory you wish to scan:

```bash
python src/scavenger.py --path ./
```

Replace `./` with the target directory. The utility will print a report of all broken links found.

### Example Output

```
Scanning directory: ./
Found 2 Markdown files.

--- Broken Link Report ---

File: README.md
  - [Broken Link] https://example.com/non-existent-page (Status: 404 Not Found)
  - [Broken Link] https://api.example.org/down-service (Status: 500 Internal Server Error)

File: docs/guide.md
  - [Broken Link] https://old-docs.io/deprecated (Status: 410 Gone)

--- Scan Complete ---
Total broken links found: 3
```

## Development

### Requirements

*   Python 3.8+
*   `requests` library (`pip install requests`)

### Running Tests

Navigate to the utility's root directory and run `pytest`:

```bash
cd utils/nightly-resource-scavenger
pytest
```
