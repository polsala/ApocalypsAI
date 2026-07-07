# Nightly Digital Dust Bunny Sweeper

✨ Welcome to the Nightly Digital Dust Bunny Sweeper! ✨

This whimsical Bash script helps you maintain a tidy digital realm by identifying and optionally sweeping away old, unused files and forgotten empty directories – what we affectionately call 'digital dust bunnies'. Over time, temporary files, old downloads, and abandoned project remnants can accumulate, cluttering your system and consuming precious storage. This utility helps you banish those forgotten bytes with a touch of charm.

## Features

*   **Targeted Cleaning**: Specify any directory to scan.
*   **Age-Based Filtering**: Define how old a file or empty directory must be to be considered a 'dust bunny'.
*   **Dry Run Mode**: Preview what would be deleted without making any changes, ensuring peace of mind.
*   **Interactive Deletion**: Confirm before any files are permanently removed.
*   **Whimsical Output**: Enjoy delightful messages as you cleanse your digital space.

## Usage

To run the Digital Dust Bunny Sweeper, execute the script with the target directory and the age in days:

```bash
./src/dust_bunny_sweeper.sh <directory> <age_in_days> [--dry-run]
```

### Arguments:

*   `<directory>`: The path to scan for old files and empty directories (e.g., `~/Downloads`, `/var/log`, `~/tmp`).
*   `<age_in_days>`: Files and empty directories older than this many days will be considered 'dust bunnies'.
*   `--dry-run`: (Optional) If provided, the script will only list the items that *would* be deleted, without actually removing anything. This is highly recommended for a first run!

### Examples:

1.  **Perform a dry run to see old files in your Downloads folder (older than 60 days):**
    ```bash
    ./src/dust_bunny_sweeper.sh ~/Downloads 60 --dry-run
    ```

2.  **Interactively delete files older than 30 days in your temporary directory:**
    ```bash
    ./src/dust_bunny_sweeper.sh /tmp 30
    ```
    (The script will prompt you for confirmation before deleting.)

3.  **Clean up old log files in a specific directory (older than 90 days):**
    ```bash
    ./src/dust_bunny_sweeper.sh /var/log/old_app_logs 90
    ```

## Installation

This is a standalone Bash script. Simply ensure it's executable:

```bash
chmod +x src/dust_bunny_sweeper.sh
```

Then you can run it as shown in the Usage section.

## Contributing

Feel free to suggest new whimsical messages, additional cleanup strategies (e.g., specific file types, broken symlinks), or improvements to the script! Let's keep our digital realms sparkling clean and full of joy.
