# Nightly Temporal Rift Repair Kit

This utility, the 'Temporal Rift Repair Kit', is designed to ensure the integrity of your documentation by scanning Markdown files for broken links. It identifies both external URLs that are unreachable and internal file paths or anchors that no longer exist, helping to prevent 'temporal rifts' in your project's knowledge base.

## Usage

Run the script from the repository root to scan the entire repository:

```bash
python3 src/link_checker.py
```

Or specify a target directory to scan only a subset of files:

```bash
python3 src/link_checker.py --path ./docs
```

## Output

The script will print a JSON report to stdout, detailing any broken links found. If no broken links are found, it will print an empty JSON array `[]` and exit with code `0`. If broken links are found, it will print the report and exit with code `1`.

```json
[
  {
    "file": "README.md",
    "line": 10,
    "link_text": "broken external link",
    "url": "https://example.com/non-existent",
    "reason": "External link failed: 404 Not Found"
  },
  {
    "file": "docs/guide.md",
    "line": 5,
    "link_text": "missing internal file",
    "url": "./non-existent-file.md",
    "reason": "Internal file not found: /path/to/repo/docs/non-existent-file.md"
  },
  {
    "file": "docs/api.md",
    "line": 12,
    "link_text": "missing anchor",
    "url": "./api.md#missing-section",
    "reason": "Anchor '#missing-section' not found in '/path/to/repo/docs/api.md'"
  }
]
```

## Development

To run tests:

```bash
python3 -m unittest tests/test_link_checker.py
```
