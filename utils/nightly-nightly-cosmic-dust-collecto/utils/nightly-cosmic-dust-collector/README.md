# Nightly Cosmic Dust Collector

## 🌌 Purpose

The Nightly Cosmic Dust Collector is a whimsical yet practical utility designed to help keep your project directories tidy and free from digital clutter. It scans specified paths for "cosmic dust" – files that are empty, excessively small, or haven't been modified in a long time. By identifying and optionally managing these forgotten files, it helps maintain a clean, focused, and efficient repository.

## ✨ How it Works

This utility performs a recursive scan of the target directory. For each file found, it checks:
1.  **Emptiness**: Is the file 0 bytes in size?
2.  **Age**: Has the file been untouched (not modified) for a configurable number of days?

Based on these criteria, it can either list the identified "dust" or, with explicit confirmation, proceed to delete them.

## 🚀 Usage

```bash
python src/dust_collector.py --path <directory_to_scan> [--age <days>] [--action <list|delete>] [--dry-run]
```

### Arguments:

*   `--path <directory>`: The root directory to start scanning for cosmic dust. **Required.**
*   `--age <days>`: Files not modified for this many days or more will be considered old dust. Default is `30` days.
*   `--action <list|delete>`:
    *   `list` (default): Only list the files identified as cosmic dust.
    *   `delete`: Permanently delete the identified cosmic dust files. **Use with caution!**
*   `--dry-run`: When used with `--action delete`, it will show which files *would* be deleted without actually deleting them. Recommended for review.

### Examples:

1.  **List all dust files older than 60 days in the current directory:**
    ```bash
    python src/dust_collector.py --path . --age 60 --action list
    ```
2.  **Perform a dry run of deleting dust files older than 90 days in a specific folder:**
    ```bash
    python src/dust_collector.py --path /var/log/old_logs --age 90 --action delete --dry-run
    ```
3.  **Actually delete empty files and files older than 30 days in the 'temp' directory:**
    ```bash
    python src/dust_collector.py --path ./temp --action delete
    ```

## ⚠️ Warning

The `--action delete` option will permanently remove files. Always use `--dry-run` first to review the files that would be affected. The ApocalypsAI team is not responsible for any data loss due to misuse.
