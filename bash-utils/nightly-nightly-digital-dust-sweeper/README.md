# Nightly Digital Dust Bunny Sweeper

## Summary
This utility helps keep your digital spaces tidy by identifying and optionally removing old, forgotten files and empty directories, affectionately dubbed "digital dust bunnies". It's perfect for cleaning up temporary files, old logs, or abandoned project remnants that accumulate over time.

## Usage
```bash
bash src/dust_sweeper.sh [OPTIONS] [PATH]
```

### Arguments
*   `PATH`: The directory to scan for digital dust bunnies. Defaults to the current directory (`.`) if not specified.

### Options
*   `-a <days>`, `--age <days>`: Specifies the age threshold in days. Files and empty directories accessed more than `<days>` ago will be considered dust bunnies. Default is `7` days.
*   `-n`, `--dry-run`: Performs a scan and lists the identified dust bunnies, but does not actually delete anything. Useful for previewing the sweep.
*   `-y`, `--yes`: Skips the confirmation prompt and automatically proceeds with the deletion of identified dust bunnies.
*   `-h`, `--help`: Displays the help message and exits.

## Examples

1.  **Scan the current directory for items older than 7 days (default) and ask for confirmation:**
    ```bash
    bash src/dust_sweeper.sh
    ```

2.  **Scan `/var/log` for files older than 30 days, without deleting:**
    ```bash
    bash src/dust_sweeper.sh -a 30 --dry-run /var/log
    ```

3.  **Automatically sweep all dust bunnies older than 14 days in your downloads folder:**
    ```bash
    bash src/dust_sweeper.sh -a 14 -y ~/Downloads
    ```

4.  **Display help message:**
    ```bash
    bash src/dust_sweeper.sh --help
    ```

## How it Works
The script uses `find` to locate files and empty directories based on their last access time (`-atime`). It then presents a list to the user (unless `--dry-run` or `--yes` is used) and, upon confirmation, uses `rm -rf` to remove them. The script is designed to be safe by default, requiring confirmation unless explicitly told otherwise.

## Whimsical Note
In the post-apocalyptic digital landscape, even data can gather dust. These 'digital dust bunnies' are the forgotten remnants of past endeavors, silently consuming precious storage and mental bandwidth. The Nightly Digital Dust Bunny Sweeper is here to bring order to the chaos, one byte at a time, ensuring your systems remain nimble and ready for whatever the digital wasteland throws your way.
