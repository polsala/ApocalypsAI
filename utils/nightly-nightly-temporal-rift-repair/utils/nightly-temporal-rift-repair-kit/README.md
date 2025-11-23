# Nightly Temporal Rift Repair Kit

## Purpose

The ApocalypsAI project thrives on clear, accessible documentation. Over time, external links in `README.md`, `AGENTS.md`, and other Markdown files can become outdated or broken, creating 'temporal rifts' in our collective knowledge. The Nightly Temporal Rift Repair Kit is designed to automatically scan specified directories for Markdown files, extract all external URLs, and verify their reachability.

By identifying and reporting broken links, this utility helps maintain the integrity and reliability of our documentation, ensuring that all references lead to valid destinations.

## Usage

To run the Temporal Rift Repair Kit, execute the `link_checker.py` script with the path to the directory you wish to scan.

```bash
python src/link_checker.py --path <directory_to_scan>
```

### Example:

To scan the entire repository for broken links in Markdown files:

```bash
python src/link_checker.py --path .
```

### Output:

The script will print a report to `stdout` listing any broken or unreachable links found, along with the file they were found in and the HTTP status code (if applicable).

```
Scanning directory: .

File: README.md
  [BROKEN] https://example.com/non-existent (Status: 404)
  [ERROR] https://unreachable-domain.com (Error: Connection Error)

File: AGENTS.md
  [BROKEN] https://old-spec.dev/v1 (Status: 404)

Scan complete. Found 3 broken/unreachable links.
```

### Exit Codes:

*   `0`: No broken or unreachable links found.
*   `1`: One or more broken or unreachable links found.

## Development

### Dependencies

This utility requires `requests`.

```bash
pip install requests
```

### Testing

Tests are located in `tests/test_link_checker.py` and can be run using `unittest`.

```bash
python -m unittest tests/test_link_checker.py
```
