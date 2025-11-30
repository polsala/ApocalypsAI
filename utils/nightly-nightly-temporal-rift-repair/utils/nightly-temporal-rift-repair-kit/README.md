# Nightly Temporal Rift Repair Kit

## Description

The "Nightly Temporal Rift Repair Kit" is a whimsical yet crucial utility designed to mend the fabric of your repository's documentation. It scans specified markdown files for broken internal and external links, identifying "temporal rifts" that lead to nowhere. By ensuring all your documentation links are valid, this kit helps maintain a coherent and navigable knowledge base, preventing users from getting lost in the informational void.

## Features

*   Scans markdown files for both `[text](internal/path)` and `[text](http://external.link)` style links.
*   Validates internal file paths against the local filesystem.
*   Checks external URLs for reachability (HTTP 200 OK).
*   Provides a clear report of all broken links found.

## Usage

To use the Temporal Rift Repair Kit, run the `link_checker.py` script with the path to the directory containing your markdown files.

```bash
python src/link_checker.py --path /path/to/your/docs
```

### Arguments

*   `--path <directory>`: **Required**. The root directory to scan for markdown files.
*   `--ignore-patterns <pattern1> <pattern2> ...`: Optional. A space-separated list of glob patterns for files/directories to ignore during the scan (e.g., `node_modules/*`, `*.bak`).
*   `--timeout <seconds>`: Optional. Timeout for external link checks in seconds (default: 5).

## Example Output

```
Scanning directory: /path/to/your/docs

--- Checking file: /path/to/your/docs/README.md ---
  [OK] Internal link: docs/setup.md
  [BROKEN] Internal link: non-existent-file.md (File not found)
  [OK] External link: https://github.com/polsala/ApocalypsAI
  [BROKEN] External link: https://broken-link.example.com (HTTP Error: 404)

--- Checking file: /path/to/your/docs/agents/AGENTS.md ---
  [OK] Internal link: ../README.md
  [BROKEN] External link: https://another-broken-link.org (Connection Error)

Scan complete. Found 3 broken links in 2 files.
```
