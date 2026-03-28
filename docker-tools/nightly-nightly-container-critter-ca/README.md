# Nightly Container Critter Caretaker

A whimsical-yet-useful containerized utility to monitor, refresh, and prune your Docker "pet" containers, ensuring a healthy and tidy environment. Think of it as a digital pet sitter for your long-running Docker services!

## Features

*   **Health Check**: Monitors specified "pet" containers and reports their status.
*   **Auto-Refresh (Optional)**: Automatically attempts to restart unwell (stopped/exited) pet containers.
*   **Environment Grooming (Optional)**: Prunes unused Docker images, volumes, and networks to reclaim disk space and keep your Docker environment tidy.

## Classifier

`docker-tools`

## How to Use

### 1. Build the Critter Caretaker Image

Navigate to the `nightly-container-critter-care` directory and build the Docker image:

```bash
docker build -t nightly-critter-caretaker .
```

### 2. Configure Your Pet Containers

The caretaker uses environment variables for configuration. You can set these directly when running the Docker container or, more conveniently, via a `docker-compose.yml` file.

*   `PET_CONTAINERS`: A comma-separated list of Docker container names that you consider your "pets" and want to monitor/refresh.
    *   Example: `PET_CONTAINERS="my-web-app,my-database,another-service"`
*   `PRUNE_ENABLED`: Set to `"true"` to enable automatic pruning of unused Docker objects. Set to `"false"` to disable.
    *   Default: `"true"`
*   `REFRESH_ENABLED`: Set to `"true"` to enable automatic restart attempts for unwell pet containers. Set to `"false"` to disable.
    *   Default: `"false"`

### 3. Run the Critter Caretaker

#### Option A: Using Docker Compose (Recommended for ease of use)

The `docker-compose.yml` in this directory provides a convenient way to run the caretaker.

1.  **Edit `docker-compose.yml`**: Adjust the `PET_CONTAINERS`, `PRUNE_ENABLED`, and `REFRESH_ENABLED` environment variables under the `critter_caretaker` service to match your needs.
    *   Alternatively, you can set these as shell environment variables before running `docker-compose`.
2.  **Run**:
    ```bash
    docker-compose up --build --force-recreate
    ```
    This will build the image (if not already built), create the service, run it, and then exit.

#### Option B: Direct Docker Run

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e PET_CONTAINERS="my-web-app,my-database" \
  -e PRUNE_ENABLED="true" \
  -e REFRESH_ENABLED="false" \
  nightly-critter-caretaker
```

**Note**: For continuous or scheduled caretaking, you would typically integrate this into a host-level cron job or a CI/CD pipeline that triggers the `docker-compose up` or `docker run` command periodically.

## Automated Tests

The utility includes a self-contained bash script for testing its core logic without requiring a live Docker daemon.

To run the tests:

```bash
bash tests/test_care_script.sh
```

This script mocks the `docker` commands to simulate various scenarios (healthy containers, unwell containers, pruning operations) and asserts the expected output and behavior of `src/care_script.sh`.
