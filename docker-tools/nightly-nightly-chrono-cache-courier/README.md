# Nightly Chrono-Cache Courier

A whimsical-yet-useful containerized ephemeral note-sharing and retrieval system for quick, temporary messages across your team or personal projects. Think of it as a transient message board that automatically cleans itself after a "temporal cycle" (default: 24 hours).

## Features

*   **Ephemeral Storage**: Store short notes or snippets with a key.
*   **Time-Based Cleaning**: Notes are automatically removed after a configurable retention period.
*   **Containerized**: Runs in a Docker container, providing a consistent and isolated environment.
*   **Simple CLI**: Easy-to-use command-line interface for adding, retrieving, and listing notes.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-chrono-cache-courier` directory and build the Docker image:

```bash
docker build -t chrono-cache-courier .
```

### 2. Run the Container and Interact

You can run commands directly against the container. The cache data is stored in a Docker volume, so it persists across container restarts (until cleaned).

**Example: Add a note**

```bash
docker run -v chrono-cache-data:/cache/notes chrono-cache-courier add "project-status" "Frontend dev is 80% complete, backend needs review."
```

**Example: Retrieve a note**

```bash
docker run -v chrono-cache-data:/cache/notes chrono-cache-courier get "project-status"
```

**Example: List all active notes**

```bash
docker run -v chrono-cache-data:/cache/notes chrono-cache-courier list
```

**Example: Manually clean old notes**

This command will remove any notes older than the configured `CHRONO_RETENTION_HOURS` (default: 24 hours).

```bash
docker run -v chrono-cache-data:/cache/notes chrono-cache-courier clean
```

**Example: Run with custom retention (e.g., 1 hour)**

```bash
docker run -e CHRONO_RETENTION_HOURS=1 -v chrono-cache-data:/cache/notes chrono-cache-courier add "quick-thought" "Remember to check the anomaly logs."
```

### 3. Using Docker Compose (Recommended for persistent service)

For a more persistent and easier-to-manage setup, you can use `docker-compose.yml`.

**`docker-compose.yml`**:
```yaml
version: '3.8'
services:
  chrono-cache:
    build: .
    image: chrono-cache-courier:latest
    volumes:
      - chrono-cache-data:/cache/notes
    environment:
      - CHRONO_RETENTION_HOURS=24 # Default retention, can be overridden
    # This service is designed to run commands, not as a long-running daemon.
    # We'll override the entrypoint for interactive use or specific commands.
    # For example, to run 'list' command:
    # docker-compose run chrono-cache list
    # To run 'add' command:
    # docker-compose run chrono-cache add "key" "value"
    # To run 'clean' command:
    # docker-compose run chrono-cache clean
    # The default CMD is 'help', so 'docker-compose run chrono-cache' will show help.

volumes:
  chrono-cache-data:
```

To use with Docker Compose:

1.  Place the `docker-compose.yml` file in the same directory as your `Dockerfile` and `src/app.sh`.
2.  Build the service:
    ```bash
    docker-compose build
    ```
3.  Run commands:
    ```bash
    docker-compose run chrono-cache add "urgent-task" "Deploy temporal distortion stabilizer."
    docker-compose run chrono-cache get "urgent-task"
    docker-compose run chrono-cache list
    docker-compose run chrono-cache clean
    ```

## Development and Testing

### Running Tests

The tests use `shunit2`, a unit test framework for Bourne-like shells.

1.  **Install `shunit2`**:
    ```bash
    # On Debian/Ubuntu
    sudo apt-get update && sudo apt-get install shunit2
    # Or download it manually and place it in your PATH or current directory
    # wget https://raw.githubusercontent.com/kward/shunit2/master/shunit2
    # chmod +x shunit2
    ```
    *Mock rationale: `shunit2` is a standard shell testing framework. Its installation is a prerequisite for running tests, but the tests themselves are self-contained and deterministic once `shunit2` is available.* 

2.  **Execute Tests**:
    ```bash
    bash tests/test_app.sh
    ```

The tests create a temporary directory for cache files (`/tmp/chrono_cache_test_*`) to ensure isolation and clean up after themselves. File modification times are explicitly set in tests using `touch -t` and `date -r @<timestamp>` to ensure deterministic results for the `clean` function, regardless of when the tests are run.
