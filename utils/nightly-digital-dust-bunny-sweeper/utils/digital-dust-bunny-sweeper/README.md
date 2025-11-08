# Digital Dust Bunny Sweeper

## 🧹 Overview

The Digital Dust Bunny Sweeper is a whimsical yet practical utility designed to help you declutter your digital workspace. It scans specified directories for "digital dust bunnies" – old, forgotten files and empty folders – and provides options to report or remove them. Keep your repository clean and your mind clear!

## ✨ Features

*   **Aged File Detection**: Identifies files that haven't been modified for a configurable period (default: 90 days).
*   **Empty Directory Cleanup**: Finds and lists directories that contain no files or subdirectories.
*   **Report Mode**: Lists all identified dust bunnies without making any changes.
*   **Cleanup Mode**: Safely removes identified dust bunnies after confirmation.

## 🚀 Usage

### Prerequisites

*   Python 3.8+ (tested with 3.11)

### Installation (Standalone)

1.  Navigate to the `utils/digital-dust-bunny-sweeper/` directory.
2.  You can run the script directly.

### Running the Sweeper

```bash
python src/sweeper.py --path <directory_to_scan> [options]
```

#### Arguments:

*   `--path <directory>` (required): The root directory to scan for dust bunnies.
*   `--age <days>` (optional): Files older than this many days will be considered dust bunnies. Default is 90 days.
*   `--report-only` (optional): If set, the utility will only report findings and not delete anything. This is the default behavior if `--delete` is not specified.
*   `--delete` (optional): If set, the utility will prompt for confirmation before deleting identified dust bunnies. **Use with caution!**
*   `--verbose` (optional): Print more detailed output during scanning.

#### Examples:

1.  **Report dust bunnies in the current directory (default 90 days age):**
    ```bash
    python src/sweeper.py --path . --report-only
    ```

2.  **Report dust bunnies in a specific folder, older than 30 days:**
    ```bash
    python src/sweeper.py --path /path/to/my/project --age 30 --report-only
    ```

3.  **Delete dust bunnies in a folder, older than 180 days (with confirmation):**
    ```bash
    python src/sweeper.py --path /path/to/downloads --age 180 --delete
    ```

## ⚠️ Safety First!

Always run with `--report-only` first to review what will be deleted before using the `--delete` flag. The `--delete` flag will prompt for confirmation before proceeding.
