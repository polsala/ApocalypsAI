# Nightly Data Dust Bunny Duster

## 🧹 Whimsical Digital Decluttering

Welcome to the Nightly Data Dust Bunny Duster! This utility is designed to help you keep your digital environment tidy by sniffing out those forgotten files (stale files) and identifying pesky duplicates that hog precious storage space. Think of it as a diligent, automated dust bunny, sweeping away the digital detritus that accumulates over time.

### ✨ Features

*   **Stale File Detection**: Identifies files that haven't been accessed or modified in a specified number of days.
*   **Duplicate File Finder**: Locates identical files based on their content (MD5 hash) after an initial size-based grouping.
*   **Comprehensive Reporting**: Provides a clear summary of identified stale and duplicate files.
*   **Optional Quarantine**: Safely moves identified files to a designated 'dustbin' directory for your review, rather than deleting them outright.

### 🚀 How to Use

This utility is a standalone Python script. No special installation is required beyond having Python 3.11+.

#### Basic Usage

To scan a directory and get a report:

```bash
python src/duster.py /path/to/your/directory
```

#### Finding Stale Files

Specify the number of days a file must be untouched to be considered 'stale'. For example, to find files not modified in the last 90 days:

```bash
python src/duster.py /path/to/your/directory --stale-days 90
```

#### Finding Duplicate Files

To enable duplicate file detection:

```bash
python src/duster.py /path/to/your/directory --find-duplicates
```

#### Quarantining Files

To move identified files to a 'dustbin' directory instead of just reporting them:

```bash
python src/duster.py /path/to/your/directory --stale-days 180 --find-duplicates --quarantine-dir /path/to/your/dustbin
```

**Note**: Files moved to the quarantine directory will have their original names preserved, but if a name conflict occurs, a unique suffix will be added.

### ⚙️ Arguments

*   `<directory>` (required): The root directory to scan.
*   `--stale-days <N>`: Integer. Files not modified in `N` days are considered stale. Default: `0` (disabled).
*   `--find-duplicates`: Flag. If present, the utility will search for duplicate files.
*   `--quarantine-dir <PATH>`: Path to a directory where identified files will be moved. If not provided, files are only reported.

### 💡 Example Output

```
Scanning /home/user/my_docs...

--- Stale Files (not modified in 90 days) ---
  - /home/user/my_docs/old_project/report_v1.pdf (Last modified: 2023-01-15)
  - /home/user/my_docs/archive/ancient_log.txt (Last modified: 2022-11-01)

--- Duplicate Files ---
  - Hash: a1b2c3d4e5f6...
    - /home/user/my_docs/photos/IMG_001.jpg
    - /home/user/my_docs/backup/IMG_001.jpg
  - Hash: f6e5d4c3b2a1...
    - /home/user/my_docs/docs/draft.docx
    - /home/user/my_docs/temp/draft_copy.docx

--- Summary ---
Found 2 stale files.
Found 2 groups of duplicate files (4 files total).
No files were quarantined.
```

Happy decluttering, fellow survivors!
