# Nightly Dust Bunny Sweeper

A whimsical Bash script to sweep away digital dust bunnies: old, unused, or broken files and directories. Keep your digital lair tidy and free from the accumulated cruft of the apocalypse!

## Features

*   **Find Old Files**: Identifies files not accessed within a specified number of days.
*   **Find Empty Directories**: Locates directories that contain no files or subdirectories.
*   **Find Broken Symlinks**: Detects symbolic links that point to non-existent targets.
*   **Dry Run Mode**: Preview what would be cleaned without making any changes.
*   **Interactive Deletion**: Prompt before deleting each item (optional).
*   **Automated Cleanup**: Delete all found items without prompting (use with caution!).

## Usage

```bash
./src/dust_bunny_sweeper.sh [OPTIONS] [TARGET_DIRECTORY]
```

### Options

*   `-a <days>`, `--age <days>`: Find files not accessed in `<days>` days. Default: 30.
*   `-e`, `--empty-dirs`: Include empty directories in the scan.
*   `-b`, `--broken-links`: Include broken symbolic links in the scan.
*   `-d`, `--delete`: Delete found items. **Use with extreme caution!**
*   `-i`, `--interactive`: Prompt before deleting each item (only with `-d`).
*   `-h`, `--help`: Display this help message.

### Examples

1.  **Dry run, find files older than 60 days in the current directory:**
    ```bash
    ./src/dust_bunny_sweeper.sh -a 60
    ```

2.  **Dry run, find empty directories and broken links in `/var/log`:**
    ```bash
    ./src/dust_bunny_sweeper.sh -e -b /var/log
    ```

3.  **Delete files older than 7 days, empty directories, and broken links in `~/Downloads` (with prompt):**
    ```bash
    ./src/dust_bunny_sweeper.sh -a 7 -e -b -d -i ~/Downloads
    ```

4.  **Automatically delete all findings in `/tmp` (DANGEROUS!):**
    ```bash
    ./src/dust_bunny_sweeper.sh -a 1 -e -b -d /tmp
    ```

## Installation

Simply clone the repository and make the script executable:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/bash-utils/nightly-dust-bunny-sweeper
chmod +x src/dust_bunny_sweeper.sh
```

## Contributing

Feel free to suggest improvements or new "dust bunny" types!
