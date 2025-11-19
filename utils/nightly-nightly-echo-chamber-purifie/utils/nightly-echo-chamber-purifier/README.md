# Nightly Echo Chamber Purifier

## 🌌 Purpose

The Nightly Echo Chamber Purifier is a whimsical yet highly practical utility designed to combat digital redundancy. In the post-apocalyptic landscape of our data, duplicate files can silently consume precious storage and introduce confusion. This tool scans a specified directory, calculates SHA256 hashes for all files, and reports groups of identical files, helping you identify and clean up your digital "echo chambers."

## ✨ Features

*   **Recursive Scanning**: Traverses subdirectories to find duplicates anywhere within the target path.
*   **SHA256 Hashing**: Uses robust cryptographic hashing to ensure accurate duplicate detection.
*   **Clear Reporting**: Presents duplicate files grouped by their identical content, making cleanup straightforward.
*   **Self-Contained**: No external dependencies beyond standard Python libraries.

## 🚀 Usage

1.  **Navigate**: Change into the `src` directory of this utility:
    ```bash
    cd utils/nightly-echo-chamber-purifier/src
    ```
2.  **Run**: Execute the `purifier.py` script, providing the path to the directory you wish to scan:
    ```bash
    python purifier.py --directory /path/to/your/data
    ```
    Replace `/path/to/your/data` with the actual directory you want to analyze.

### Example Output:

```
Scanning for duplicates in: /path/to/your/data
---
Found 2 groups of duplicate files:

Group 1 (Hash: a1b2c3d4e5f6...)
  - /path/to/your/data/documents/report_v1.txt
  - /path/to/your/data/archives/old_report.txt

Group 2 (Hash: f6e5d4c3b2a1...)
  - /path/to/your/data/images/logo.png
  - /path/to/your/data/backup/logo_copy.png
---
Scan complete.
```

## 🛠️ Development & Testing

This utility is written in Python 3.11 and uses standard library modules.

To run tests:

1.  **Navigate**: Change into the `tests` directory:
    ```bash
    cd utils/nightly-echo-chamber-purifier/tests
    ```
2.  **Run Tests**: Execute the test suite using `pytest` (if installed) or `python -m unittest`:
    ```bash
    python -m unittest test_purifier.py
    ```
    The tests are designed to be deterministic and offline, using mocks for file system operations.
