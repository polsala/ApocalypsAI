# Nightly Resource Scavenger

## Overview
The ApocalypsAI Nightly Resource Scavenger is a vigilant utility designed to combat digital decay by identifying and reporting broken external links within your repository's documentation and code comments. Like a diligent scavenger, it sifts through specified file types, ensuring that all referenced resources are still accessible and preventing the accumulation of dead ends in your digital landscape.

## Features
- Scans `.md` (Markdown) and `.py` (Python) files by default.
- Extracts HTTP/HTTPS URLs using regular expressions.
- Checks the status of each unique URL using efficient HTTP HEAD requests (with a GET fallback for servers that disallow HEAD).
- Reports broken links (e.g., 404 Not Found, 500 Server Error, connection errors, timeouts) along with their source file and line number.

## Usage
```bash
python src/scavenger.py --path ./ --extensions md py
```

### Arguments
- `--path <directory>`: The root directory to start scanning from. Defaults to the current directory (`.`).
- `--extensions <ext1> <ext2> ...`: A space-separated list of file extensions to scan (e.g., `md py txt`). Defaults to `md py`.

## Dependencies
This utility requires the `requests` Python library. It can be installed via pip:
```bash
pip install requests
```

## Example Output
```
Scanning directory: .
Looking for files with extensions: md, py
Found 5 URLs in 2 files.

Broken Links:
--------------------------------------------------
[404 NOT FOUND] https://example.com/non-existent-page (src/example.md:5)
[ERROR: Connection Error] https://api.broken.com/v1 (src/my_script.py:22)
--------------------------------------------------
Scan complete. 2 broken links found.
```
