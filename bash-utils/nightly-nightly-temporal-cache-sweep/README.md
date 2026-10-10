# Nightly Temporal Cache Sweeper

## 🌌 Overview

In the ever-shifting sands of digital existence, temporary files and cache detritus can accumulate, becoming ancient relics that weigh down your system. The `Nightly Temporal Cache Sweeper` is a whimsical yet powerful utility designed to detect these temporal anomalies and, with your permission, purge them from your designated directories.

It scans specified paths for files that have lingered beyond their temporal prime (i.e., are older than a given number of days) and can either list them for your review or initiate a "temporal sweep" to remove them.

## ✨ Features

*   **Temporal Anomaly Detection**: Identifies files older than a configurable age.
*   **Whimsical Reporting**: Presents findings with a touch of cosmic flair.
*   **Safe Listing Mode**: By default, only lists files, allowing you to review before any action is taken.
*   **Sweep Protocol**: An optional flag to initiate the deletion of ancient files.
*   **Cross-Platform Compatibility**: Designed for Bash, compatible with both GNU and BSD `date` commands for robust testing.

## 🚀 Usage

To invoke the Temporal Cache Sweeper, use the following syntax:

```bash
./src/temporal_cache_sweeper.sh <directory> [age_in_days] [--sweep]
```

### Arguments:

*   `<directory>`: The absolute or relative path to the directory you wish to scan for ancient files. This is a mandatory argument.
*   `[age_in_days]`: (Optional) An integer specifying the number of days. Files older than this age will be considered "ancient." If omitted, the default age is `7` days.
*   `--sweep`: (Optional) If this flag is present, the utility will proceed to delete the identified ancient files. **Use with caution!** Without this flag, files are only listed.

### Examples:

1.  **List files older than 7 days in your home cache directory (default age):**
    ```bash
    ./src/temporal_cache_sweeper.sh ~/.cache
    ```

2.  **List files older than 30 days in the system's temporary directory:**
    ```bash
    ./src/temporal_cache_sweeper.sh /tmp 30
    ```

3.  **Purge files older than 14 days from a specific project's build cache:**
    ```bash
    ./src/temporal_cache_sweeper.sh ~/projects/my-app/.cache 14 --sweep
    ```

4.  **Purge files older than the default 7 days from `/var/log/old_logs`:**
    ```bash
    ./src/temporal_cache_sweeper.sh /var/log/old_logs --sweep
    ```

## 🛠️ How It Works

The script utilizes the `find` command with the `-mtime` option to locate files based on their modification time. It then processes these findings, either displaying them or invoking `find -delete` for efficient and safe removal.

## 🧪 Testing

To ensure the Temporal Cache Sweeper is functioning correctly and to verify its temporal integrity, run the provided test suite:

```bash
./tests/test_temporal_cache_sweeper.sh
```

The tests create temporary directories and files with specific modification times to deterministically verify listing and sweeping functionalities without affecting your actual system files.
