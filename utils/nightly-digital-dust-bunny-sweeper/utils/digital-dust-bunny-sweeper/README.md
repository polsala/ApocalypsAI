# Digital Dust Bunny Sweeper

## Overview

The Digital Dust Bunny Sweeper is a whimsical utility designed to help you declutter your digital space. It scans a specified directory for 'digital dust bunnies' – old, forgotten files and empty directories – and provides a charming report of its findings. Think of it as a tiny, automated Roomba for your filesystem, but with a flair for cosmic pronouncements.

## Features

*   **Empty Directory Detection**: Identifies and lists directories that contain no files or subdirectories.
*   **Ancient File Foraging**: Locates files older than a specified age threshold, focusing on common temporary or log file extensions.
*   **Whimsical Reporting**: Presents its findings in a delightful, easy-to-read format, making cleanup feel less like a chore and more like a cosmic quest.

## How to Use

1.  **Navigate**: Change into the `utils/digital-dust-bunny-sweeper/src` directory.
2.  **Run**: Execute the `sweeper.py` script with the target directory you wish to scan.

    ```bash
    python sweeper.py --path /path/to/your/directory [--age-days 90] [--extensions .log .tmp .bak]
    ```

    *   `--path`: (Required) The absolute or relative path to the directory you want to sweep.
    *   `--age-days`: (Optional) The age in days. Files older than this will be flagged. Defaults to 90 days.
    *   `--extensions`: (Optional) A space-separated list of file extensions to consider for age-based flagging (e.g., `.log`, `.tmp`). If not provided, common temporary extensions are used by default.

## Example Output

```
✨ Initiating Cosmic Debris Scan for: /home/user/my_project ✨

Scanning the astral plains of your filesystem...

--- Cosmic Debris Report ---

🌌 Empty Voids Discovered (Empty Directories):
  - /home/user/my_project/old_builds/empty_cache
  - /home/user/my_project/temp_logs/archive

⏳ Ancient Relics Unearthed (Old Files):
  - /home/user/my_project/logs/debug.log (Last modified: 2023-01-15)
  - /home/user/my_project/temp/temp_report.tmp (Last modified: 2023-02-01)

--- End of Report ---

🧹 A clean sweep for your cosmic data-verse! 🧹
```

## Development

This utility is written in Python 3.11 and uses only standard library modules, ensuring maximum compatibility and minimal overhead.

## Tests

To run the tests, navigate to the `utils/digital-dust-bunny-sweeper/tests` directory and execute:

```bash
python -m unittest test_sweeper.py
```
