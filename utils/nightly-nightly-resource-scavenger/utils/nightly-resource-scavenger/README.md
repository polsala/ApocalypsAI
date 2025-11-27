# Nightly Resource Scavenger

## Purpose

The Nightly Resource Scavenger is a whimsical-yet-useful utility designed to roam the digital wasteland of your repository, sniffing out broken external links in Markdown files. In the post-apocalyptic landscape of code, even documentation can decay. This tool ensures your READMEs, AGENTS.md, and other Markdown documents point to valid, accessible resources.

## Usage

To run the scavenger, simply execute the `scavenger.py` script with the `--root-dir` argument, specifying the directory to start scanning from. It will recursively search for Markdown files (`.md`, `.markdown`) and check all `http(s)://` links found within them.

```bash
python3 src/scavenger.py --root-dir .
```

### Arguments

*   `--root-dir <path>`: The root directory from which to start scanning for Markdown files. (Required)
*   `--file-extensions <ext1> <ext2> ...`: Optional. A space-separated list of file extensions to scan (e.g., `.md .markdown`). Defaults to `.md .markdown`.

## Output

The scavenger will print a list of all broken links it finds, along with the file path where they were discovered and the reason for their failure (e.g., HTTP 404, connection error, timeout).

```
Scanning directory: .
Checking file: README.md
  [BROKEN] https://example.com/non-existent-page (Status: 404 Not Found)
  [BROKEN] https://broken.link/timeout (Error: Connection timed out)
Checking file: agents/AGENTS.md
  [OK] https://github.com/polsala/ApocalypsAI

--- Scan Complete ---
Found 2 broken links.
```

## How it Works

1.  **File Discovery**: Recursively walks the specified `--root-dir` to find files matching the configured Markdown extensions.
2.  **Link Extraction**: Uses regular expressions to find `[text](url)` patterns in the file content, specifically targeting `http(s)://` URLs.
3.  **Link Validation**: For each extracted URL, it performs a `HEAD` request (or `GET` if `HEAD` is not allowed by the server) to check its HTTP status code. It considers 2xx status codes as valid and anything else (4xx, 5xx, connection errors, timeouts) as broken.

## Development

This utility is written in Python 3.11 and uses the `requests` library for HTTP requests. Tests are located in `tests/test_scavenger.py` and use `unittest` with `unittest.mock` for deterministic, offline testing.
