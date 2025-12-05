# Nightly Ephemeral Data Sweeper

## Purpose

The `nightly-ephemeral-data-sweeper` is a whimsical yet practical utility designed to help you maintain a clean digital workspace. It identifies and offers to remove transient files such as logs, cache files, and temporary build artifacts based on user-defined paths, age thresholds, and file patterns. By regularly sweeping away this 'digital dust', you can prevent unnecessary disk space consumption and improve system performance.

## Usage

1.  **Create a configuration file** (e.g., `config.yaml`) based on `config.example.yaml`.
    Define the directories to scan, the maximum age (in days) for files to be considered ephemeral, and optional file patterns.

    ```yaml
    ephemeral_paths:
      - path: /var/log/my_app
        max_age_days: 7
        patterns: ["*.log", "*.old"]
      - path: ~/.cache/my_project
        max_age_days: 30
        patterns: ["*"] # Matches all files in this path
      - path: ./temp_build_output
        max_age_days: 14
        patterns: ["*.tmp", "*.bak"]
    ```

2.  **Run the sweeper in dry-run mode** to see what files would be affected:

    ```bash
    python3 src/sweeper.py --config config.yaml --dry-run
    ```

3.  **Run the sweeper to actually remove files** (use with caution!):

    ```bash
    python3 src/sweeper.py --config config.yaml
    ```

## Arguments

*   `--config <path>`: Path to the YAML configuration file (required).
*   `--dry-run`: If present, the utility will only report files to be removed, without actually deleting them (default: `False`).
