# Nightly Temporal Dust Bunny Sweeper

A whimsical bash script to sweep away old temporary files and directories, treating them as "temporal dust bunnies" that have accumulated over time. Keep your digital burrows tidy!

## ✨ Features

*   **Whimsical Output**: Enjoy delightful messages as your old files are swept into the temporal void.
*   **Age-Based Cleaning**: Specify how many days old a file or directory must be to be considered a "dust bunny."
*   **Targeted Sweeping**: Cleans only the immediate children (files and directories) within a specified directory, preventing accidental deep deletions.
*   **Safe & Simple**: Designed for straightforward cleanup of temporary or cache directories.

## 🚀 Usage

```bash
./src/dust_bunny_sweeper.sh <target_directory> <age_in_days>
```

### Arguments:

*   `<target_directory>`: The path to the directory you want to sweep for temporal dust bunnies.
*   `<age_in_days>`: The minimum age (in days) for a file or directory to be considered a "dust bunny" and swept away. For example, `7` would sweep items older than 7 days.

### Examples:

Sweep files and directories in `/tmp` that are older than 30 days:
```bash
./src/dust_bunny_sweeper.sh /tmp 30
```

Clean up old cache files in your home directory's `.cache` folder that are older than 7 days:
```bash
./src/dust_bunny_sweeper.sh ~/.cache 7
```

## 🛠️ How it Works

The script uses the `find` command to locate files and directories within the specified `<target_directory>` that have a modification time (`-mtime`) older than the given `<age_in_days>`. It specifically targets only the immediate children of the `target_directory` (using `-maxdepth 1 -mindepth 1`). Once identified, these "temporal dust bunnies" are then removed using `rm -rf`.

## 🧪 Testing

To run the tests, navigate to the utility's root directory and execute the test script:

```bash
./tests/test_dust_bunny_sweeper.sh
```

The tests create a temporary directory, populate it with files and directories of various ages, and then run the `dust_bunny_sweeper.sh` script to verify that only the appropriately aged items are removed. The tests are self-contained and clean up after themselves.
