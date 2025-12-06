# Nightly Digital Debris Detector

## 🧹 What is this?

The Nightly Digital Debris Detector is your personal post-apocalyptic scavenger, designed to help you maintain a pristine and efficient repository. It meticulously scans your project for 'digital debris' – specifically, untracked files (those not managed by Git) and empty directories. Think of it as a clean-up crew for the digital wasteland, ensuring no forgotten files or hollow structures linger.

## ✨ Features

- **Untracked File Detection**: Identifies files that are present in your working directory but are not tracked by Git, helping you spot forgotten temporary files, build artifacts, or files that should be added to `.gitignore`.
- **Empty Directory Identification**: Locates and reports directories that contain no files or subdirectories, perfect for cleaning up after refactoring or failed operations.
- **Whimsical Reporting**: Presents its findings in a clear, actionable, yet slightly whimsical report.

## 🚀 How to Run

This utility is designed to be run from the root of a Git repository.

```bash
python3 src/detector.py <path_to_repository>
```

**Example:**

```bash
python3 src/detector.py .
```

This will print a report of detected debris to the console.

## 🛠️ Development

### Requirements

- Python 3.11+
- Git (must be available in PATH)

### Running Tests

```bash
python3 -m pytest tests/test_detector.py
```

## 📜 Output Example

```
--- Digital Debris Report ---

Scanning repository: /path/to/your/repo

🗑️ Untracked Files (Forgotten Relics):
  - temp/log.txt
  - build/output.tmp

🕳️ Empty Directories (Hollow Ruins):
  - empty_folder/
  - another_empty_dir/

--- End of Report ---
```
