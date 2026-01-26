# Nightly Temporal Dust Bunny Sweeper

The digital realm, much like the physical, accumulates its fair share of dust. Files long forgotten, unaccessed, and gathering virtual cobwebs can clutter your precious storage and weigh down your system's temporal flow. The `nightly-temporal-dust-bunny-sweeper` is here to help you identify and manage these digital "dust bunnies."

This utility scans specified directories for files that haven't been accessed in a given number of days, offering a clear report and an optional "sweep" function to move them to a designated archive.

## Usage

```bash
./src/dust_bunny_sweeper.sh <directory> <age_in_days> [--sweep]
```

- `<directory>`: The path to the directory you want to scan.
- `<age_in_days>`: Files not accessed for this many days (or more) will be considered "dust bunnies."
- `--sweep` (optional): If provided, identified dust bunnies will be moved to a `.dust_bunnies_archive` subdirectory within the scanned directory. If this directory doesn't exist, it will be created.

## Examples

1.  **List all files in `/var/log` not accessed in the last 90 days:**
    ```bash
    ./src/dust_bunny_sweeper.sh /var/log 90
    ```

2.  **Move files in `~/old_projects` not accessed in the last 365 days to an archive:**
    ```bash
    ./src/dust_bunny_sweeper.sh ~/old_projects 365 --sweep
    ```

3.  **Scan the current directory for files older than 30 days, without sweeping:**
    ```bash
    ./src/dust_bunny_sweeper.sh . 30
    ```

## How it Works

The script uses the `find` command to locate files based on their last access time (`-atime`).
- When `--sweep` is *not* used, it simply prints the paths of the identified files.
- When `--sweep` *is* used, it creates a `.dust_bunnies_archive` directory (if it doesn't exist) and moves the identified files into it. It will print the files being moved.

**Important Note:** Use the `--sweep` option with caution. Always review the output of a dry run (without `--sweep`) before performing any file movements.
