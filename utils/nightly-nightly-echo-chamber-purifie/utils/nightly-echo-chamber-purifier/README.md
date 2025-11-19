# Nightly Echo Chamber Purifier

## 🌌 What it does

The Nightly Echo Chamber Purifier is a whimsical utility designed to silence the echoes of redundant data within your file system. It scans a specified directory, calculates cryptographic hashes for each file's content, and then reports any files that are exact duplicates. Think of it as a digital librarian that helps you declutter your archives, ensuring every byte has a unique voice.

## ✨ Why it's useful

*   **Disk Space Reclamation**: Easily identify and remove unnecessary copies of files, freeing up valuable storage.
*   **Data Integrity**: Helps maintain a cleaner, more organized repository or project directory by highlighting unintended duplications.
*   **Efficiency**: Avoids processing or backing up the same data multiple times.

## 🚀 How to use it

1.  **Navigate**: Change into the `nightly-echo-chamber-purifier` directory.
2.  **Run**: Execute the `purifier.py` script with the target directory as an argument.

    ```bash
    python3 src/purifier.py /path/to/your/directory
    ```

    Replace `/path/to/your/directory` with the actual path you want to scan.

### Example Output

```
Scanning /path/to/my/project for duplicates...

Found 2 groups of duplicate files:

--- Group 1 (Hash: a1b2c3d4e5f6...)
  - /path/to/my/project/docs/report_v1.pdf
  - /path/to/my/project/archive/old_report.pdf

--- Group 2 (Hash: f6e5d4c3b2a1...)
  - /path/to/my/project/images/logo_copy.png
  - /path/to/my/project/assets/logo.png

Scan complete. Consider reviewing and removing duplicate files.
```

## 🛠️ Development

### Dependencies

This utility uses only standard Python 3.11 libraries (`os`, `hashlib`, `argparse`). No external dependencies are required.

### Running Tests

To ensure the purifier is working correctly, run the provided tests:

```bash
python3 -m unittest tests/test_purifier.py
```
