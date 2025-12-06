# Nightly Data Debris Collector

## Purpose
This utility, the 'Nightly Data Debris Collector', helps maintain the integrity of your repository's external links. It scans specified file types (e.g., Markdown, Python source, plain text) for URLs and checks if they are still reachable. Broken links are reported, allowing you to clean up outdated references and prevent 'link rot'.

## How it Works
1.  **File Scanning**: Traverses the repository (or a specified directory) to find files with common extensions (`.md`, `.py`, `.txt`).
2.  **URL Extraction**: Uses regular expressions to identify potential URLs within the file content, including Markdown link syntax `[text](url)` and raw `http(s)://` patterns.
3.  **Link Validation**: For each extracted URL, it attempts to make a `HEAD` request (or `GET` if `HEAD` is not supported) to check its reachability. A short timeout is used to prevent long delays.
4.  **Reporting**: Compiles a list of all broken or unreachable URLs, along with the file paths where they were found.

## Usage
```bash
python src/collector.py --path <directory_to_scan> [--file-types <ext1,ext2>] [--timeout <seconds>]
```

**Example:**
```bash
python src/collector.py --path . --file-types md,py
```

## Output
The utility prints broken links to `stdout` in a human-readable format, indicating the file and the broken URL. If broken links are found, the script exits with code `1`; otherwise, it exits with `0`.

```
Scanning '.' for broken links in ['md', 'py'] files with a 5.0s timeout...

--- Broken Links Found ---
Broken Link in path/to/file.md: https://broken.example.com/page
Broken Link in another/file.py: https://nonexistent.org/
--- End of Report ---
```
