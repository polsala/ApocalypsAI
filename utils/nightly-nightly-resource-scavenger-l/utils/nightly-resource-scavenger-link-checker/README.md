# Nightly Resource Scavenger Link Checker

The ApocalypsAI Nightly Resource Scavenger Link Checker is a whimsical-yet-useful utility designed to prevent "link rot" in your documentation. It scours specified Markdown files for external HTTP/HTTPS links and verifies their accessibility, reporting any broken connections. Keep your resources fresh, even as the world crumbles around us!

## Usage

Run the `link_checker.py` script with the paths to the Markdown files you want to scan.

```bash
python src/link_checker.py path/to/README.md path/to/AGENTS.md
```

### Example Output

```
Scanning: path/to/README.md
  [✓] https://github.com/polsala/ApocalypsAI
  [✗] https://broken-link.example.com (Status: 404 Not Found)
  [✗] https://another-broken.example.org (Error: Connection refused)

Scanning: path/to/AGENTS.md
  [✓] https://docs.python.org/3/
```

## Features

*   Extracts HTTP/HTTPS links from Markdown files.
*   Checks link status (200 OK, 4xx Client Error, 5xx Server Error, connection issues).
*   Provides clear, actionable output for broken links.

## Installation

This utility is self-contained and requires Python 3.11+.
It uses the `requests` library, which can be installed via pip:

```bash
pip install requests
```
