# Nightly Digital Dust Bunny Sweeper

A whimsical Bash script designed to keep your digital spaces tidy by sweeping away old, forgotten files—affectionately dubbed "digital dust bunnies"—from specified directories. It helps reclaim disk space and maintain a pristine digital environment, reporting on the clutter it clears.

## How it Works

The `dust_bunny_sweeper.sh` script scans one or more specified directories for files older than a given number of days. It can operate in a `--dry-run` mode to show you what it *would* delete, or perform an actual sweep to usher those dusty relics into the void.

It provides a summary of the files processed and the total digital fluff (disk space) reclaimed.

## Usage

```bash
./src/dust_bunny_sweeper.sh <age_in_days> [directory1] [directory2] ... [--dry-run]
```

- `<age_in_days>`: The age threshold in days. Files older than this will be considered "dust bunnies". Must be a positive integer.
- `[directory1] [directory2] ...`: One or more paths to directories you want to sweep. If no directories are specified, the script will sweep the current working directory (`.`).
- `--dry-run`: (Optional) Run the sweep in simulation mode. No files will be deleted, but the script will report what it *would* have swept.

## Examples

1.  **Dry run to see old files in `/var/log` and `/tmp` older than 30 days:**
    ```bash
    ./src/dust_bunny_sweeper.sh 30 /var/log /tmp --dry-run
    ```

2.  **Actually sweep files in your `~/Downloads` folder older than 7 days:**
    ```bash
    ./src/dust_bunny_sweeper.sh 7 ~/Downloads
    ```

3.  **Sweep files in the current directory older than 14 days (without specifying a directory):**
    ```bash
    ./src/dust_bunny_sweeper.sh 14
    ```

## Testing

To ensure the Digital Dust Bunny Sweeper is working as intended without actually deleting your precious files, you can run its self-contained tests.

```bash
# Navigate to the utility's root directory
cd nightly-dust-bunny-sweeper

# Run the test script
./tests/test_dust_bunny_sweeper.sh
```

The test script uses mocks for `find`, `rm`, `du`, and `numfmt` to create a controlled environment. This ensures tests are deterministic, fast, and do not affect your actual file system.
