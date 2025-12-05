# Nightly Web Weaver Repairman

The Nightly Web Weaver Repairman is a diligent ApocalypsAI utility designed to ensure the integrity of your repository's documentation. It tirelessly scans Markdown files for broken external hyperlinks, helping you maintain a pristine and reliable web of information. No more dead ends in your READMEs or AGENTS.md!

## Features

*   **Markdown Link Extraction**: Identifies external `[text](url)` links within `.md` files.
*   **HTTP Head Checks**: Efficiently pings URLs using HTTP HEAD requests to verify their availability.
*   **Broken Link Reporting**: Clearly lists all detected broken links (4xx, 5xx, or network errors).
*   **Repository-Wide Scan**: Recursively searches for Markdown files throughout the repository.

## Usage

To run the Web Weaver Repairman, execute the `link_checker.py` script from the repository root:

```bash
python3 -m utils.nightly-web-weaver-repairman.src.link_checker
```

The script will print any broken links it finds to standard output.

## Example Output

```
Scanning for broken links...
Found 2 .md files.
Checking link: https://example.com/non-existent-page (from README.md)
  Status: 404 Not Found
Checking link: https://broken-domain-that-does-not-exist.com (from AGENTS.md)
  Status: Connection Error: Max retries exceeded with url: ...

--- Broken Links Found ---
- README.md: https://example.com/non-existent-page (404 Not Found)
- AGENTS.md: https://broken-domain-that-does-not-exist.com (Connection Error)
```

## Development

The utility is written in Python 3.11 and uses the `requests` library.

### Running Tests

```bash
python3 -m unittest utils.nightly-web-weaver-repairman.tests.test_link_checker
```
