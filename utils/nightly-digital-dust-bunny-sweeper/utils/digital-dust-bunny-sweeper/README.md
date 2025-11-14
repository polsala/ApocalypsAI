# Digital Dust Bunny Sweeper

## Overview

The Digital Dust Bunny Sweeper is a whimsical yet practical utility designed to help you keep your project directories clean and free of forgotten cruft. It scans a specified directory for files that are either very old, match common temporary file patterns, or are simply deemed 'unused' based on a configurable age threshold. Think of it as a tiny, digital vacuum cleaner for your filesystem.

## Features

*   **Age-based Detection**: Identifies files older than a specified number of days.
*   **Pattern-based Detection**: Catches common temporary or junk files (e.g., `.tmp`, `.bak`, `~`, `.log`).
*   **Configurable**: Easily adjust the age threshold and add custom file patterns.
*   **Non-destructive**: Only reports findings; it never deletes files.

## How to Use

1.  **Navigate to the utility's directory**:
    ```bash
    cd utils/digital-dust-bunny-sweeper
    ```
2.  **Run the sweeper**: 
    Provide the target directory, an age threshold in days, and optional patterns.

    ```bash
    python src/sweeper.py --path /path/to/your/project --age 365 --patterns "\.tmp$" "\.bak$" "~$" "\.log$"
    ```

    *   `--path`: The directory to scan (e.g., `.` for current directory).
    *   `--age`: Files older than this many days will be flagged (e.g., `365` for files older than a year).
    *   `--patterns`: One or more regular expression patterns to match against filenames. Files matching any pattern will be flagged regardless of age. Default patterns are provided if none are specified.

## Example Output

```
Scanning /path/to/your/project for digital dust bunnies...

Found 3 digital dust bunnies:

- /path/to/your/project/old_report.csv (Reason: Older than 365 days, Last modified: 2022-01-15)
- /path/to/your/project/temp_file.tmp (Reason: Matches pattern: \.tmp$, Last modified: 2023-10-20)
- /path/to/your/project/subdir/backup.bak (Reason: Matches pattern: \.bak$, Last modified: 2023-09-01)

Consider reviewing these files for potential cleanup.
```
