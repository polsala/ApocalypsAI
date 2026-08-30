# Nightly Cobweb Sweeper

A containerized utility designed to help you keep your project directories tidy by identifying "digital cobwebs" – temporary files, large build artifacts, empty directories, and potentially sensitive configuration files. Run it against any directory to get a quick report on potential cleanup opportunities.

## Features

*   **Temporary File Detection**: Flags files ending with common temporary extensions (`.tmp`, `.bak`, `~`, `#*#`).
*   **Large File Identification**: Reports files exceeding a configurable size threshold (default: 10MB).
*   **Empty Structure Detection**: Finds empty files and directories.
*   **Sensitive Pattern Scan**: Identifies common sensitive file names like `.env` or `id_rsa`.
*   **Containerized**: Runs in an isolated Docker container, ensuring consistent scanning environment and no host dependencies other than Docker itself.

## Usage

1.  **Build the Docker Image**:
    ```bash
    docker build -t nightly-cobweb-sweeper .
    ```

2.  **Scan a Directory**:
    Navigate to the directory you want to scan and run:
    ```bash
    docker run --rm -v "$(pwd):/scan_target" nightly-cobweb-sweeper
    ```
    The `$(pwd)` part mounts your current working directory into the container at `/scan_target`. The `--rm` flag ensures the container is removed after the scan.

    You can also specify a different target directory within the container if you mount it differently:
    ```bash
    docker run --rm -v /path/to/your/project:/my_project_dir nightly-cobweb-sweeper /my_project_dir
    ```

## Configuration (via Environment Variables)

You can customize the scanner's behavior by passing environment variables to the `docker run` command:

*   `MAX_FILE_SIZE_MB`: Maximum allowed file size in megabytes. Files larger than this will be flagged. Default: `10`.
    Example: `docker run --rm -e MAX_FILE_SIZE_MB=5 -v "$(pwd):/scan_target" nightly-cobweb-sweeper`
*   `EXCLUDE_PATTERNS`: A comma-separated list of glob patterns (relative to the mounted root, e.g., `/scan_target/*.log`) to exclude from scanning. The patterns are matched against the full path of the file/directory within the container.
    Example: `docker run --rm -e EXCLUDE_PATTERNS="/scan_target/*.log,/scan_target/node_modules/*" -v "$(pwd):/scan_target" nightly-cobweb-sweeper`

## Output

The utility will print a categorized report to standard output, listing all detected cobwebs.
