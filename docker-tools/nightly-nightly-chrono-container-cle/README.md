# Nightly Chrono-Container Cleaner

The ApocalypsAI community thrives on fresh, vibrant containers! This utility, the "Chrono-Container Cleaner," helps you identify "dusty" (old or outdated) Docker images lurking in your `Dockerfile`s and `docker-compose.yml` files. It's like an archaeological dig for your container ecosystem, unearthing ancient layers and suggesting a 'freshening' ritual to keep your deployments spry and secure.

## Features

*   **Image Archaeology**: Scans specified directories for `Dockerfile` and `docker-compose.yml` files.
*   **Temporal Analysis**: Extracts image names and attempts to determine their age (local build date or Docker Hub last push date).
*   **Dust Detection**: Flags images older than a configurable threshold as "dusty."
*   **Freshening Suggestions**: Provides whimsical advice on how to update your ancient containers.

## Usage

### Prerequisites

*   Docker installed and running (for local image inspection).
*   Python 3.8+ and `pip` (if running directly).
*   `docker-compose` (if you have `docker-compose.yml` files).

### Running as a Container (Recommended)

Build the utility's Docker image:
```bash
docker build -t chrono-container-cleaner .
```

Then, run it, mounting your project directory and the Docker socket (for local image inspection):
```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$(pwd)/my_project_dir:/app/project" \
  chrono-container-cleaner \
  python src/main.py --path /app/project --threshold-days 180
```
Replace `/my_project_dir` with the path to your project containing Dockerfiles.

### Running Directly

1.  Navigate to the `nightly-chrono-container-cleaner` directory.
2.  Install dependencies:
    ```bash
    pip install -r src/requirements.txt
    ```
3.  Run the script:
    ```bash
    python src/main.py --path /path/to/your/project --threshold-days 365
    ```

### Arguments

*   `--path <directory>`: The root directory to scan for Dockerfiles and docker-compose files. (Required)
*   `--threshold-days <days>`: Images older than this many days will be flagged as "dusty." Default is 365 days.

## Examples

Scan the current directory for images older than 6 months:
```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$(pwd):/app/project" \
  chrono-container-cleaner \
  python src/main.py --path /app/project --threshold-days 180
```

## Development & Testing

### Running Tests

To run the automated tests, ensure you have `pytest` installed (`pip install pytest`).

```bash
pytest tests/
```

The tests use mocks for file system operations, Docker API calls, and external HTTP requests to ensure determinism and offline execution.
