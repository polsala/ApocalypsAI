# Digital Dust Bunny Hoover

## 🧹 Whimsical Utility for Digital Hygiene 🧹

In the ever-expanding digital cosmos, forgotten files accumulate like cosmic dust, slowing down our systems and obscuring our path to true efficiency. The `digital-dust-bunny-hoover` is here to help! This utility whimsically yet effectively identifies and purges old, neglected files from your specified directories, ensuring your digital realm remains pristine and ready for the next apocalypse (or just the next commit).

It's not just deletion; it's **digital purification**!

### ✨ Features

*   **Recursive Scanning**: Delves deep into subdirectories to find every last dust bunny.
*   **Age-Based Filtering**: Targets files older than a specified number of days.
*   **Dry Run Mode**: See what would be 'hoovered' before committing to deletion.
*   **Deletion Confirmation**: Requires explicit `--delete` flag to perform actual removal.
*   **Whimsical Output**: Adds a touch of fun to your system maintenance.

### 🚀 Usage

```bash
python src/hoover.py <directory_path> --age <days> [--delete] [--verbose]
```

**Arguments:**

*   `<directory_path>`: The root directory to start scanning from.
*   `--age <days>`: Files older than this many days will be considered dust bunnies. (e.g., `--age 30` for files older than 30 days).
*   `--delete`: **WARNING!** Use this flag to actually delete the identified files. Without it, the utility will only report.
*   `--verbose`: Print detailed information about each file found.

### 💡 Examples

**1. Dry Run: See what files older than 90 days are in your `temp` directory:**

```bash
python src/hoover.py /var/tmp --age 90
```

**2. Purify: Delete all files older than 7 days in your `downloads` folder:**

```bash
python src/hoover.py ~/Downloads --age 7 --delete
```

**3. Verbose Dry Run: Get detailed info on old log files:**

```bash
python src/hoover.py /var/log --age 365 --verbose
```

### 🛠️ Development

The `digital-dust-bunny-hoover` is written in Python 3.11 and is self-contained.

To run tests:

```bash
python -m unittest tests/test_hoover.py
```

May your digital spaces be ever clean!
