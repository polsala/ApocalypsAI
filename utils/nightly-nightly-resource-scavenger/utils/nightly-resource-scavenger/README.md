# Nightly Resource Scavenger

## Overview

The `Nightly Resource Scavenger` is a vigilant utility designed to patrol your digital archives for signs of decay: broken or unreachable web links. In the post-apocalyptic landscape of information, dead links are a common blight. This tool helps you identify and mend them, ensuring your documentation, code comments, and configuration files remain connected to the living web.

It recursively scans a specified directory for text-based files (e.g., `.md`, `.txt`, `.py`, `.json`, `.yml`, `.xml`, etc.), extracts all HTTP/HTTPS URLs, and then attempts to reach each one. A report of all broken links is generated, allowing you to keep your repository's external references robust and reliable.

## Usage

To run the scavenger, simply provide the path to the directory you wish to scan:

```bash
python3 src/scavenger.py --path ./my_project_docs
```

### Arguments

*   `--path <directory>`: The root directory to start scanning for files and links. (Required)
*   `--file-extensions <ext1,ext2,...>`: Comma-separated list of file extensions to scan (e.g., `md,py,txt`). Defaults to common text/code files.
*   `--timeout <seconds>`: Timeout for each HTTP request in seconds. Defaults to 5 seconds.

## Example Output

```
Scanning directory: ./my_project_docs
Found 5 files to scan.
Found 3 unique URLs across all files.
Checking URL: https://example.com/valid-link (OK)
Checking URL: https://broken.link/page (Status: 404)
Checking URL: https://nonexistent.domain/resource (Error: ConnectionError)

--- Broken Links Report ---

https://broken.link/page (Source: ./my_project_docs/docs/guide.md) (Status: Status: 404)
https://nonexistent.domain/resource (Source: ./my_project_docs/src/config.py) (Status: Error: ConnectionError)

Scan complete. Found 2 broken links.
```
