# Digital Dust Bunny Sweeper

## Whimsical Purpose
Even the most pristine digital realms accumulate forgotten detritus. Like mischievous dust bunnies under a server rack, old logs, temporary files, and forgotten backups can silently hog disk space and clutter your system. The Digital Dust Bunny Sweeper is here to help you reclaim your digital hygiene, one ancient byte at a time!

## Practical Utility
This Python utility scans specified directories for files older than a given age, optionally filtering by file patterns (e.g., `.log`, `.tmp`, `.bak`). It can either list these 'dust bunnies' for review or, with your explicit permission, sweep them away, freeing up valuable disk space and improving system performance.

## Usage

```bash
# List files older than 30 days in /var/log and /tmp, matching .log or .tmp patterns
python src/sweeper.py --paths /var/log /tmp --age 30 --patterns "*.log" "*.tmp" --list

# Delete files older than 90 days in /home/user/downloads (no pattern filter)
python src/sweeper.py --paths /home/user/downloads --age 90 --delete

# Force delete files older than 7 days in /var/cache, matching .cache pattern
python src/sweeper.py --paths /var/cache --age 7 --patterns "*.cache" --delete --force

# Default behavior: list files older than 14 days in current directory (no patterns)
python src/sweeper.py --paths . --age 14
```

### Arguments:
*   `--paths <path1> [<path2> ...]`: **Required**. One or more directories to scan.
*   `--age <days>`: **Required**. Files older than this many days will be considered 'dust bunnies'.
*   `--patterns <pattern1> [<pattern2> ...]`: **Optional**. Only consider files matching these glob patterns (e.g., `*.log`, `*.tmp`). If not provided, all files older than `--age` are considered.
*   `--list`: **Optional**. List the identified dust bunnies without deleting them. This is the default behavior if `--delete` is not specified.
*   `--delete`: **Optional**. Delete the identified dust bunnies. **Use with caution!**
*   `--force`: **Optional**. Skip the confirmation prompt when using `--delete`.

## Installation
This utility is self-contained and requires Python 3.6+.

```bash
# No special installation needed. Just run it directly:
python src/sweeper.py --help
```

## Development & Testing

To run tests:
```bash
python -m unittest tests/test_sweeper.py
```
