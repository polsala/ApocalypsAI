# Nightly Temporal Cache Cleaner

## Summary

The `nightly-temporal-cache-cleaner` is a whimsical-yet-useful containerized utility designed to help you manage digital clutter. It scans specified directories for files older than a configurable age and, in live mode, sweeps them away into the temporal void. Think of it as a digital dust bunny sweeper for your forgotten files.

## How it Works

This utility is packaged as a Docker image. Inside, a Python script (`app.py`) performs the core logic:

1.  It takes a comma-separated list of target directories, an age threshold (in days), and a dry-run flag as input.
2.  For each target directory, it recursively walks through all files.
3.  It checks the modification time (`mtime`) of each file.
4.  If a file's `mtime` is older than the specified age threshold, it's identified as "temporal detritus."
5.  In dry-run mode, it merely reports which files *would* be deleted. In live mode, it proceeds to delete them.

## Usage

The utility is run via Docker. You need to mount the directories you want to scan into the container.

### Build the Docker Image (if not using a pre-built one)

```bash
docker build -t temporal-cache-cleaner .
```

### Run the Cleaner

You can configure the cleaner using environment variables or command-line arguments.

**Environment Variables:**

*   `TARGET_DIRS`: A comma-separated string of directories to scan (e.g., `/app/cache,/app/logs`). **Required.**
*   `AGE_DAYS`: The age in days. Files older than this will be considered for sweeping. Defaults to `30`.
*   `DRY_RUN`: Set to `true` for a dry run (default), or `false` to perform actual deletions.

**Command-Line Arguments (override environment variables):**

*   `--dirs <path1,path2>`: Comma-separated list of directories.
*   `--age <days>`: Age threshold in days.
*   `--live`: Flag to enable live deletion (disables dry run).

#### Example: Dry Run (Recommended first step!)

This command will scan `/var/log` and `/tmp/cache` within the container (which map to your host's `/var/log` and `/tmp/my_app_cache`) and report files older than 7 days, without deleting anything.

```bash
docker run --rm \
  -v /var/log:/var/log \
  -v /tmp/my_app_cache:/tmp/cache \
  -e TARGET_DIRS="/var/log,/tmp/cache" \
  -e AGE_DAYS="7" \
  -e DRY_RUN="true" \
  temporal-cache-cleaner
```

Or using CLI arguments:

```bash
docker run --rm \
  -v /var/log:/var/log \
  -v /tmp/my_app_cache:/tmp/cache \
  temporal-cache-cleaner --dirs /var/log,/tmp/cache --age 7
```

#### Example: Live Sweep (Use with Caution!)

This command will actually delete files older than 30 days in the mounted `/tmp/my_app_cache` directory.

```bash
docker run --rm \
  -v /tmp/my_app_cache:/tmp/cache \
  -e TARGET_DIRS="/tmp/cache" \
  -e AGE_DAYS="30" \
  -e DRY_RUN="false" \
  temporal-cache-cleaner
```

Or using CLI arguments:

```bash
docker run --rm \
  -v /tmp/my_app_cache:/tmp/cache \
  temporal-cache-cleaner --dirs /tmp/cache --age 30 --live
```

## Development and Testing

To develop or test this utility:

1.  **Python Code Tests**: Run `python tests/test_app.py` to execute the unit tests for the Python logic. These tests use mocks to simulate file system interactions, ensuring determinism and isolation.
2.  **Docker Build Test**: Run `bash tests/test_docker_build.sh` to verify that the Docker image can be built successfully. This script will build the image and then remove it.
