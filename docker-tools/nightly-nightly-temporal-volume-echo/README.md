# Nightly Temporal Volume Echo

A Dockerized utility to capture, list, and restore 'temporal echoes' (snapshots) of Docker volumes. Ever wished you could rewind your Docker volume to a previous state? The Temporal Volume Echo lets you do just that, creating named snapshots of your volume's contents and restoring them with a simple command. Perfect for development, testing, or just playing with temporal paradoxes!

## Features

*   **Capture Echo**: Take a snapshot of any Docker volume's current state.
*   **List Echoes**: See all available snapshots for a given volume.
*   **Restore Echo**: Revert a Docker volume to a previously captured snapshot.

## How it Works

The utility runs as a Docker container that interacts with your Docker daemon (via `/var/run/docker.sock`). It uses a dedicated Docker volume (`temporal-echo-data`) to store all snapshots. When you capture an echo, it creates a temporary container, mounts your target volume and the `temporal-echo-data` volume, and uses `tar` to copy the contents of your target volume into a timestamped archive within `temporal-echo-data`. Restoration works in reverse.

## Setup

1.  **Build the Docker Image**:
    ```bash
    docker build -t temporal-volume-echo .
    ```

2.  **Ensure Snapshot Data Volume Exists**:
    The utility uses a Docker volume named `temporal-echo-data` to store all snapshots. Create it if it doesn't exist:
    ```bash
    docker volume create temporal-echo-data
    ```

## Usage

The `temporal-volume-echo` container needs access to your Docker daemon and the `temporal-echo-data` volume.

### General Command Structure

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v temporal-echo-data:/snapshots \
  temporal-volume-echo <command> <volume_name> [snapshot_name]
```

### 1. Capture a Temporal Echo

Capture the current state of a Docker volume. If `snapshot_name` is omitted, a timestamped name will be generated.

```bash
# Capture with an auto-generated timestamped name
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v temporal-echo-data:/snapshots \
  temporal-volume-echo capture my_app_data_volume

# Capture with a specific name
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v temporal-echo-data:/snapshots \
  temporal-volume-echo capture my_app_data_volume "pre_feature_x_update"
```

### 2. List Temporal Echoes

List all available snapshots for a given Docker volume.

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v temporal-echo-data:/snapshots \
  temporal-volume-echo list my_app_data_volume
```

### 3. Restore a Temporal Echo

Restore a Docker volume to a previously captured snapshot. **WARNING: This will overwrite the current contents of the target volume.**

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v temporal-echo-data:/snapshots \
  temporal-volume-echo restore my_app_data_volume "pre_feature_x_update"
```

## Development & Testing

See the `tests/` directory for examples of how to test this utility.
