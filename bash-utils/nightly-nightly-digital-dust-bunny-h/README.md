# Nightly Digital Dust Bunny Hunt

## Summary
This whimsical-yet-useful bash utility helps you identify and manage old, forgotten files – your 'digital dust bunnies' – lurking in your directories. It can report them, 're-energize' them (update their modification timestamp), or 'archive them to the void' (move them to a specified archive directory).

## Usage
```bash
./src/dust_bunny_hunt.sh [-d <directory>] [-a <age_days>] [-x <action>] [-o <archive_output_dir>] [-h]
```

### Options:
*   `-d <directory>`: The target directory to scan for dust bunnies. Defaults to the current directory (`.`).
*   `-a <age_days>`: Files older than this many days will be considered digital dust bunnies. Defaults to `30` days.
*   `-x <action>`: The action to perform on identified dust bunnies. Choose one of:
    *   `report` (default): Simply list the files found.
    *   `re-energize`: Use `touch` to update the modification timestamp of the files, making them 'fresh' again.
    *   `archive`: Move the files to a specified archive directory.
*   `-o <archive_output_dir>`: **Required for the `archive` action.** Specifies the directory where files will be moved. If the directory does not exist, the utility will attempt to create it.
*   `-h`: Display the usage help message.

## Examples

1.  **Report all dust bunnies older than 60 days in your home directory:**
    ```bash
    ./src/dust_bunny_hunt.sh -d "$HOME" -a 60 -x report
    ```

2.  **Re-energize forgotten configuration files in `/etc/old_configs` that are older than 90 days:**
    ```bash
    ./src/dust_bunny_hunt.sh -d /etc/old_configs -a 90 -x re-energize
    ```

3.  **Archive old log files from `/var/log/archive_me` to `/tmp/the_void`:**
    ```bash
    ./src/dust_bunny_hunt.sh -d /var/log/archive_me -a 180 -x archive -o /tmp/the_void
    ```

## How to Run Tests

To ensure the Digital Dust Bunny Hunt is working as expected, navigate to the utility's root directory and run the test script:

```bash
./tests/test_dust_bunny_hunt.sh
```

The tests are designed to be deterministic and offline, using mocked system commands (`find`, `touch`, `mv`, `mkdir`) to simulate file operations without affecting your actual filesystem. This allows for reliable and repeatable testing.
