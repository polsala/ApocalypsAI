# Cosmic Dust Bunny Collector

## 🌌 Unearthing Digital Relics from the Cosmic Dust 🌌

In the vast expanse of your digital universe, forgotten files accumulate like cosmic dust bunnies, silently consuming precious space and energy. The `Cosmic Dust Bunny Collector` is your trusty companion in this endless battle against digital entropy. It's a whimsical-yet-powerful utility designed to help you identify and manage stale, unused files across your directories.

Whether you're preparing for a digital apocalypse or simply tidying up your data nebula, this tool will help you reclaim your digital real estate.

## ✨ Features

*   **Recursive Scanning**: Delves deep into subdirectories to find every last dust bunny.
*   **Age-Based Filtering**: Identifies files older than a specified number of days.
*   **Dry Run Mode**: Safely preview which files would be 'collected' without actually deleting them.
*   **Exclusion Patterns**: Ignore specific files or directories that are meant to be ancient.
*   **Whimsical Output**: Reports findings with a touch of cosmic charm.

## 🚀 Installation & Usage

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

1.  **Navigate to the utility directory:**
    ```bash
    cd utils/cosmic-dust-bunny-collector/src
    ```
2.  **Run the collector:**
    ```bash
    python collector.py --path /path/to/your/directory --age 90
    ```

### Arguments:

*   `--path <directory>` (required): The root directory to scan for dust bunnies.
*   `--age <days>` (required): Files older than this many days will be flagged as dust bunnies.
*   `--collect` (optional): Add this flag to actually delete the identified files. **Use with caution!** (Default: dry run).
*   `--exclude <pattern>` (optional, can be repeated): Glob patterns (e.g., `*.log`, `temp_dir/*`) to exclude files or directories from scanning.

## 🧹 Examples

### 1. List dust bunnies older than 180 days in your downloads folder (dry run):

```bash
python collector.py --path ~/Downloads --age 180
```

### 2. Collect (delete) dust bunnies older than 30 days in a temporary directory, excluding `.tmp` files:

```bash
python collector.py --path /var/tmp --age 30 --collect --exclude '*.tmp'
```

## ⚠️ Safety First!

Always run in dry-run mode first (by omitting `--collect`) to review the files that would be affected. The ApocalypsAI is not responsible for accidentally collected cosmic artifacts!
