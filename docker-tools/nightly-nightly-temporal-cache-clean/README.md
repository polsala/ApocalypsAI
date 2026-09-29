# Nightly Temporal Cache Cleaner

A containerized utility designed to combat 'data entropy' by identifying and optionally removing old, forgotten files from specified directories. It helps stabilize your digital timelines by clearing out 'temporal echoes' – files that have lingered beyond their useful lifespan.

## Features

*   **Age-based Filtering**: Specify how old a file must be (in days) to be considered for cleanup.
*   **Recursive Scanning**: Scans directories and their subdirectories for eligible files.
*   **Dry Run Mode**: Preview which files would be affected without making any changes.
*   **Deletion Mode**: Permanently remove identified old files.
*   **Containerized**: Runs in an isolated Docker environment, ensuring consistent operation across different systems.

## How to Build

To build the Docker image, navigate to the `nightly-temporal-cache-cleaner` directory and run:

```bash
docker build -t temporal-cache-cleaner .
```

## How to Use

The utility requires a target path and an age threshold. You can run it in dry-run mode to see what would happen, or in delete mode to actually remove files.

### Parameters

*   `--path <directory>`: **Required**. The absolute path to the directory to scan. This path must be mounted into the Docker container.
*   `--age <days>`: **Required**. Files older than this many days will be targeted.
*   `--dry-run`: **Optional**. If present, the utility will only list files that *would* be deleted, without actually deleting them. This is the default behavior if `--delete` is not specified.
*   `--delete`: **Optional**. If present, the utility will actually delete the identified old files. **Use with caution!**

### Examples

1.  **Dry run: See files older than 30 days in `/my_data` (mounted as `/data` in container):**

    ```bash
    docker run --rm -v /my_data:/data temporal-cache-cleaner --path /data --age 30 --dry-run
    ```

2.  **Delete: Remove files older than 7 days in `/var/log/old_logs` (mounted as `/logs` in container):**

    ```bash
    docker run --rm -v /var/log/old_logs:/logs temporal-cache-cleaner --path /logs --age 7 --delete
    ```

3.  **Default dry run (no explicit `--dry-run`):**

    ```bash
    docker run --rm -v /tmp/cache:/cache temporal-cache-cleaner --path /cache --age 60
    ```

## Development

The core logic is implemented in `src/cleaner.py`. The `Dockerfile` sets up a Python environment and uses `src/entrypoint.sh` to run the Python script with passed arguments.

Tests are located in `tests/test_cleaner.py` and can be run using `python -m unittest tests/test_cleaner.py` (after installing `pytest` if you prefer, though `unittest` is sufficient).
