# Digital Debris Sweeper

## 🧹 Your Personal Digital Wasteland Janitor 🧹

In the vast, ever-expanding digital cosmos, files accumulate, directories lie fallow, and forgotten metadata clutters the landscape. The `Digital Debris Sweeper` is your trusty companion, designed to identify and report the digital detritus that silently accumulates in your file system. Keep your post-apocalyptic data bunkers pristine!

### What it does:

This utility scans specified directories for common forms of "digital debris," including:
*   **Empty directories**: Folders that serve no purpose but to occupy space.
*   **Orphaned metadata files**: Such as `.DS_Store` (macOS), `Thumbs.db` (Windows), `desktop.ini`.
*   **Temporary or cache files**: Like `__pycache__` directories, `.log` files, `.tmp` files.

It provides a clear report of all identified debris, allowing you to decide what to purge.

### How to use:

1.  **Navigate** to the `utils/digital-debris-sweeper/` directory.
2.  **Run** the `sweeper.py` script with the path(s) you wish to scan:

    ```bash
    python src/sweeper.py /path/to/scan1 /path/to/scan2
    ```

    If no paths are provided, it will scan the current directory.

### Example Output:

```
🧹 Scanning /home/user/my_project for digital debris...

Identified Debris:
- Empty Directory: /home/user/my_project/old_logs
- Orphaned Metadata: /home/user/my_project/.DS_Store
- Cache Directory: /home/user/my_project/__pycache__
- Empty Directory: /home/user/my_project/data/temp_files
- Temporary File: /home/user/my_project/report.tmp

Scan complete. Your digital wasteland is a little cleaner (in knowledge, at least)!
```

### Configuration:

The script currently has hardcoded patterns for common debris. Future versions might allow custom patterns via a configuration file.

### Development:

*   **Language**: Python 3.11
*   **Dependencies**: None (standard library only)
*   **Tests**: `python -m unittest tests/test_sweeper.py`
