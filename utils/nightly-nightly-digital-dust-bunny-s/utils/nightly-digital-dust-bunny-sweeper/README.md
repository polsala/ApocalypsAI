# Nightly Digital Dust Bunny Sweeper

## 🧹 Clean Up the Digital Rubble!

The ApocalypsAI Nightly Integrator presents the **Digital Dust Bunny Sweeper**! In the post-apocalyptic digital landscape, clutter accumulates like radioactive fallout. This utility helps you identify and sweep away those pesky, old, and forgotten files – your digital "dust bunnies" – from specified directories, reclaiming precious disk space and bringing order to the chaos.

## ✨ Features

*   **Targeted Sweeping**: Specify one or more directories to scan.
*   **Age-Based Filtering**: Only target files older than a configurable number of days.
*   **Interactive Deletion**: Review identified files and confirm deletion, or run in dry-run mode.
*   **Recursive Scan**: Dives deep into subdirectories to find hidden clutter.

## 🚀 Usage

```bash
python src/sweeper.py --path /path/to/scan1 --path /path/to/scan2 --older-than 30 --dry-run
```

### Arguments:

*   `--path <directory>`: (Required, can be specified multiple times) The directory to scan for old files.
*   `--older-than <days>`: (Optional, default: 90) Only consider files older than this many days.
*   `--dry-run`: (Optional) Perform a scan and list files, but do not delete anything.
*   `--confirm-delete`: (Optional) Automatically confirm deletion of all found files without prompting. **Use with caution!**

## 🛠️ Development

### Setup

```bash
# Navigate to the utility's root directory
cd utils/nightly-digital-dust-bunny-sweeper/

# No special dependencies beyond standard Python 3.x libraries.
```

### Running Tests

```bash
# Navigate to the utility's root directory
cd utils/nightly-digital-dust-bunny-sweeper/
python -m unittest tests/test_sweeper.py
```

## ⚠️ Warning

Always use the `--dry-run` option first to review what will be deleted. The `--confirm-delete` option will delete files without further prompting, which can lead to data loss if used carelessly. ApocalypsAI is not responsible for files swept into the digital void!
