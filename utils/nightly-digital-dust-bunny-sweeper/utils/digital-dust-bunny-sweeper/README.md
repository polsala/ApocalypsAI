# Digital Dust Bunny Sweeper

## 🧹 What is this?

The Digital Dust Bunny Sweeper is a whimsical-yet-useful utility designed to help you maintain a clean and tidy digital workspace. It scans a specified directory for 'digital dust bunnies' – specifically, empty directories and files that haven't been touched in a long, long time (older than a configurable threshold).

Think of it as a tiny, autonomous Roomba for your file system, but instead of vacuuming, it just politely points out what could be tidied up.

## ✨ Features

*   **Empty Directory Detection**: Finds and lists all empty subdirectories within a given path.
*   **Ancient File Identification**: Locates files older than a specified number of days, suggesting they might be forgotten relics.
*   **Configurable Threshold**: You decide how 'old' a file needs to be to qualify as a dust bunny.
*   **Non-Destructive**: This tool only *reports* findings; it never deletes or modifies any files.

## 🚀 How to Use

1.  Navigate to the `utils/digital-dust-bunny-sweeper/src` directory.
2.  Run the `sweeper.py` script with the target path and an optional age threshold in days.

```bash
python3 sweeper.py <path_to_scan> [--age-threshold <days>]
```

*   `<path_to_scan>`: The absolute or relative path to the directory you want to sweep.
*   `--age-threshold <days>`: (Optional) The number of days. Files older than this will be reported. Defaults to 90 days if not specified.

### Example:

To scan your current directory for files older than 180 days and empty folders:

```bash
python3 sweeper.py . --age-threshold 180
```

## 📊 Example Output

```
Scanning /home/user/my_project for digital dust bunnies...

--- Empty Directories Found ---
🧹 /home/user/my_project/old_build_artifacts/temp/
🧹 /home/user/my_project/empty_logs/

--- Ancient Files Found (older than 90 days) ---
⏳ /home/user/my_project/legacy_docs/old_spec.txt (Last modified: 2023-01-15)
⏳ /home/user/my_project/backup/archive_2022.zip (Last modified: 2022-11-01)

--- Sweeping Complete! ---
Your workspace is sparkling clean! No digital dust bunnies found.
```

*(Note: The final message will vary based on findings.)*
