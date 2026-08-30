# nightly-dust-bunny-sweeper

A whimsical-yet-useful containerized utility to sweep away digital dust bunnies: old Docker images, containers, and volumes that are no longer needed. Keep your Docker environment tidy and reclaim precious disk space!

## 🗑️ What it Does

This tool identifies and optionally prunes the following types of "digital dust bunnies":

1.  **Dangling Images**: Docker images that are not tagged and not referenced by any container. These are often intermediate layers from failed builds or old versions.
2.  **Exited Containers**: Containers that have stopped running. While they don't consume CPU/memory, they still occupy disk space with their filesystem layers and logs.
3.  **Unused Volumes**: Docker volumes that are not currently attached to any container. These can accumulate over time from removed containers.

By default, the `nightly-dust-bunny-sweeper` runs in **report-only mode**, showing you what *could* be cleaned without making any changes. To actually perform the cleanup, you must explicitly pass the `--prune` flag.

## 🚀 How to Use

### Prerequisites

*   Docker installed and running on your host machine.
*   Access to the Docker daemon socket (`/var/run/docker.sock`).

### 1. Build the Docker Image (Optional, or use pre-built)

```bash
docker build -t apocalypsai/dust-bunny-sweeper .
```

### 2. Run in Report-Only Mode (Recommended First Step)

This will show you all the digital dust bunnies without removing anything.

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/dust-bunny-sweeper
```

Example Output:
```
ApocalypsAI Digital Dust Bunny Sweeper Report
---------------------------------------------

--- Dangling Images (untagged layers) ---
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
<none>              <none>              a1b2c3d4e5f6        2 hours ago         10MB
<none>              <none>              b2c3d4e5f6a1        5 hours ago         20MB

--- Exited Containers ---
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS               NAMES
c1d2e3f4g5h6        myimage:latest      "/bin/sh"           3 hours ago         Exited (0) 2 hours ago                          old_app_1
d2e3f4g5h6c1        another:v1          "/bin/bash"         6 hours ago         Exited (137) 5 hours ago                        temp_service_2

--- Unused Volumes ---
DRIVER              VOLUME NAME
local               my_old_data_volume
local               temp_log_volume

---------------------------------------------
Report complete. Run with '--prune' to remove identified resources.
```

### 3. Run in Prune Mode (To Clean Up)

**Use with caution!** This will permanently remove the identified resources.

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/dust-bunny-sweeper --prune
```

Example Output:
```
ApocalypsAI Digital Dust Bunny Sweeper Report
---------------------------------------------

--- Dangling Images (untagged layers) ---
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
<none>              <none>              a1b2c3d4e5f6        2 hours ago         10MB
<none>              <none>              b2c3d4e5f6a1        5 hours ago         20MB
Pruning dangling images...
Removed image a1b2c3d4e5f6
Removed image b2c3d4e5f6a1
Dangling images pruned.

--- Exited Containers ---
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS               NAMES
c1d2e3f4g5h6        myimage:latest      "/bin/sh"           3 hours ago         Exited (0) 2 hours ago                          old_app_1
d2e3f4g5h6c1        another:v1          "/bin/bash"         6 hours ago         Exited (137) 5 hours ago                        temp_service_2
Removing exited containers...
Removed container c1d2e3f4g5h6
Removed container d2e3f4g5h6c1
Exited containers removed.

--- Unused Volumes ---
DRIVER              VOLUME NAME
local               my_old_data_volume
local               temp_log_volume
Pruning unused volumes...
Removed volume my_old_data_volume
Removed volume temp_log_volume
Unused volumes pruned.

---------------------------------------------
Cleanup complete.
```

### 4. Help Message

```bash
docker run --rm apocalypsai/dust-bunny-sweeper --help
```

## 🛠️ Development

To run tests:

```bash
# Navigate to the utility's root directory
cd nightly-dust-bunny-sweeper
bash tests/test_sweep.sh
```

The tests use a mocked `docker` command to ensure determinism and avoid actual Docker daemon interaction during testing.
