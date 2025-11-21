# Digital Debris Destroyer

## 🧹 Purpose

The Digital Debris Destroyer (DDD) is your trusty companion for tidying up the digital wasteland of your project. It scours specified directories for files and folders matching given patterns that are older than a certain age, offering to either report them or obliterate them from existence. Keep your repository lean, clean, and free from the digital dust bunnies of forgotten build artifacts, old logs, and temporary files.

## ✨ Features

*   **Pattern-based Matching**: Use glob patterns (e.g., `*.log`, `__pycache__`) to target specific types of debris.
*   **Age-based Filtering**: Only target files and directories older than a configurable number of days.
*   **Dry Run Mode**: Safely preview what would be deleted before committing to destruction.
*   **Recursive Scanning**: Traverses directories to find hidden clutter.

## 🚀 Usage

Run the utility from your terminal. It requires Python 3.8+.

```bash
python src/cleaner.py --path <directory_to_scan> \
                      --patterns <pattern1> [<pattern2> ...] \
                      --age-days <number_of_days> \
                      [--delete]
```

### Arguments:

*   `--path <directory_to_scan>`: The root directory from which to start scanning for debris. (e.g., `.`, `./build`, `/tmp`)
*   `--patterns <pattern1> [<pattern2> ...]`: One or more glob patterns to match files or directories. (e.g., `*.log`, `__pycache__`, `*.tmp`, `dist/`)
*   `--age-days <number_of_days>`: The minimum age in days for a file or directory to be considered 'old' and eligible for deletion. (e.g., `7`, `30`, `90`)
*   `--delete`: **(Optional)** If provided, the utility will actually delete the matched files/directories. **Use with caution!** By default, it runs in dry-run mode, only reporting what *would* be deleted.

### Examples:

1.  **Dry run: Find all `.log` files and `__pycache__` directories older than 30 days in the current directory:**
    ```bash
    python src/cleaner.py --path . --patterns "*.log" "__pycache__" --age-days 30
    ```

2.  **Delete: Remove all `.tmp` files older than 7 days in the `/tmp` directory:**
    ```bash
    python src/cleaner.py --path /tmp --patterns "*.tmp" --age-days 7 --delete
    ```

3.  **Dry run: Find `dist/` directories and `build/` directories older than 90 days in a specific project folder:**
    ```bash
    python src/cleaner.py --path ~/my_project --patterns "dist/" "build/" --age-days 90
    ```

## ⚠️ Warning

Always perform a dry run first to ensure you understand what will be deleted. The `--delete` flag is irreversible. The ApocalypsAI team is not responsible for any data loss due to misuse of this utility. Use wisely, and may your digital space be ever clean!
