# Nightly Digital Dust Bunny Sweeper

## \uD83D\uDD70\uFE0F What is this?

The `nightly-digital-dust-bunny-sweeper` is a whimsical-yet-useful utility designed to help you combat digital clutter. It scans specified directories for old, forgotten files \u2013 your "digital dust bunnies" \u2013 and provides options to either report them, archive them to a designated "Digital Void," or permanently vaporize them. Keep your digital spaces sparkling clean and free up precious storage!

## \u2728 Features

*   **Age-based Scanning**: Identify files older than a specified number of days.
*   **Flexible Actions**: Choose to `report` (list files), `archive` (move to a specified directory), or `delete` (permanently remove) the identified files.
*   **Exclusion Filters**: Prevent important files (e.g., logs, backups) from being swept by excluding specific file extensions.
*   **Confirmation Prompt**: Safety first! Actions like archiving or deleting require confirmation unless forced.
*   **Whimsical Output**: Enjoy themed messages as you clean up your digital realm.

## \uD83D\uDE80 Usage

```bash
./src/dust_bunny_sweeper.sh <directory> [options]
```

### Arguments

*   `<directory>`: The path to scan for old files. This is a mandatory argument.

### Options

*   `-a <days>`: Files older than `<days>` will be considered dust bunnies.
    *   Default: `30` days.
*   `-x <ext1,ext2>`: Comma-separated list of file extensions to **EXCLUDE** from sweeping actions (e.g., `'log,tmp,bak'`).
    *   Default: `log,tmp,bak,swp`.
*   `-m <mode>`: Action mode.
    *   `report` (default): Just list the files. No changes are made.
    *   `archive`: Move files to the archive directory.
    *   `delete`: Permanently delete files. **Use with caution!**
*   `-o <path>`: Specify a custom archive directory for `archive` mode.
    *   Default: `~/.digital_void_archive`.
*   `-f`: Force action without confirmation (use with extreme caution for `archive` or `delete` modes).
*   `-h`: Display the help message and exit.

### Examples

1.  **Just report files older than 90 days in your downloads folder:**
    ```bash
    ./src/dust_bunny_sweeper.sh /home/user/Downloads -a 90
    ```

2.  **Permanently delete all files (except `.log` and `.gz`) older than 7 days in `/var/log/temp` without confirmation:**
    ```bash
    ./src/dust_bunny_sweeper.sh /var/log/temp -a 7 -x "log,gz" -m delete -f
    ```

3.  **Archive old documents (older than 180 days) to a specific cold storage location:**
    ```bash
    ./src/dust_bunny_sweeper.sh /home/user/Documents -a 180 -m archive -o /mnt/cold_storage/digital_void
    ```

4.  **List all files older than 30 days, excluding `.bak` and `.zip` files:**
    ```bash
    ./src/dust_bunny_sweeper.sh /path/to/data -a 30 -x "bak,zip"
    ```

## \uD83D\uDEE0\uFE0F Development & Testing

The utility is a self-contained Bash script.

### Running Tests

To run the automated tests, navigate to the utility's root directory and execute:

```bash
./tests/test_dust_bunny_sweeper.sh
```

The tests create temporary directories and files to simulate various scenarios (old files, new files, different actions) and verify the script's behavior without affecting your actual filesystem.

### Mock Rationale for Tests

The tests are designed to be deterministic and offline. They achieve this by:
*   **Temporary Filesystem**: Using `mktemp -d` to create isolated test directories for each test case, ensuring no side effects on the host system.
*   **Controlled File Timestamps**: Employing `touch -t` with `date --date="N days ago"` to precisely set the modification times of mock files. This allows `find -mtime` to deterministically identify "old" files based on the script's age criteria, regardless of when the test is run.
*   **Simulated User Input**: Using `echo "y" |` or `echo "N" |` to provide non-interactive responses to confirmation prompts, making the tests fully automated.
*   **Environment Variable Mocking**: Setting `export HOME="$TEST_DIR"` to control where the script's default archive directory (`~/.digital_void_archive`) would be created, ensuring it's within the temporary test environment.
