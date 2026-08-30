# Nightly Digital Flora Pruner

## 🌿 Overview

In the ever-expanding digital wilderness, files can accumulate like overgrown weeds, consuming precious storage and obscuring the vibrant digital ecosystem. The `nightly-digital-flora-pruner` is your trusty digital gardener, a whimsical bash utility designed to help you identify and 'prune' withered digital flora (old, unused files) from your specified directories.

Treat your filesystem as a thriving garden. This tool helps you maintain its health by gently removing the digital leaves that have long since fallen and are no longer contributing to the vibrant life of your system.

## ✨ Features

*   **Digital Garden Tending**: Specify a directory to scan for old files.
*   **Age-Based Pruning**: Define how many days a file must be unaccessed to be considered 'withered'.
*   **Dry Run Mode**: Preview which files would be pruned without actually deleting them.
*   **Interactive Confirmation**: Get a chance to review and confirm deletions before they happen.
*   **Force Pruning**: Skip confirmation for automated or confident pruning.

## 🚀 Usage

```bash
bash src/pruner.sh -d <directory_path> -a <age_in_days> [-n] [-f]
```

### Arguments:

*   `-d <directory_path>`: **Required**. The path to your digital garden (directory) to be tended. The script will recursively search for files within this directory.
*   `-a <age_in_days>`: **Required**. Files older than this many days (based on last access time) will be considered withered digital flora and candidates for pruning.
*   `-n`: **Optional**. Perform a dry run. The script will identify and list the files that *would* be pruned, but will not actually delete anything. Useful for previewing changes.
*   `-f`: **Optional**. Force pruning. Skip the interactive confirmation step and proceed directly with deletion. Use with caution!

### Examples:

1.  **Dry run to see files older than 30 days in `/var/log`:**
    ```bash
    bash src/pruner.sh -d /var/log -a 30 -n
    ```

2.  **Interactively prune files older than 7 days in your home directory's `temp` folder:**
    ```bash
    bash src/pruner.sh -d ~/temp -a 7
    ```

3.  **Force prune files older than 90 days in `/tmp` without confirmation:**
    ```bash
    bash src/pruner.sh -d /tmp -a 90 -f
    ```

## ⚠️ Important Notes

*   **Access Time (`-atime`)**: This script uses `find -atime` to determine file age based on *last access time*. Be aware that some systems or configurations (e.g., `noatime` mount option) might not update access times reliably. In such cases, files might appear 'new' even if they haven't been used in a long time.
*   **Permissions**: The script requires appropriate read and write permissions for the specified directory and its contents to function correctly.
*   **Backup**: Always ensure you have backups of important data before running any deletion utility, especially with the `-f` (force) flag.

## 🛠️ Development

This utility is a simple bash script. Contributions are welcome to enhance its whimsical nature or add more robust gardening features!
