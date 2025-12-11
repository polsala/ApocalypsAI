# Nightly Digital Scavenger

The digital wasteland is vast, and forgotten files accumulate like dust in the ruins of old servers. The Nightly Digital Scavenger is here to help you reclaim valuable disk space by identifying and optionally purging "stale" files – those ancient digital relics that haven't been touched in ages.

Think of it as a post-apocalyptic cleanup crew for your file system, sifting through the digital debris to find what can be safely recycled (deleted).

## Features

*   **Stale File Detection**: Easily find files older than a specified number of days.
*   **Dry Run Mode**: Preview which files would be deleted without actually removing them, ensuring you don't accidentally scavenge something vital.
*   **Configurable Age**: Define what "stale" means to you (default is 30 days).
*   **Interactive or Forceful Deletion**: Confirm each deletion or run in a fully automated, no-questions-asked mode.
*   **Whimsical Output**: Enjoy a touch of post-apocalyptic charm with every scan.

## Usage

```bash
./src/main.sh -d <directory> [-a <age_in_days>] [--dry-run] [--force]
```

### Arguments

*   `-d <directory>`, `--directory <directory>` (Required): The root directory where the scavenger will begin its search for stale files.
*   `-a <age_in_days>`, `--age <age_in_days>` (Optional): Specifies the age in days. Any file with a modification time older than this will be considered stale. Defaults to `30` days.
*   `--dry-run` (Optional): If present, the script will only list the files it *would* delete, but won't actually remove them. This is highly recommended for initial runs!
*   `--force` (Optional): If present, the script will proceed with deletion without asking for user confirmation. Use with extreme caution!
*   `-h`, `--help`: Display the usage information.

## Examples

1.  **Perform a dry run in your downloads folder for files older than 60 days:**
    ```bash
    ./src/main.sh -d ~/Downloads -a 60 --dry-run
    ```

2.  **Delete files older than 90 days in a specific archive directory, with confirmation:**
    ```bash
    ./src/main.sh -d /var/log/old_archives -a 90
    ```

3.  **Forcefully delete all files older than 7 days in a temporary directory (use with caution!):**
    ```bash
    ./src/main.sh -d /tmp/my_temp_data -a 7 --force
    ```

## Testing

To run the tests for this utility:

```bash
cd tests
bash test_main.sh
```

The tests create temporary files and directories to simulate various scenarios (no stale files, dry run, actual deletion, user abort) and verify the script's behavior without affecting your actual file system.
