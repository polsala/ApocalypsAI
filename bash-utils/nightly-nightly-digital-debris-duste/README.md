# Nightly Digital Debris Duster

## ✨ Whimsical Cleanup for Your Digital Wasteland ✨

Are your digital realms feeling a bit... dusty? Is your filesystem cluttered with forgotten files, transient wisps, and hollow caverns? Fear not, for the Nightly Digital Debris Duster is here to bring a breath of fresh air to your system!

This whimsical Bash script helps you identify and optionally sweep away old, unused files, common temporary files, and empty directories, making your digital environment feel lighter and more organized.

## Usage

To invoke the Duster, simply run the script with your desired target directories and options:

```bash
bash src/digital_debris_duster.sh [OPTIONS] [TARGET_DIRECTORY...]
```

If no `TARGET_DIRECTORY` is specified, the script will default to the current directory (`.`).

### Options

*   `-a <days>`: Specify the age in days for files to be considered 'old'. Files older than this many days will be flagged. (Default: 30 days).
*   `-d`: **Dry Run Mode**. The script will identify all debris but will not perform any actual deletions. Perfect for a reconnaissance mission before the big sweep!
*   `-i`: **Interactive Mode**. For each piece of debris found, the script will ask for your confirmation before sweeping it away. For the cautious cleaner.
*   `-h`: Display the help message and exit.

### Examples

1.  **Dust the current directory for default old files (30 days) and temporary clutter (dry run):**
    ```bash
bash src/digital_debris_duster.sh -d .
    ```

2.  **Sweep away files older than 60 days in your home directory, interactively:**
    ```bash
bash src/digital_debris_duster.sh -i -a 60 ~/my_documents
    ```

3.  **Perform a full, non-interactive sweep of `/tmp` and `/var/log` (use with caution!):**
    ```bash
bash src/digital_debris_duster.sh /tmp /var/log
    ```

4.  **Just see what's old in a specific project directory, without touching anything:**
    ```bash
bash src/digital_debris_duster.sh -d ~/projects/my_old_project
    ```

## What it Sweeps

*   **Ancient Scrolls**: Files older than the specified age (default 30 days).
*   **Fleeting Wisps**: Common temporary files like `*.tmp`, `*.bak`, `*~`, `.DS_Store`, `Thumbs.db`.
*   **Hollow Caverns**: Empty directories that serve no purpose.

## Important Notes

*   **Permissions**: The script will only be able to clean files and directories for which your user has appropriate permissions.
*   **System Directories**: Critical system directories (e.g., `/proc`, `/sys`, `/dev`) are excluded by default to prevent accidental system instability.
*   **Backup**: While this tool is designed to be helpful, always exercise caution when deleting files. Consider backing up important data before a major cleanup, especially when not using dry-run or interactive modes.

Happy dusting! 🧹
