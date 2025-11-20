# Nightly Digital Dust Bunny Sweeper

## 🧹 What is this?

The Digital Dust Bunny Sweeper is a whimsical utility designed to help you keep your digital workspace clean and free of clutter. Just like real dust bunnies accumulate in forgotten corners, digital 'dust bunnies' – empty directories and potentially stale, small files – can build up in your project folders, making navigation harder and wasting precious disk space.

This tool scans a specified directory and reports on these digital nuisances, helping you identify areas for cleanup. For now, it's a reporting tool, not a deleter, ensuring you have full control over what gets 'swept away'.

## ✨ Features

*   **Empty Directory Detection**: Identifies and lists all truly empty subdirectories within a given path (those containing no files and no subdirectories).
*   **Stale File Identification**: Flags files that are older than a specified age (e.g., 30 days) and smaller than a certain size (e.g., 1MB), which are often temporary or forgotten artifacts.
*   **Clear Reporting**: Provides a structured output of all found 'dust bunnies'.
*   **Safe & Non-Destructive**: Currently operates in a 'dry run' mode, only reporting findings without making any changes to your filesystem.

## 🚀 How to Use

1.  **Navigate**: Change into the utility's directory:
    ```bash
    cd utils/nightly-digital-dust-bunny-sweeper/src
    ```
2.  **Run**: Execute the `sweeper.py` script with the target directory you want to scan. By default, it scans the current directory (`.`).

    ```bash
    python sweeper.py --path /path/to/your/project
    ```

    Or to scan the current directory:

    ```bash
    python sweeper.py
    ```

    You can also customize the criteria for stale files:

    ```bash
    python sweeper.py --path /path/to/scan --age-days 60 --max-size-mb 5
    ```

## ⚙️ Arguments

*   `--path <directory>`: The root directory to start scanning from. Defaults to the current working directory.
*   `--age-days <int>`: Files older than this many days will be considered stale. Defaults to `30`.
*   `--max-size-mb <int>`: Files smaller than this many megabytes will be considered stale. Defaults to `1`.

## 💡 Example Output

```
Scanning /path/to/your/project for digital dust bunnies...

🧹 Found 2 Empty Directories:
  - /path/to/your/project/temp/empty_folder
  - /path/to/your/project/another_empty_dir

⏳ Found 3 Stale Files (older than 30 days, smaller than 1MB):
  - /path/to/your/project/logs/old_log.txt (Modified: 2023-01-15 10:30:00, Size: 0.50 MB)
  - /path/to/your/project/cache/temp_data.json (Modified: 2023-02-01 14:00:00, Size: 0.10 MB)
  - /path/to/your/project/backup/old_config.bak (Modified: 2023-01-20 08:15:00, Size: 0.02 MB)

Scan complete. Time to get sweeping!
```
