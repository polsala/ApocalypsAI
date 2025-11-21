# Nightly Resource Scavenger

The digital landscape is ever-shifting, and even the most robust documentation can fall victim to link rot. The Nightly Resource Scavenger is here to help! This utility diligently patrols your repository, sniffing out broken external and internal links within your Markdown files.

It's like a digital bloodhound, ensuring that every reference, every pointer, and every path in your documentation leads somewhere meaningful, not into the void. Keep your knowledge base pristine and your readers informed, even as the apocalypse looms.

## Usage

Run the scavenger from your repository root:

```bash
python src/scavenger.py --repo .
```

The utility will scan all `.md` files, check their links, and report any broken ones to standard output. If any broken links are found, the utility will exit with a non-zero status code.

## Features

*   **External Link Validation**: Uses HTTP HEAD requests to check the reachability of external URLs.
*   **Internal Link Validation**: Verifies if relative file paths and anchor links within the repository exist.
*   **Comprehensive Scanning**: Recursively searches for `.md` files from the specified root directory.
*   **Detailed Reporting**: Provides file paths, line numbers, and the broken link itself for easy remediation.

## Development

### Requirements

*   Python 3.8+
*   `requests` library (`pip install requests`)

### Running Tests

```bash
python -m unittest tests/test_scavenger.py
```
