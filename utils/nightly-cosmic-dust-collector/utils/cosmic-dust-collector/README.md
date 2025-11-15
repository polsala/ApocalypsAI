# Cosmic Dust Collector

## Purpose
This utility, the 'Cosmic Dust Collector', helps you maintain a pristine repository by identifying and optionally cleaning up 'cosmic dust' – files that are untracked by Git, potentially old, or excessively large. It's designed to sweep away forgotten build artifacts, temporary files, or other digital debris that can accumulate over time.

## Features
- **Untracked File Detection**: Leverages Git to find files not under version control.
- **Size Filtering**: Focus on large files that consume significant space.
- **Age Filtering**: Target files that haven't been modified recently.
- **Dry Run Mode**: Preview deletions before committing to them.

## Installation
This utility is self-contained and written in Python 3.11+. No special installation steps are required beyond having Python and Git installed on your system.

## Usage
Run the `dust_collector.py` script from your repository's root or any subdirectory. It will scan the current directory and its subdirectories by default.

```bash
python src/dust_collector.py [OPTIONS]
```

### Options
- `--path <directory>`: The root directory to start scanning from. Defaults to the current working directory (`.`).
- `--dry-run`: (Optional) Perform a dry run. Files will be identified and reported, but not deleted. **Highly recommended to use this first!**
- `--min-size <size>`: (Optional) Only consider files larger than this size. Examples: `100K`, `5M`, `1G`. (Default: `0` - no minimum size).
- `--older-than <duration>`: (Optional) Only consider files older than this duration. Examples: `7d` (7 days), `30d` (30 days), `1y` (1 year). (Default: `0d` - no age limit).
- `--delete`: (Optional) **WARNING**: Actually delete the identified files. Use with extreme caution and always after a `--dry-run`.

### Examples

1.  **Find all untracked files (dry run):**
    ```bash
    python src/dust_collector.py --dry-run
    ```

2.  **Find untracked files larger than 5MB and older than 30 days (dry run):**
    ```bash
    python src/dust_collector.py --min-size 5M --older-than 30d --dry-run
    ```

3.  **Delete untracked files larger than 100KB and older than 7 days:**
    ```bash
    python src/dust_collector.py --min-size 100K --older-than 7d --delete
    ```

## How it Works
The script uses `git ls-files --others --exclude-standard` to get a list of untracked files. It then filters this list based on the provided size and age criteria before reporting or deleting them.

## Contributing
Feel free to contribute to the Cosmic Dust Collector by opening issues or pull requests in the main ApocalypsAI repository.
