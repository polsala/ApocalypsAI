# Digital Dust Bunny Sweeper 🧹🐰

## Overview

The Digital Dust Bunny Sweeper is a whimsical-yet-useful utility designed to help you declutter your digital workspace. It scans a specified directory for "digital dust bunnies" – these include empty folders, old temporary files, and common log files – and presents a list of suggested items for cleanup. Keep your repository (or any project folder!) sparkling clean and free from digital debris!

## Features

*   **Empty Folder Detection**: Identifies and lists directories that contain no files or subdirectories.
*   **Temporary & Log File Scanning**: Locates files matching common temporary or log file patterns (e.g., `.log`, `.tmp`, `~`).
*   **Age-Based Filtering**: Optionally filters files older than a specified number of days.
*   **Non-Destructive**: By default, it only *suggests* items for deletion, giving you full control over what gets removed.

## Usage

### Prerequisites

*   Python 3.6+ (standard library only)

### Running the Sweeper

1.  Navigate to the `src` directory:
    ```bash
    cd utils/digital-dust-bunny-sweeper/src
    ```
2.  Run the script with the target directory:
    ```bash
    python dust_bunny_sweeper.py /path/to/your/project
    ```

### Command-line Arguments

*   `<target_directory>` (required): The path to the directory you want to scan.
*   `--age <days>` (optional): Only suggest files older than this many days. Default is 30 days.
*   `--patterns <pattern1,pattern2,...>` (optional): Comma-separated list of file extensions/patterns to look for (e.g., `.log,.tmp,~`). Default is `.log,.tmp,~`.

### Examples

Scan your current directory for dust bunnies:
```bash
python dust_bunny_sweeper.py .
```

Scan a specific project directory, only showing files older than 60 days:
```bash
python dust_bunny_sweeper.py /home/user/my_awesome_project --age 60
```

Scan with custom file patterns (e.g., only `.bak` files):
```bash
python dust_bunny_sweeper.py /var/www/html --patterns .bak
```

## Output

The utility will print a categorized list of found dust bunnies:

```
🧹🐰 Digital Dust Bunny Sweeper Report 🐰🧹

Scanning: /path/to/your/project
Age Threshold: 30 days
File Patterns: ['.log', '.tmp', '~']

--- Empty Directories ---
- /path/to/your/project/empty_folder_1
- /path/to/your/project/another_empty_dir

--- Old/Temporary Files ---
- /path/to/your/project/logs/app.log (Last modified: 2023-01-15)
- /path/to/your/project/temp/cache.tmp (Last modified: 2023-02-01)
- /path/to/your/project/config.bak~ (Last modified: 2023-03-10)

--- Scan Complete! ---
Found 4 digital dust bunnies. Consider giving them a good sweep!
```

## Development

### Running Tests

From the `utils/digital-dust-bunny-sweeper` directory:

```bash
python -m unittest tests/test_dust_bunny_sweeper.py
```
