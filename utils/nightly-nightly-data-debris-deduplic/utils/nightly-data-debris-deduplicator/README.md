# Nightly Data Debris Deduplicator

## 🗑️ Overview

In the post-apocalyptic digital landscape, data debris accumulates fast! The `Nightly Data Debris Deduplicator` is a whimsical-yet-useful utility designed to help you clean up your digital wasteland by identifying and reporting duplicate files across your directories. By calculating SHA256 hashes of file contents, this tool ensures you're only keeping the truly unique data, freeing up precious storage and reducing clutter.

Think of it as your personal digital scavenger, sifting through the rubble to find redundant copies and help you maintain a lean, efficient data hoard.

## ✨ Features

*   **Content-Based Deduplication**: Identifies duplicates by comparing file content hashes (SHA256), not just names or sizes.
*   **Recursive Scanning**: Traverses subdirectories to find duplicates anywhere within the specified path.
*   **Symlink Awareness**: Skips symbolic links to prevent infinite loops and incorrect reporting.
*   **Simple CLI**: Easy to run from your terminal with a single directory argument.
*   **Language Agnostic**: Works on any file type, as it only cares about the raw byte content.

## 🚀 How to Use

1.  **Navigate to the utility's directory**:
    ```bash
    cd utils/nightly-data-debris-deduplicator
    ```

2.  **Run the deduplicator**:
    Provide the path to the directory you want to scan.

    ```bash
    python src/deduplicator.py /path/to/your/data/hoard
    ```

    Replace `/path/to/your/data/hoard` with the actual directory you wish to scan.

### Example Output

```
Scanning '/path/to/your/data/hoard' for duplicate files...

--- Duplicate File Groups Found ---

Hash: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2
  - /path/to/your/data/hoard/documents/report_v1.txt
  - /path/to/your/data/hoard/backups/old_reports/report_v1_copy.txt

Hash: f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9
  - /path/to/your/data/hoard/images/sunset.jpg
  - /path/to/your/data/hoard/photos/archive/sunset_copy.jpg
  - /path/to/your/data/hoard/downloads/temp/sunset.jpg

--- End of Duplicates ---
Found 2 groups of duplicate files.
```

If no duplicates are found, you'll see a message indicating your data debris is pristine!

## 🧪 Testing

To ensure the deduplicator is working correctly and reliably, you can run its self-contained tests:

1.  **Navigate to the utility's directory**:
    ```bash
    cd utils/nightly-data-debris-deduplicator
    ```
2.  **Run the tests**: 
    ```bash
    python -m unittest tests/test_deduplicator.py
    ```

The tests use mocking to simulate file system interactions, ensuring they are deterministic and do not require actual files or network access.
