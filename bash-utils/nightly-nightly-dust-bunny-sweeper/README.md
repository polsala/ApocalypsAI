# Nightly Digital Dust Bunny Sweeper

## Summary
This whimsical-yet-useful bash utility helps you keep your digital environment tidy by identifying and optionally sweeping away "digital dust bunnies" – old, unused files and empty directories that accumulate over time.

## Usage
To run the Digital Dust Bunny Sweeper, navigate to the directory you wish to clean or specify a target directory as an argument.

```bash
./src/dust_bunny_sweeper.sh [options] [<directory>]
```

### Options
*   `-d` : **Dry Run**. Only list the digital dust bunnies found; do not perform any deletion.
*   `-a <days>` : Specify the age in days for files to be considered dust bunnies (default: 30 days). Files accessed more than this many days ago will be flagged.
*   `-y` : **Auto-confirm**. Automatically confirm deletion without prompting (use with extreme caution!).
*   `<directory>` : The target directory to scan. If not specified, the current directory (`.`) will be used.

### Examples

1.  **Scan current directory for dust bunnies older than 30 days (dry run):**
    ```bash
    ./src/dust_bunny_sweeper.sh -d
    ```

2.  **Scan a specific directory (`/var/log/old_logs`) for dust bunnies older than 7 days, then prompt for cleanup:**
    ```bash
    ./src/dust_bunny_sweeper.sh -a 7 /var/log/old_logs
    ```

3.  **Aggressively sweep away all dust bunnies older than 60 days in your home directory without confirmation (DANGER!):**
    ```bash
    ./src/dust_bunny_sweeper.sh -y -a 60 ~/my_messy_folder
    ```

## How it Works
The script uses the `find` command to locate files that haven't been accessed for a specified number of days (`-atime`) and to identify empty directories. It then presents these findings to you and, if not in dry-run mode, asks for confirmation before using `rm` and `rmdir` to sweep them away.

Keep your digital space sparkling clean!
