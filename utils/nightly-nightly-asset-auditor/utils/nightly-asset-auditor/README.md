# Nightly Asset Auditor

A whimsical-yet-useful utility for the discerning digital hoarder. The Nightly Asset Auditor scans a specified directory, providing a comprehensive summary of its contents: total files, total size, and a breakdown of files by their extensions. Perfect for inventorying your digital treasures before the inevitable.

## Features

*   **Directory Scan:** Recursively traverses a given directory.
*   **File Count:** Reports the total number of files found.
*   **Total Size:** Calculates the cumulative size of all files.
*   **Extension Breakdown:** Categorizes and counts files by their file extensions (e.g., `.py`, `.md`, `.json`).
*   **Empty File Detection:** Identifies and counts files with zero bytes.
*   **Human-Readable Output:** Presents sizes in B, KB, MB, GB, TB.

## Usage

To run the auditor, simply provide the path to the directory you wish to audit:

```bash
python src/auditor.py /path/to/your/directory
```

### Example

```bash
python src/auditor.py .
```

This will output a report similar to this:

```
--- Asset Audit Report for: . ---
Total Files: 15
Total Size: 12.34 MB

Files by Extension:
  : 2
  .css: 1
  .js: 3
  .json: 2
  .md: 3
  .py: 4

Empty Files: 1
---------------------------------------
```

## Development

### Prerequisites

*   Python 3.6+

### Running Tests

To ensure the auditor is functioning correctly, navigate to the `utils/nightly-asset-auditor` directory and run the tests:

```bash
python -m unittest tests/test_auditor.py
```

## Contributing

Feel free to contribute by opening issues or pull requests.
