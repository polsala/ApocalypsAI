# Nightly Echo Locator

## 📡 Locate Redundant Data in the Digital Wasteland

The Nightly Echo Locator is a crucial utility for the discerning survivor, designed to scan your digital territories for redundant data. In a world where every byte counts, why hoard duplicates? This tool helps you identify identical files across specified directories, allowing you to reclaim precious storage and streamline your data reserves.

### Features

*   **Recursive Scanning**: Delves deep into directory structures to find all files.
*   **Content-Based Hashing**: Uses SHA256 to ensure true content duplication detection, not just name or size.
*   **Clear Reporting**: Presents a grouped list of duplicate files, showing all instances of each unique duplicate set.
*   **Self-Contained**: No external dependencies beyond standard Python libraries.

### Usage

```bash
python src/echo_locator.py <path1> [path2 ...]
```

**Example:**

```bash
python src/echo_locator.py ./my_data /mnt/backup_drive
```

This will scan `./my_data` and `/mnt/backup_drive` for duplicate files and print a report to the console.

### Output Format

The tool will print groups of duplicate files. Each group represents a set of files that have identical content.

```
--- Duplicate Group (SHA256: <hash_value>) ---
  Size: <file_size> bytes
  - /path/to/first/duplicate/file.txt
  - /path/to/second/duplicate/file.txt
  - /path/to/another/duplicate/file.txt
---
```

### Development

To run tests:

```bash
python -m unittest tests/test_echo_locator.py
```
