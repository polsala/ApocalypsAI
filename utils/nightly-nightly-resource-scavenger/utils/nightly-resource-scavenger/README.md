# Nightly Resource Scavenger

## Overview

The `nightly-resource-scavenger` is a vital utility in the ApocalypsAI arsenal, designed to ensure the integrity of external references within your repository's documentation and content files. In a world where digital resources can vanish without a trace, this tool acts as a diligent scavenger, identifying and reporting broken HTTP/HTTPS links in specified files (e.g., Markdown, HTML).

Keeping your links fresh and functional is crucial for maintaining reliable information pathways, even after the apocalypse.

## Usage

```bash
python src/scavenger.py --files README.md docs/guide.md
```

### Arguments

*   `--files <file1> <file2> ...`: One or more file paths to scan for broken links. Supports Markdown (`.md`), HTML (`.html`, `.htm`), and plain text files.

## Example Output

```
Scanning files for broken links...

File: README.md
  ✅ https://example.com/valid-link (200 OK)
  ❌ https://broken.link/404 (404 Not Found)

File: docs/guide.md
  ✅ https://another.valid.org (200 OK)

Scan complete. Found 1 broken link across 2 files.
```

## Development

### Requirements

*   Python 3.8+
*   `requests` library

### Installation

```bash
cd utils/nightly-resource-scavenger
pip install -r requirements.txt
```

### Running Tests

```bash
cd utils/nightly-resource-scavenger
python -m unittest tests/test_scavenger.py
```
