# Nightly Digital Dust Bunny Sweeper

## Summary
The Nightly Digital Dust Bunny Sweeper is a whimsical-yet-useful containerized utility designed to keep your digital spaces clean in the post-apocalyptic world. It identifies and removes old, forgotten files (our "digital dust bunnies") from specified directories, preventing clutter and conserving precious storage resources.

## How it Works
This tool runs a simple Bash script inside a Docker container. You provide it with a list of directories to clean and a maximum age for files to retain. Any files older than the specified age in the target directories will be gently swept away.

## Usage

1.  **Build the Docker image:**
    ```bash
    docker build -t digital-dust-bunny-sweeper .
    ```

2.  **Run the sweeper:**
    Mount the directories you want to clean as volumes into the container.
    Specify the directories to clean and the age threshold (in days).

    ```bash
    # Example: Clean files older than 7 days in /var/log and /tmp
    docker run --rm \
      -v /var/log:/var/log:rw \
      -v /tmp:/tmp:rw \
      digital-dust-bunny-sweeper \
      /var/log /tmp --age 7
    ```

    **Arguments:**
    *   `[DIRECTORY...]`: One or more paths to directories inside the container that should be cleaned. These should correspond to volumes you've mounted.
    *   `--age <DAYS>`: (Optional) The maximum age (in days) for files to be kept. Files older than this will be deleted. Defaults to `30` days if not specified.
    *   `--dry-run`: (Optional) Perform a dry run, listing files that *would* be deleted without actually deleting them.
    *   `--help`: (Optional) Display the help message.

    **Important:** Ensure the mounted volumes have write permissions if you intend to delete files.

## Configuration
The tool is configured via command-line arguments when running the Docker container. No internal configuration files are needed.

## Examples

*   **Dry run to see what would be cleaned in `/app/logs` older than 14 days:**
    ```bash
    docker run --rm \
      -v /path/to/your/app/logs:/app/logs:rw \
      digital-dust-bunny-sweeper \
      /app/logs --age 14 --dry-run
    ```

*   **Clean `/data/cache` and `/data/temp` older than 3 days:**
    ```bash
    docker run --rm \
      -v /path/to/your/data/cache:/data/cache:rw \
      -v /path/to/your/data/temp:/data/temp:rw \
      digital-dust-bunny-sweeper \
      /data/cache /data/temp --age 3
    ```

## Development & Testing
See the `tests/test_sweeper.sh` file for how to run the automated tests.
