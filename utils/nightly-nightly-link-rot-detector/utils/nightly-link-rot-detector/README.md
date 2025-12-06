# Nightly Link Rot Detector

The ApocalypsAI Nightly Link Rot Detector is a crucial utility for maintaining the integrity of our documentation in the face of digital decay. It scans all Markdown files within a specified directory for external HTTP/HTTPS links and reports any that are broken, ensuring our knowledge base remains robust and accessible.

## Purpose

In the ever-shifting landscape of the internet, links can become stale, leading to "link rot." This utility acts as a digital scavenger, identifying and reporting these broken connections before they accumulate, helping to keep our repository's documentation accurate and reliable.

## How to Run

The utility is a Python 3.11 script.

```bash
python src/link_rot_detector.py <path_to_directory>
```

**Example:**

```bash
python src/link_rot_detector.py .
```

This will scan the current directory and its subdirectories for Markdown files and check their external links.

## Output

The script will print a report to `stdout`.
- If no broken links are found, it will print a success message.
- If broken links are found, it will list each file and the problematic URLs within it, along with their status (e.g., HTTP status code or error message).

**Example Output (broken links):**

```
Scanning directory: .

File: README.md
  - Broken Link: https://example.com/non-existent (Status: 404 Not Found)
  - Broken Link: https://another-broken.link/page (Status: Connection Error: Max retries exceeded)

File: docs/important.md
  - Broken Link: https://old-api.com/docs (Status: 500 Internal Server Error)

Summary: Found 3 broken links in 2 files.
```

**Example Output (no broken links):**

```
Scanning directory: .

All external links checked. No link rot detected. The digital garden is thriving!
```

## Development Notes

-   **Dependencies**: `requests`
-   **Link Detection**: Uses a simple regex to find `[text](http/https://...)` patterns.
-   **Network Calls**: Performs `HEAD` requests to minimize bandwidth. Timeouts are set to prevent indefinite hangs.
-   **Offline Tests**: The test suite uses `unittest.mock` to intercept and simulate network requests, ensuring tests are fast, deterministic, and do not rely on external services.
