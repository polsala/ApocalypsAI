# Nightly Digital Archaeologist

## Summary
Scans specified directories for ancient, forgotten files and digital relics, helping to unearth or reclaim valuable storage space.

## Description
In the vast, ever-expanding digital wasteland, files accumulate like dust bunnies in forgotten corners. The Nightly Digital Archaeologist is here to help you uncover these long-lost artifacts. This whimsical utility scans your chosen directories for files that meet specific criteria (e.g., older than a certain age, larger than a certain size) and presents them as "relics from a bygone digital era." Use it to identify potential candidates for archival, deletion, or simply to marvel at your digital history.

## Usage

### Prerequisites
- Bash shell
- `find`, `du`, `stat` (GNU coreutils versions are assumed for full functionality, especially `stat -c %y` and `date -d` for tests)
- `truncate` (for creating test files, not strictly needed for runtime)

### Running the Archaeologist

Navigate to the utility's directory and run the script:

```bash
./src/archaeologist.sh [OPTIONS]
```

### Options

- `-d <directory>`: The target directory to scan. Defaults to the current directory (`.`).
- `-a <min_age_days>`: The minimum age in days for a file to be considered an "artifact." Files modified more than this many days ago will be reported. Defaults to `365` (1 year).
- `-s <min_size_mb>`: The minimum size in megabytes (MB) for a file to be considered an "artifact." Files larger than this size will be reported. Defaults to `100` MB.
- `-h`: Display the help message and exit.

### Examples

1. **Scan the current directory for files older than 2 years and larger than 50MB:**
   ```bash
   ./src/archaeologist.sh -a 730 -s 50
   ```

2. **Scan your home directory for any file older than 30 days, regardless of size (set size to 0):**
   ```bash
   ./src/archaeologist.sh -d ~/ -a 30 -s 0
   ```

3. **Find all files larger than 1GB in a specific project directory, regardless of age (set age to 0):**
   ```bash
   ./src/archaeologist.sh -d /path/to/my/project -a 0 -s 1024
   ```

## Example Output

```
--- Nightly Digital Archaeologist Report ---
Unearthing digital artifacts from: './my_archive'
Searching for relics older than: 365 days
Searching for relics larger than: 100 MB
------------------------------------------

  [ARTIFACT FOUND] Path: ./my_archive/old_project_backup_2020.zip
    Size: 1.2G
    Last Modified: 2020-03-15
    (A relic from a bygone digital era...)

  [ARTIFACT FOUND] Path: ./my_archive/forgotten_vm_image.vmdk
    Size: 5.8G
    Last Modified: 2021-01-20
    (A relic from a bygone digital era...)

--- End of Archaeological Survey ---
Consider cataloging these finds or repatriating them to the void.
```
