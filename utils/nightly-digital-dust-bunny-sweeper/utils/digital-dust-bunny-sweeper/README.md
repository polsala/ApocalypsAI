# Digital Dust Bunny Sweeper

## 🧹 What is this?

In the vast digital catacombs of your repository, forgotten files and empty folders accumulate like digital dust bunnies, silently consuming precious bytes and cluttering your workspace. The `Digital Dust Bunny Sweeper` is a whimsical-yet-useful utility designed to help you identify these digital detritus. It scans a specified directory for:

*   **Empty directories**: The hollow shells of forgotten features.
*   **Ancient files**: Files untouched for a configurable period (default: 365 days).
*   **Common temporary/log files**: The ephemeral remnants of builds and debugging sessions.

It won't delete anything (we're not *that* apocalyptic!), but it will provide a clear report, allowing you to decide which digital dust bunnies to banish to the void.

## ✨ Features

*   Scans a target directory recursively.
*   Identifies empty folders.
*   Flags files older than a specified age.
*   Detects common temporary file patterns.
*   Generates a human-readable report.

## 🚀 How to Use

1.  **Navigate** to the utility's directory:
    ```bash
    cd utils/digital-dust-bunny-sweeper/src
    ```
2.  **Run** the script, providing the path to the directory you want to sweep.
    ```bash
    python dust_bunny_sweeper.py /path/to/your/project
    ```
    (Replace `/path/to/your/project` with the actual path you want to scan.)

3.  **Optional arguments**:
    *   `--path <directory>`: The directory to scan (default: current directory).
    *   `--age <days>`: Files older than this many days will be flagged (default: 365).
    *   `--patterns <pattern1,pattern2,...>`: Comma-separated list of additional file patterns to flag (e.g., `*.log,*.tmp`).

    Example:
    ```bash
    python dust_bunny_sweeper.py --path ~/my_old_project --age 180 --patterns "*.bak,*.old"
    ```

## 📜 Example Output

```
Scanning /path/to/your/project for digital dust bunnies...

--- Digital Dust Bunny Report ---

🧹 Empty Directories:
  - /path/to/your/project/old_feature/empty_dir
  - /path/to/your/project/another_module/logs/archive

⏳ Ancient Files (older than 365 days):
  - /path/to/your/project/docs/old_spec.md (Last modified: 2022-01-15)
  - /path/to/your/project/src/legacy_code.py (Last modified: 2021-11-01)

🗑️ Temporary/Pattern-Matched Files:
  - /path/to/your/project/build/temp.log
  - /path/to/your/project/__pycache__/module.cpython-39.pyc
  - /path/to/your/project/.DS_Store

--- End Report ---
Found 5 digital dust bunnies. Time for a cleanup!
```
