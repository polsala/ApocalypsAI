# Digital Dust Bunny Sweeper

## 🧹 What is this?

In the post-apocalyptic digital wasteland, every byte counts! The `digital-dust-bunny-sweeper` is your trusty companion for tidying up your file system. It scours specified directories for 'digital dust bunnies' – those forgotten, empty folders and ancient, temporary files that accumulate over time, silently consuming precious storage.

Think of it as a pre-emptive strike against digital entropy, ensuring your data bunkers are lean and efficient when the real collapse comes.

## ✨ Features

*   **Empty Directory Detection**: Finds and lists directories that contain no files or subdirectories.
*   **Aged File Identification**: Locates files matching specified patterns (e.g., `.log`, `.tmp`) that haven't been modified in a configurable number of days.
*   **Dry Run Mode**: Safely preview what would be cleaned without making any changes.
*   **Whimsical Reporting**: Get updates on your cleaning progress with a touch of apocalyptic charm.

## 🚀 How to Use

1.  **Navigate**: Change into the `digital-dust-bunny-sweeper` directory.
2.  **Run**: Execute the `dust_bunny_sweeper.py` script with your desired options.

```bash
python src/dust_bunny_sweeper.py --help
```

### Basic Usage (Dry Run)

To see what dust bunnies are lurking in your current directory and its subfolders, without deleting anything:

```bash
python src/dust_bunny_sweeper.py --path . --dry-run
```

### Finding Old Log Files

To find all `.log` files older than 30 days in your `/var/log` directory (dry run):

```bash
python src/dust_bunny_sweeper.py --path /var/log --age-days 30 --patterns "*.log" --dry-run
```

### Cleaning Up Empty Directories and Old Temp Files

To actually remove empty directories and `.tmp` files older than 7 days in your `~/downloads` folder:

```bash
python src/dust_bunny_sweeper.py --path ~/downloads --age-days 7 --patterns "*.tmp" --delete
```

**⚠️ WARNING**: Always use `--dry-run` first to review what will be deleted. Deletion is permanent!

## 🛠️ Development

This utility is written in Python 3.11 and uses standard library modules only. Tests are located in the `tests/` directory.
