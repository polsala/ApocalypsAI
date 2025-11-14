# Digital Dust Bunny Sweeper

## 🧹 What is it?

The Digital Dust Bunny Sweeper is a whimsical-yet-useful command-line utility designed to help you tidy up your digital workspace. It scans specified directories for 'digital dust bunnies' – those pesky, often forgotten files and folders that accumulate over time, cluttering your system and potentially hogging precious disk space.

It identifies:
*   **Empty directories**: Folders that serve no purpose other than to exist.
*   **Stale temporary files**: Files ending in `.tmp` or similar, older than a specified age.
*   **Stale log files**: Files ending in `.log` or similar, older than a specified age.

Once identified, you can choose to simply list these digital nuisances or bravely sweep them away!

## 🚀 Installation

This utility is self-contained. Simply copy the `digital-dust-bunny-sweeper` folder into your `utils/` directory. No external dependencies beyond Python's standard library are required.

## 💡 Usage

Run the `sweeper.py` script with the target path and optional arguments:

```bash
python3 src/sweeper.py <path_to_scan> [--delete] [--age-days <int>] [--patterns <pattern1,pattern2,...>]
```

**Arguments:**
*   `<path_to_scan>`: The root directory from which to start scanning for dust bunnies. (Required)
*   `--delete`: If present, the utility will prompt for confirmation and then delete the identified dust bunnies. **Use with caution!** Without this flag, it will only list them.
*   `--age-days <int>`: Specifies the minimum age in days for a file to be considered 'stale'. Defaults to `30` days. Only applies to files, not empty directories.
*   `--patterns <pattern1,pattern2,...>`: A comma-separated list of file extensions or patterns (e.g., `.tmp,.log,cache_*.txt`) to consider as stale files. Defaults to `.tmp,.log`.

### Examples:

1.  **List all dust bunnies in your downloads folder (default age 30 days, patterns .tmp,.log):**
    ```bash
    python3 src/sweeper.py ~/Downloads
    ```

2.  **List dust bunnies older than 7 days, including `.bak` files, in your project directory:**
    ```bash
    python3 src/sweeper.py ~/my_project --age-days 7 --patterns .tmp,.log,.bak
    ```

3.  **Delete all identified dust bunnies in `/var/log/old_logs` (after confirmation):**
    ```bash
    python3 src/sweeper.py /var/log/old_logs --delete
    ```

## 🧪 Testing

To ensure the sweeper is working as expected, navigate to the `utils/digital-dust-bunny-sweeper` directory and run the tests:

```bash
python3 -m unittest tests/test_sweeper.py
```
