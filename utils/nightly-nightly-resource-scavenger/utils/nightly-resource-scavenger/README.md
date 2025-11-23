# Nightly Resource Scavenger

## Overview

The `nightly-resource-scavenger` is a whimsical-yet-useful utility designed to help maintain the health of your repository's external links. Like a diligent scavenger in a post-apocalyptic wasteland, it roams through your files, identifying external URLs and verifying their reachability. This ensures that your documentation, code comments, and other textual assets don't point to broken or defunct resources.

## Features

*   **Link Discovery**: Automatically finds URLs in Markdown files (`[text](url)` format) and raw URLs in various text-based files (e.g., `.md`, `.py`, `.txt`).
*   **Reachability Check**: Performs HTTP HEAD requests to verify if discovered URLs return a successful status code (2xx). Falls back to GET for client errors (4xx) if HEAD is blocked.
*   **Error Reporting**: Clearly reports broken links, including their source file, line number, and the HTTP status code or error encountered.
*   **Flexible Scanning**: Can scan individual files or entire directories, with options to exclude specific paths.

## Usage

To run the scavenger, navigate to the `utils/nightly-resource-scavenger/` directory and execute the `scavenger.py` script.

```bash
python src/scavenger.py --path <file_or_directory> [--exclude <pattern>]
```

### Arguments:

*   `--path <file_or_directory>` (required): The file or directory path to scan for URLs. If a directory, it will be traversed recursively.
*   `--exclude <pattern>` (optional): A glob-style pattern (e.g., `*.log`, `temp_dir/*`) to exclude files or directories from the scan. Can be specified multiple times.

### Examples:

Scan a single Markdown file:

```bash
python src/scavenger.py --path README.md
```

Scan the entire `docs/` directory:

```bash
python src/scavenger.py --path docs/
```

Scan the current directory, excluding `node_modules` and `.git` directories:

```bash
python src/scavenger.py --path . --exclude "node_modules/*" --exclude ".git/*"
```

Scan Python files in `agents/` but exclude `test_*.py` files:

```bash
python src/scavenger.py --path agents/ --exclude "*test_*.py"
```

## Output

The utility prints its findings to standard output. Successful checks are noted, and broken links are highlighted with details.

```
Scanning: README.md
  [OK] https://example.com/valid-link (Found in README.md:3)
  [BROKEN] https://example.com/broken-link (404 Not Found) (Found in README.md:5)
  [ERROR] https://nonexistent-domain.com (Connection Error) (Found in README.md:7)

Scanning: src/agent.py
  [OK] https://docs.python.org/3/library/os.html (Found in src/agent.py:1)

Scan complete. Found 2 broken links.
```
