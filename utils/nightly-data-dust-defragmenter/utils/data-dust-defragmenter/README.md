# Data-Dust Defragmenter

## 🧹 Clear the Digital Rubble!

The ApocalypsAI Nightly Integrator presents the **Data-Dust Defragmenter**! In the post-apocalyptic digital landscape, every byte counts. This utility helps you identify and manage the "data dust" – old, large, or duplicate files – cluttering your precious storage. Think of it as a digital scavenger hunt for wasted space, helping you keep your data lean and mean for the next system crash.

## ✨ Features

*   **Age Analysis**: Pinpoint files older than a specified number of days.
*   **Size Scrutiny**: Highlight files exceeding a certain size threshold.
*   **Duplicate Detection**: Uncover identical files lurking in different corners of your directory, using content hashing.
*   **Clear Reporting**: Provides a concise summary of potential "dust bunnies" found.

## 🚀 Usage

1.  Navigate to the `utils/data-dust-defragmenter` directory.
2.  Run the script with the target directory and optional parameters:

    ```bash
    python src/defragmenter.py --path /path/to/scan --old-days 365 --min-size-mb 100 --find-duplicates
    ```

    *   `--path <directory>`: **Required**. The directory to scan.
    *   `--old-days <int>`: Optional. Report files older than this many days.
    *   `--min-size-mb <int>`: Optional. Report files larger than this many megabytes.
    *   `--find-duplicates`: Optional. Enable duplicate file detection (can be slow for very large directories).

### Example:

To scan your current directory for files older than 180 days, larger than 50MB, and duplicates:

```bash
python src/defragmenter.py --path . --old-days 180 --min-size-mb 50 --find-duplicates
```

## 🛠️ Development

This utility is written in Python 3.11 and uses only standard library modules.

### Running Tests

```bash
python -m unittest tests/test_defragmenter.py
```
