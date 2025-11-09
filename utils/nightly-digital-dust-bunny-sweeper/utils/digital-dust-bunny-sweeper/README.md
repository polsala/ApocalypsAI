# Digital Dust Bunny Sweeper

## 🧹 What is this?

The Digital Dust Bunny Sweeper is a whimsical-yet-useful utility designed to help you keep your digital workspace tidy. It scans a specified directory for 'dust bunnies' – specifically, empty directories and old, forgotten temporary/log files – and provides suggestions for their removal. Think of it as a tiny, automated janitor for your file system!

## ✨ Features

*   **Empty Directory Detection**: Finds and lists directories that contain no files or subdirectories.
*   **Old File Identification**: Locates files with common temporary/log extensions (`.log`, `.tmp`, `.bak`, `.old`, `.swp`, `.DS_Store`) that haven't been modified in a configurable number of days.
*   **Dry Run (Default)**: Safely previews what would be removed without making any changes.
*   **Deletion Mode**: With explicit consent, can remove the identified dust bunnies.

## 🚀 Usage

### Prerequisites

*   Python 3.6+

### Running the Sweeper

1.  Navigate to the `utils/digital-dust-bunny-sweeper/src` directory.
2.  Run the `sweeper.py` script with your desired options.

```bash
# Dry run (default): See what would be swept (scans current directory, files older than 90 days)
python sweeper.py

# Scan a specific path, looking for files older than 30 days
python sweeper.py --path /path/to/your/repo --age 30

# Execute deletion: Actually remove the identified dust bunnies (use with caution!)
python sweeper.py --path /path/to/your/repo --age 60 --delete
```

### Options

*   `--path <directory>`: The root directory to scan. Defaults to the current working directory (`.`).
*   `--age <days>`: The minimum age (in days) for temporary/log files to be considered 'old'. Defaults to 90 days.
*   `--delete`: A flag to enable actual deletion of files and directories. **Use with caution!** By default, the script runs in dry-run mode.

## 🧪 Testing

To run the tests for the Digital Dust Bunny Sweeper:

```bash
cd utils/digital-dust-bunny-sweeper
python -m unittest tests/test_sweeper.py
```
