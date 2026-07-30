# Nightly Temporal Docker Echo Chamber

## Summary
A whimsical-yet-useful Docker utility that allows you to snapshot the filesystem state of a running container and "rewind" it to a previous snapshot. This creates a "temporal echo chamber" for your development and testing, enabling safe experimentation, quick rollbacks, and idempotent testing of destructive commands without constantly rebuilding images or manually cleaning up.

## Classifier
`docker-tools`

## Usage

### Prerequisites
- Docker installed and running.
- Bash shell.

### How it works
The utility uses `docker commit` to create new images (snapshots) from a running container's state. When you "rewind," it stops and removes the current container, then recreates it from a chosen snapshot image.

### Commands

1.  **`init <image_name> <container_name>`**:
    Initializes a new "echo chamber." It pulls the specified base `image_name` (e.g., `alpine:latest`), creates a new container named `container_name`, and takes an initial snapshot, tagging it as `<container_name>-snapshot-initial`.
    Example: `./src/echo_chamber.sh init alpine:latest my-dev-env`

2.  **`snapshot <container_name> <snapshot_tag>`**:
    Takes a snapshot of the current state of `container_name`. A new Docker image will be created and tagged as `<container_name>-snapshot-<snapshot_tag>`.
    Example: `./src/echo_chamber.sh snapshot my-dev-env pre-install`

3.  **`rewind <container_name> <snapshot_tag>`**:
    "Rewinds" the `container_name` to a previously taken snapshot. The current container is stopped and removed, and a new one is started from the image `<container_name>-snapshot-<snapshot_tag>`.
    Example: `./src/echo_chamber.sh rewind my-dev-env pre-install`

4.  **`run <container_name> <command>`**:
    Executes a command inside the specified `container_name`.
    Example: `./src/echo_chamber.sh run my-dev-env "ls -la /app"`
    Example: `./src/echo_chamber.sh run my-dev-env "sh -c 'echo \"Hello from the past!\" > /app/message.txt'"`

5.  **`cleanup <container_name>`**:
    Stops and removes the `container_name` and all associated snapshot images created by this utility.
    Example: `./src/echo_chamber.sh cleanup my-dev-env`

## Example Workflow

```bash
# 1. Initialize the echo chamber
./src/echo_chamber.sh init alpine:latest my-test-container

# 2. Run some commands and take a snapshot
./src/echo_chamber.sh run my-test-container "sh -c 'echo \"First state\" > /app/state.txt'"
./src/echo_chamber.sh snapshot my-test-container first-state

# 3. Run more commands (these will be undone later)
./src/echo_chamber.sh run my-test-container "sh -c 'echo \"Second state\" > /app/state.txt; mkdir /app/new_dir'"
./src/echo_chamber.sh run my-test-container "ls -la /app" # Should show state.txt and new_dir

# 4. Rewind to the 'first-state'
./src/echo_chamber.sh rewind my-test-container first-state

# 5. Verify the rewind (second state changes should be gone)
./src/echo_chamber.sh run my-test-container "cat /app/state.txt" # Should output "First state"
./src/echo_chamber.sh run my-test-container "ls -la /app" # Should NOT show new_dir

# 6. Clean up
./src/echo_chamber.sh cleanup my-test-container
```
