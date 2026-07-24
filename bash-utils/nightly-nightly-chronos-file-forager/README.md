# Chronos's File Forager

## Summary

`nightly-chronos-file-forager` is a whimsical-yet-useful bash utility designed to help you manage digital clutter by finding and optionally removing files older than a specified number of days within a given directory. Think of Chronos, the personification of time, diligently foraging through your filesystem for forgotten relics.

## Usage

```bash
./src/chronos_forager.sh <directory> <age_in_days> [dry-run|delete]
```

### Arguments:

*   `<directory>`: The path to the directory where Chronos will forage for old files. This is a mandatory argument.
*   `<age_in_days>`: The minimum age (in full days) for files to be considered 'old'. For example, `7` would target files modified 7 or more days ago. This is a mandatory argument.
*   `[dry-run|delete]`: An optional action argument.
    *   If `dry-run` is specified (or no action is given), the script will only list the files that *would* be affected without making any changes.
    *   If `delete` is specified, the script will actually remove the identified old files.

## Examples

1.  **List files older than 30 days in `/var/log` (dry-run):**
    ```bash
    ./src/chronos_forager.sh /var/log 30 dry-run
    ```

2.  **Delete files older than 7 days in `/tmp/my_app_cache`:**
    ```bash
    ./src/chronos_forager.sh /tmp/my_app_cache 7 delete
    ```

3.  **List files older than 1 day in the current directory (default dry-run):**
    ```bash
    ./src/chronos_forager.sh . 1
    ```

## Safety Warning

Using the `delete` option will permanently remove files. Always perform a `dry-run` first to ensure you understand which files will be affected. Use with caution, especially in critical system directories.
