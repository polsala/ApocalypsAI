# Cosmic Cache Cleaner

## Purge Digital Cosmic Dust from Your System!

This utility, the **Cosmic Cache Cleaner**, helps you navigate the digital cosmos of your file system to identify and purge 'cosmic dust' – old, large, or redundant files lurking in common cache directories. Reclaim precious disk space and ensure your system operates with celestial efficiency!

### Features

*   **OS-Aware Cache Path Detection**: Automatically identifies common cache locations across Windows, macOS, and Linux.
*   **Customizable Filters**: Define what constitutes 'cosmic dust' by setting minimum age (days) and minimum size (MB) thresholds.
*   **Dry-Run Reporting**: Get a detailed 'Cosmic Debris Report' without making any changes, showing what would be cleaned.
*   **Interactive Deletion**: Optionally proceed with deletion after reviewing the report, with a confirmation prompt.
*   **Whimsical Output**: Enjoy a touch of cosmic flair in the console output.

### Usage

Navigate to the `utils/cosmic-cache-cleaner` directory and run the `cleaner.py` script.

```bash
cd utils/cosmic-cache-cleaner

# Perform a dry run to see what would be cleaned (recommended first step)
python src/cleaner.py --dry-run

# Scan for files older than 30 days and larger than 100 MB (dry run)
python src/cleaner.py --dry-run --age 30 --size 100

# Scan for files older than 7 days and delete them (prompts for confirmation)
python src/cleaner.py --delete --age 7

# Scan a specific custom path (e.g., your project's build cache) for files larger than 500MB
python src/cleaner.py --dry-run --paths "/path/to/your/project/cache" --size 500

# Delete all identified cosmic dust without confirmation (use with extreme caution!)
python src/cleaner.py --delete --force
```

### Arguments

*   `--dry-run`: (Default) Scan and report, but do not delete any files.
*   `--delete`: Enable deletion of identified files. Will prompt for confirmation unless `--force` is also used.
*   `--force`: Use with `--delete` to skip the confirmation prompt. **Use with extreme caution!**
*   `--age <days>`: Only consider files older than this many days (default: 30).
*   `--size <MB>`: Only consider files larger than this many megabytes (default: 100).
*   `--paths <path1> [<path2> ...]`: Specify custom directories to scan instead of default system caches. Separate multiple paths with spaces.

### Example Cosmic Debris Report

```
🌌 Initiating Cosmic Cache Scan... 🌌

Scanning for rogue celestial debris in known cache orbits...

🚀 Analyzing: /Users/apocalypsai/Library/Caches
🚀 Analyzing: /var/cache

✨ Cosmic Debris Report ✨

Identified 3 pieces of space junk:

- /Users/apocalypsai/Library/Caches/old_log.txt (150.0 MB, last modified: 2023-01-15)
- /var/cache/temp_data/large_archive.zip (520.5 MB, last modified: 2022-11-01)
- /var/cache/another_old_file.tmp (120.0 MB, last modified: 2023-02-20)

Total estimated mass of cosmic dust to be purged: 790.5 MB

To proceed with orbital decay protocol (deletion), run with --delete.
```
