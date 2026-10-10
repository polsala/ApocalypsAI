# Nightly Digital Dust Sweeper

## Summary
The `nightly-digital-dust-sweeper` is a whimsical-yet-useful Bash utility designed to help you reclaim precious digital real estate. It scans specified directories for "digital dust bunnies" – files and directories that are old, large, and potentially forgotten. Think of it as a post-apocalyptic scavenger hunt for lost bytes!

## Classifier
`bash-utils`

## Usage

### Prerequisites
-   Bash (version 4.0 or higher recommended)
-   `find`, `du`, `stat`, `dd` (standard Unix utilities)

### Running the Sweeper

1.  **Make the script executable:**
    ```bash
    chmod +x src/dust_sweeper.sh
    ```

2.  **Run with default settings:**
    This will scan the current directory for files older than 365 days and larger than 100MB.
    ```bash
    ./src/dust_sweeper.sh
    ```

3.  **Specify a custom path:**
    ```bash
    ./src/dust_sweeper.sh -p /var/log
    # or
    ./src/dust_sweeper.sh --path /home/user/downloads
    ```

4.  **Adjust age and size thresholds:**
    Scan for files/directories older than 90 days and larger than 50MB:
    ```bash
    ./src/dust_sweeper.sh -a 90 -s 50
    # or
    ./src/dust_sweeper.sh --age 90 --size 50
    ```

5.  **Combine options:**
    ```bash
    ./src/dust_sweeper.sh -p /mnt/data -a 180 -s 200
    ```

6.  **Get help:**
    ```bash
    ./src/dust_sweeper.sh -h
    ```

### Output
The script will print a list of identified "digital dust bunnies" (files and directories) along with their size and last modification date. It will then offer a whimsical suggestion to consider them for archiving or deletion.

**Example Output:**
```
=== Initiating Digital Dust Bunny Sweep ===
Scanning '/home/user' for digital dust bunnies (older than 365 days, larger than 100 MB)...

Found some ancient byte-piles (files) that might be digital dust bunnies:
  [FILE] 150M (2022-01-15) - /home/user/old_projects/backup_2022.tar.gz

Discovered some forgotten data-caverns (directories) that could be hoarding dust:
  [DIR]  2.5G (2021-08-20) - /home/user/archive/legacy_data

Consider these for archiving or deletion to free up space. Use with caution!
=== Digital Dust Sweep Complete! Reclaim your precious bytes! ===
```

## How it Works
The script leverages standard Unix commands like `find`, `du`, and `stat` to efficiently locate files and directories matching the specified criteria (age and size). It then formats this information with a touch of post-apocalyptic charm.

**Important Note:** This utility is purely a *reporting* tool. It does **not** delete or modify any files. It merely identifies potential candidates for cleanup, leaving the final decision (and action) to the user. Always review the output carefully before performing any file operations.

## Development & Testing

### Running Tests
To run the automated tests:
1.  Navigate to the `tests` directory.
2.  Make the test script executable:
    ```bash
    chmod +x tests/test_dust_sweeper.sh
    ```
3.  Execute the test script:
    ```bash
    ./tests/test_dust_sweeper.sh
    ```
The tests create a temporary directory with various files and directories of different ages and sizes to simulate a real-world scenario. This ensures the `dust_sweeper.sh` script correctly identifies or ignores "dust bunnies" based on the provided criteria. The temporary environment is cleaned up automatically after tests complete.
