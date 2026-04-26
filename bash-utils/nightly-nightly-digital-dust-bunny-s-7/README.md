# Nightly Digital Dust Bunny Sweeper

## Summary

This whimsical Bash script helps you declutter your digital space by identifying old, unused files and directories. It playfully categorizes them as 'digital dust bunnies' (files) or 'forgotten cobwebs' (directories) and suggests potential cleanup actions. Think of it as a friendly digital janitor, pointing out where the dust has settled.

## Usage

```bash
./src/dust_bunny_sweeper.sh [OPTIONS]
```

### Options:

*   `-p, --path <directory>`: The starting directory to scan. Defaults to the current directory (`.`).
*   `-a, --age-days <days>`: The minimum age in days for a file/directory to be considered a 'dust bunny' or 'cobweb'. Defaults to `90` days.
*   `-e, --exclude <pattern>`: A comma-separated list of patterns to exclude from the scan (e.g., `.git,node_modules`). Can be used multiple times. Defaults to common system and development directories.
*   `-s, --suggest-commands`: Suggest `rm` commands for identified items. **Use with caution!** Always review suggested commands before execution.
*   `-h, --help`: Display this help message.

### Examples:

1.  **Scan the current directory for items older than 180 days:**
    ```bash
    ./src/dust_bunny_sweeper.sh --age-days 180
    ```

2.  **Scan a specific project directory, excluding `build` folders:**
    ```bash
    ./src/dust_bunny_sweeper.sh --path ~/my_project --exclude build
    ```

3.  **List items and suggest `rm` commands (review carefully!):**
    ```bash
    ./src/dust_bunny_sweeper.sh --suggest-commands
    ```

## How it Works

The script uses the `find` command to locate files and directories that haven't been accessed or modified within the specified age threshold. It then filters out common system paths and user-defined exclusions to focus on potentially unused user data. The output is formatted with whimsical labels to make cleanup a bit more fun.

## Safety Note

This tool is designed to *suggest* cleanup. When using `--suggest-commands`, always carefully review the output before executing any `rm` commands. Deleting files permanently can lead to data loss. It's recommended to back up important data before performing any cleanup actions.
