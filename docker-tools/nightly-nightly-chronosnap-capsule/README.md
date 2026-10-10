# Nightly Chronosnap Capsule

A whimsical-yet-useful Docker-based utility for time-traveling your directories! The Chronosnap Capsule allows you to create timestamped snapshots of any specified directory and restore them at will. This is incredibly useful for development environments, testing, or any scenario where you need to quickly revert changes or maintain consistent states.

## Features

*   **Snapshot Creation**: Easily capture the current state of a directory.
*   **Snapshot Restoration**: Revert a directory to a previously saved state.
*   **Snapshot Listing**: View all available temporal echoes.
*   **Containerized**: Runs as a lightweight Docker container, easily integrated into existing Docker Compose setups.

## How it Works

The `chronosnap-capsule` container mounts two volumes: one for the `TARGET_DIR` (the directory whose state you want to manage) and one for the `SNAPSHOT_ROOT_DIR` (where all your timestamped `.tar.gz` snapshots will be stored). It uses `tar` for efficient archiving and restoration.

## Usage

1.  **Build the Docker Image**:

    Navigate to the `nightly-chronosnap-capsule` directory and run:

    ```bash
    docker build -t chronosnap-capsule .
    ```

2.  **Run the Container (Example with Docker Compose)**:

    The `docker-compose.yml` file provides an example of how to integrate the `chronosnap-capsule` as a sidecar to your application. It assumes your application (e.g., `my_app`) writes data to a volume mounted at `/data`, and the capsule will manage snapshots of this `/data` directory.

    ```bash
    docker compose up -d
    ```

3.  **Interact with the Chronosnap Capsule**:

    You can execute commands directly on the `chronosnap` service (or standalone container):

    *   **Create a snapshot**:

        ```bash
        docker compose exec chronosnap /usr/local/bin/entrypoint.sh snapshot
        ```

    *   **List available snapshots**:

        ```bash
        docker compose exec chronosnap /usr/local/bin/entrypoint.sh list
        ```
        This will output a list of timestamps, e.g., `20231027103000`.

    *   **Restore a snapshot** (replace `<timestamp>` with one from the list):

        ```bash
        docker compose exec chronosnap /usr/local/bin/entrypoint.sh restore <timestamp>
        ```

## Development & Testing

To run the automated tests, ensure you have Docker installed and then execute:

```bash
./tests/test_chronosnap.sh
```

This script will build the image, simulate file changes, take snapshots, restore them, and verify the outcomes, then clean up the temporary resources.
