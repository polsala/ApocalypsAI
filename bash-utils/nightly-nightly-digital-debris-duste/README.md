# Nightly Digital Debris Duster

## Summary
In the post-apocalyptic digital landscape, forgotten files accumulate like dust bunnies in a derelict server farm. The `nightly-digital-debris-duster` is a whimsical Bash script designed to help you identify and optionally scavenge (delete) these old, unused files, tidying up your digital wasteland.

## Philosophy
Every byte counts in the new world. This utility helps you reclaim precious storage by clearing out the digital detritus that no longer serves a purpose, making your systems leaner and more efficient for survival.

## Usage

To run the Digital Debris Duster, execute the script with optional arguments for the target directory, the age threshold, and the minimum size for debris.

```bash
bash src/debris_duster.sh [DIRECTORY] [DAYS_OLD] [MIN_SIZE_KB]
```

- `DIRECTORY`: (Optional) The path to the directory to scan. Defaults to the current directory (`.`).
- `DAYS_OLD`: (Optional) Files older than this many days will be considered debris. Defaults to `30` days.
- `MIN_SIZE_KB`: (Optional) Files smaller than this many kilobytes will be ignored. Defaults to `1` KB.

### Examples

1. **Scan the current directory for debris older than 30 days and larger than 1KB (default behavior):**
   ```bash
   bash src/debris_duster.sh
   ```

2. **Scan a specific directory (`/var/log/old_archives`) for files older than 90 days and larger than 100KB:**
   ```bash
   bash src/debris_duster.sh /var/log/old_archives 90 100
   ```

3. **Scan your home directory for any file older than 7 days, regardless of size (by setting MIN_SIZE_KB to 0):**
   ```bash
   bash src/debris_duster.sh ~/ 7 0
   ```

Upon identifying potential debris, the script will list the files and prompt you for confirmation before proceeding with deletion. Always review the list carefully before confirming!
