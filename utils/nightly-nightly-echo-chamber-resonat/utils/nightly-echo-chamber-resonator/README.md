# Nightly Echo Chamber Resonator

## 🌌 Resonate and Reveal Redundancy 🌌

The cosmos is vast, and sometimes, echoes of data reverberate through our file systems, creating unnecessary duplicates. The Nightly Echo Chamber Resonator is a whimsical yet powerful utility designed to detect these digital echoes, helping you identify and manage redundant files to declutter your storage.

It scans a specified directory, calculates cryptographic hashes for each file, and reports groups of files that share identical content.

## ✨ Features

*   **Duplicate Detection**: Identifies files with identical content using SHA256 hashing.
*   **Directory Traversal**: Recursively scans subdirectories.
*   **Clear Reporting**: Outputs a list of duplicate groups, showing all paths for each set of identical files.
*   **Self-Contained**: No external dependencies beyond standard Python libraries.

## 🚀 Usage

To run the Echo Chamber Resonator, simply execute the `resonator.py` script with the target directory as an argument:

```bash
python src/resonator.py /path/to/your/directory
```

### Example Output

```
🌌 Resonating for echoes in: /path/to/your/directory

Found 2 groups of duplicate files:

--- Group 1 (SHA256: a1b2c3d4e5f6...) ---
  - /path/to/your/directory/documents/report_v1.txt
  - /path/to/your/directory/archive/old_report.txt

--- Group 2 (SHA256: f6e5d4c3b2a1...) ---
  - /path/to/your/directory/images/logo.png
  - /path/to/your/directory/assets/branding/logo_copy.png

Resonation complete. Total 2 groups of echoes found.
```

## 🛠️ Development

The utility is written in Python 3.11 and uses standard library modules.

### Running Tests

To ensure the Echo Chamber Resonator is perfectly tuned, run its self-contained tests:

```bash
python -m unittest tests/test_resonator.py
```
