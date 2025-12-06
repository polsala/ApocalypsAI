# Nightly Data Dust-Bunny Detector

## 🧹 Overview

The Nightly Data Dust-Bunny Detector is a whimsical-yet-useful utility designed to help you keep your digital spaces tidy in the face of impending chaos. It scans specified directories for forgotten, old, or duplicate files – the digital "dust bunnies" that accumulate over time, consuming precious storage and mental bandwidth. Identify them, clean them, and prepare for a leaner, meaner post-apocalyptic data landscape!

## ✨ Features

*   **Age-based Detection**: Find files older than a specified number of days.
*   **Duplicate Detection**: Identify identical files based on their content hash.
*   **Comprehensive Reporting**: Generates a clear summary of detected dust bunnies.
*   **Non-Destructive**: Only reports findings; never deletes or modifies files.

## 🚀 Usage

```bash
python src/dust_bunny_detector.py <directory_path> [--age <days>] [--duplicates]
```

### Arguments:

*   `<directory_path>`: The root directory to scan.
*   `--age <days>`: (Optional) Detect files older than this many days.
*   `--duplicates`: (Optional) Detect duplicate files based on content hash.

### Examples:

Scan the current directory for files older than 90 days:
```bash
python src/dust_bunny_detector.py . --age 90
```

Scan your documents folder for duplicate files:
```bash
python src/dust_bunny_detector.py ~/Documents --duplicates
```

Scan your project folder for both old (30 days) and duplicate files:
```bash
python src/dust_bunny_detector.py ~/Projects/MyApocalypseProject --age 30 --duplicates
```

## 🛠️ Development

The detector is written in Python 3.11 and uses standard library modules.

### Running Tests

```bash
python -m unittest tests/test_dust_bunny_detector.py
```
