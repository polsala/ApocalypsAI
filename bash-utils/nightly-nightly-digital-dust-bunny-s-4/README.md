# Nightly Digital Dust Bunny Sweeper

## Summary
The `nightly-digital-dust-bunny-sweeper` is a whimsical yet practical Bash utility designed to help you declutter your digital workspace. It scans specified directories for old, forgotten temporary files and empty directories, affectionately dubbing them "digital dust bunnies." After identifying these digital detritus, it offers to sweep them away, freeing up valuable disk space and bringing a touch of order to your system.

## Usage
```bash
./src/dust_bunny_sweeper.sh <directory_to_scan> <age_in_days> [--force]
```

- `<directory_to_scan>`: The path to the directory you want to scan for dust bunnies (e.g., `/tmp`, `~/.cache`, `/var/log`).
- `<age_in_days>`: Files and empty directories older than this many days will be considered dust bunnies.
- `--force`: (Optional) Skip the confirmation prompt and proceed directly with deletion. Use with caution!

## Examples

1. **Scan `/tmp` for items older than 7 days (interactive):**
   ```bash
   ./src/dust_bunny_sweeper.sh /tmp 7
   ```

2. **Scan `~/.cache` for items older than 30 days and automatically delete:**
   ```bash
   ./src/dust_bunny_sweeper.sh ~/.cache 30 --force
   ```

3. **Just see what's lurking in `/var/log` older than 90 days, without deleting:**
   ```bash
   # The script will list them and then wait for your 'n' input to not delete.
   ./src/dust_bunny_sweeper.sh /var/log 90
   ```

## How it Works
The script uses `find` to locate files and empty directories based on their last modification time. It then presents a list of these "dust bunnies" and, unless `--force` is used, prompts for confirmation before using `rm` to remove them.

## Installation
This is a standalone Bash script. Simply ensure it's executable:
```bash
chmod +x src/dust_bunny_sweeper.sh
```

## Tests
To run the tests, navigate to the utility's root directory and execute:
```bash
./tests/test_dust_bunny_sweeper.sh
```
The tests use temporary directories and mock commands to ensure no actual files are deleted during testing.
