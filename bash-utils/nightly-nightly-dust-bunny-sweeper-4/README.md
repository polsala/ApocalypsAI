# Nightly Digital Dust Bunny Sweeper

## Summary
A whimsical Bash utility that helps you keep your digital space tidy by finding and optionally sweeping away old, unused files and empty directories, affectionately dubbed "digital dust bunnies."

## Description
In the post-apocalyptic digital landscape, data accumulates like dust in forgotten corners. The `Nightly Digital Dust Bunny Sweeper` is your trusty broom, designed to identify and eliminate this digital clutter. It scans a specified directory for files older than a certain age and for any empty directories, reporting them as "dust bunnies." You can run it in a `dry-run` mode to see what would be cleaned, or in `cleanup` mode to actually remove the identified clutter.

Keep your servers lean, your development environments pristine, and your storage optimized, all while enjoying a touch of whimsy!

## Usage

```bash
./src/dust_bunny_sweeper.sh <directory> [age_in_days] [mode]
```

### Arguments:
- `<directory>`: The path to scan for digital dust bunnies (e.g., `/tmp`, `/var/log`, `~/Downloads`).
- `[age_in_days]`: (Optional) Files modified more than this many days ago will be considered dust bunnies. Defaults to `7` days.
- `[mode]`: (Optional)
    - `dry-run` (default): Reports what would be cleaned without actually deleting anything.
    - `cleanup`: Actually removes the identified files and empty directories.

### Examples:

1.  **Perform a dry run on `/var/log` for files older than 30 days:**
    ```bash
    ./src/dust_bunny_sweeper.sh /var/log 30 dry-run
    ```

2.  **Clean up `/tmp` using the default age (7 days):**
    ```bash
    ./src/dust_bunny_sweeper.sh /tmp cleanup
    ```

3.  **Just see what's lurking in your home directory (default dry-run, 7 days):**
    ```bash
    ./src/dust_bunny_sweeper.sh ~/
    ```

## Installation
This is a standalone Bash script. Simply place the `src/dust_bunny_sweeper.sh` file in your desired location, ensure it has execute permissions (`chmod +x src/dust_bunny_sweeper.sh`), and run it.

## Tests
To run the automated tests:

```bash
./tests/test_sweeper.sh
```

The tests use mocks for `find` and `rm` commands to ensure deterministic and offline execution, verifying the script's logic without actual filesystem modifications during testing.
