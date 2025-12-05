# Nightly Ancient Echoes Link Checker

## Unearthing the Silent Screams of Broken Links

The digital landscape is ever-shifting, and what was once a vibrant pathway can quickly become a dead end. The "Nightly Ancient Echoes Link Checker" is your trusty archaeological tool, designed to scour your text files for URLs and report any that have fallen silent, ensuring your documentation and references remain as robust as the ancient pyramids.

### Purpose

This utility scans a specified text file (e.g., Markdown, plain text, code comments) for URLs and attempts to verify their reachability using HTTP HEAD requests. It helps maintain the integrity of your project's external links, preventing users from encountering frustrating "404 Not Found" errors.

### Usage

```bash
python src/detector.py --file <path_to_your_file>
```

**Example:**

```bash
python src/detector.py --file README.md
```

### Features

*   **URL Extraction:** Identifies URLs within various text formats.
*   **Reachability Check:** Performs non-intrusive HTTP HEAD requests to verify link status.
*   **Clear Reporting:** Provides a summary of good, broken, and unreachable links.
*   **Self-Contained:** Minimal dependencies, easy to integrate into any workflow.

### Installation

This utility requires `requests`. You can install it using pip:

```bash
pip install requests
```

### Development

To run tests:

```bash
python -m unittest tests/test_detector.py
```
