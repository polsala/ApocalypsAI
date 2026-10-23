# Nightly Digital Dust Bunny Sweeper

In the post-apocalyptic digital wasteland, even servers gather dust bunnies. Over time, forgotten log files, temporary caches, and abandoned project directories can accumulate, hogging precious storage and slowing down critical systems. The `Nightly Digital Dust Bunny Sweeper` is here to help!

This whimsical-yet-useful bash script intelligently identifies and sweeps away old, unused files and directories, ensuring your digital infrastructure remains lean, efficient, and ready for whatever the next dawn brings.

## Features

*   **Intelligent Cleanup**: Targets files and directories older than a specified age.
*   **Safety First**: Includes a list of critical system paths that the sweeper will warn about or avoid, preventing accidental system damage.
*   **Dry Run Mode**: Simulate the cleanup operation to see what would be deleted without making any actual changes.
*   **Interactive Confirmation**: Prompts for user confirmation before proceeding with deletion (can be bypassed with `--force`).
*   **Whimsical Output**: Keeps spirits high with themed messages during the sweep.

## Usage

To run the Digital Dust Bunny Sweeper, use the following syntax:

```bash
./src/dust_bunny_sweeper.sh <directory> <age_in_days> [--dry-run] [--force]
```

### Arguments

*   `<directory>`: The path to scan for digital dust bunnies (e.g., `/var/log`, `/tmp`, `/home/user/old_projects`).
*   `<age_in_days>`: Files and directories older than this number of days will be considered 'dust bunnies' and targeted for deletion.

### Options

*   `--dry-run`: (Optional) Perform a simulated sweep. The script will list all items that *would* be deleted, but no actual files will be removed. This is highly recommended for a first run!
*   `--force`: (Optional) Skip the interactive confirmation prompt and proceed directly with deletion. Use with extreme caution, especially on critical paths.

## Examples

1.  **See what would be cleaned in `/var/log` older than 30 days (dry run):**
    ```bash
    ./src/dust_bunny_sweeper.sh /var/log 30 --dry-run
    ```

2.  **Clean up `/tmp` of anything older than 7 days, with confirmation:**
    ```bash
    ./src/dust_bunny_sweeper.sh /tmp 7
    ```

3.  **Force-clean an old project directory `/home/user/old_projects` older than 180 days:**
    ```bash
    ./src/dust_bunny_sweeper.sh /home/user/old_projects 180 --force
    ```

## Safety Warning

While the script includes safeguards for critical system paths, **always exercise caution** when running deletion scripts. It is highly recommended to use the `--dry-run` option first and review the output carefully before performing any actual deletions. The ApocalypsAI Nightly Integrator is not responsible for any data loss caused by misuse of this utility.
