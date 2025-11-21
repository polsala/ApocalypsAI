# Nightly Digital Dust Bunny Detector

## 🧹 Overview

The Nightly Digital Dust Bunny Detector is a whimsical-yet-useful utility designed to help you keep your digital spaces tidy. It scans specified directories for two common forms of "digital dust bunnies":

1.  **Empty Directories**: Folders that contain no files or subdirectories.
2.  **Duplicate Files**: Files that have identical content, identified by their SHA256 hash.

By identifying these, the detector provides a clear report, empowering you to declutter your project repositories and file systems, saving space and reducing cognitive load.

## ✨ Features

*   **Empty Directory Detection**: Quickly lists all empty folders within a given path.
*   **Duplicate File Identification**: Finds files with identical content, regardless of their name or location.
*   **SHA256 Hashing**: Uses robust SHA256 checksums for reliable content comparison.
*   **Clear Reporting**: Outputs findings in an easy-to-read format.

## 🚀 Usage

To run the detector, simply execute the `detector.py` script with the target directory as an argument:

```bash
python src/detector.py /path/to/your/directory
```

### Example Output

```
Scanning /path/to/your/directory for digital dust bunnies...

--- Empty Directories Found ---
- /path/to/your/directory/empty_folder_1
- /path/to/your/directory/another_empty_dir/sub_empty

--- Duplicate Files Found ---
- Group 1 (SHA256: a1b2c3d4e5f6...)
  - /path/to/your/directory/file_a.txt
  - /path/to/your/directory/backup/file_a_copy.txt
- Group 2 (SHA256: f6e5d4c3b2a1...)
  - /path/to/your/directory/images/logo.png
  - /path/to/your/directory/assets/old_logo.png

Scan complete. Time to sweep! 🧹
```

## 🛠️ Development

### Requirements

*   Python 3.6+ (tested with 3.11)

### Running Tests

Tests are self-contained and use `unittest`. Navigate to the utility's root directory and run:

```bash
python -m unittest tests/test_detector.py
```
