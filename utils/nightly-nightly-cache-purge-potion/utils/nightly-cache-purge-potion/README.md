# Nightly Cache Purge Potion

## 🧪 Description

The Nightly Cache Purge Potion is a mystical concoction designed to magically whisk away the accumulated digital dust and grime from your system. It targets common user-level cache directories and temporary files for popular development tools (like npm, pip, cargo) and general operating system temporary locations. Regular use can help reclaim valuable disk space and keep your system feeling sprightly.

## ✨ Features

*   **Cross-Platform**: Detects and purges caches on Linux, macOS, and Windows.
*   **Targeted Cleaning**: Focuses on user-specific caches for safety.
*   **Dry Run Mode**: See what would be purged before actually deleting anything.
*   **Whimsical Output**: Provides a delightful report of the cleansing process.

## 🚀 Usage

To run the Purge Potion, navigate to the `utils/nightly-cache-purge-potion` directory and execute the `purge_potion.py` script.

```bash
python3 src/purge_potion.py
```

### Options:

*   `--dry-run`: Perform a dry run without deleting any files. This will show you which directories and files *would* be removed.
    ```bash
    python3 src/purge_potion.py --dry-run
    ```

*   `--verbose`: Show more detailed output during the purge process.
    ```bash
    python3 src/purge_potion.py --verbose
    ```

## ⚠️ Disclaimer

While this utility is designed to target non-essential cache and temporary files, **always exercise caution when deleting files**. It is recommended to use the `--dry-run` option first to review what will be removed. The creators of ApocalypsAI are not responsible for any data loss that may occur from the use of this utility.

## 🛠️ Development

### Running Tests

To run the tests, use `pytest` from the `utils/nightly-cache-purge-potion` directory:

```bash
pytest tests/
```
