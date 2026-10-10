# Nightly Digital Dust Bunny Hunt

## Summary

This whimsical utility, the `nightly-digital-dust-bunny-hunt`, helps you identify and manage those long-forgotten files lurking in your directories – we call them "digital dust bunnies." It scans a specified directory for files older than a given age, allowing you to review them and decide their fate, preventing digital clutter from accumulating in your temporal storage.

## Usage

To run the Digital Dust Bunny Hunt, execute the script with optional arguments for the target directory and the age threshold.

```bash
./src/digital_dust_bunny_hunt.sh [-d <directory>] [-a <age_in_days>]
```

### Arguments:

*   `-d <directory>`: The directory to scan for digital dust bunnies. Defaults to the current directory (`.`).
*   `-a <age_in_days>`: The age threshold in days. Files older than this will be considered dust bunnies. Defaults to `90` days.

### Examples:

1.  **Scan the current directory for files older than 90 days (default):**
    ```bash
    ./src/digital_dust_bunny_hunt.sh
    ```

2.  **Scan a specific directory (`/var/log/old_archives`) for files older than 180 days:**
    ```bash
    ./src/digital_dust_bunny_hunt.sh -d /var/log/old_archives -a 180
    ```

3.  **Scan your home directory for files older than 30 days:**
    ```bash
    ./src/digital_dust_bunny_hunt.sh -d ~/ -a 30
    ```

## How it Works

The script uses the `find` command to locate regular files (`-type f`) within the target directory that have not been modified in more than the specified number of days (`-mtime +AGE_THRESHOLD`). It then presents these files as potential "digital dust bunnies" for your review.

## Installation

This is a standalone bash script. Simply ensure it's executable:

```bash
chmod +x src/digital_dust_bunny_hunt.sh
```

## Contributing

Feel free to suggest improvements or new features for better dust bunny detection and management!
