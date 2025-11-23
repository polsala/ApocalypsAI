# Nightly Resource Scavenger

## Overview
In the digital wasteland, resources are scarce and connections can break. The Nightly Resource Scavenger is a vigilant utility designed to scour your repository's Markdown files for any broken external links. It ensures that your documentation, guides, and references remain reliable, preventing users from stumbling upon dead ends in their quest for knowledge.

## Features
- Scans Markdown files (`.md`, `.markdown`) for HTTP/HTTPS links.
- Checks the reachability of each external link.
- Reports broken links with their status codes.
- Configurable scan directory.

## Installation
This utility requires Python 3.8+ and the following packages:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/scavenger.py --path <directory_to_scan>
```

### Example
To scan the current directory and its subdirectories:
```bash
python src/scavenger.py --path .
```

## Output
The scavenger will print a report to standard output, listing all checked links and any identified broken links.

```
Scanning directory: .

Processing file: README.md
  Checking: https://example.com/valid-link (Status: 200 OK)
  Checking: https://example.com/broken-link (Status: 404 Not Found)

--- Scan Summary ---
Total links checked: 2
Broken links found: 1

Broken Links:
- https://example.com/broken-link (404 Not Found)
```
