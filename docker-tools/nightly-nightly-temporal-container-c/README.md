# Nightly Temporal Container Chronometer

## Summary

The `nightly-temporal-container-chronometer` is a whimsical-yet-useful Dockerized utility designed to detect 'temporal anomalies' in your containerized infrastructure. It scans all running Docker containers and reports if any have recently started (indicating a potential unexpected restart or rapid deployment) or have been running for an excessively long period (suggesting a forgotten process or a container that has slipped through time).

Detecting temporal drift in your containerized reality is crucial for maintaining a stable and predictable environment, even in the apocalypse!

## Usage

### Building the Docker Image

Navigate to the `nightly-temporal-container-chronometer` directory and build the Docker image:

```bash
docker build -t nightly-temporal-container-chronometer .
```

### Running the Chronometer

To run the utility, you need to mount the Docker socket (`/var/run/docker.sock`) into the container. This allows the chronometer to inspect other running containers on the host.

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  nightly-temporal-container-chronometer
```

#### Configuration

You can customize the thresholds for what constitutes a 'recently started' or 'long-running' container using environment variables:

*   `RECENT_START_THRESHOLD_MINUTES`: The maximum number of minutes a container can be running to be considered 'recently started'. Default is `5` minutes.
*   `LONG_RUNNING_THRESHOLD_DAYS`: The minimum number of days a container must be running to be considered 'excessively long-running'. Default is `30` days.

**Example with custom thresholds:**

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e RECENT_START_THRESHOLD_MINUTES=10 \
  -e LONG_RUNNING_THRESHOLD_DAYS=60 \
  nightly-temporal-container-chronometer
```

### Interpreting the Output

The chronometer will output a report for each running container, categorizing it as:

*   `ANOMALY: Container '<name>' has recently started. Uptime: <duration>`: The container's uptime is below `RECENT_START_THRESHOLD_MINUTES`.
*   `ANOMALY: Container '<name>' is excessively long-running. Uptime: <duration>`: The container's uptime is above `LONG_RUNNING_THRESHOLD_DAYS`.
*   `NORMAL: Container '<name>' is stable. Uptime: <duration>`: The container's uptime falls within the defined normal range.

If the Docker daemon is not accessible (e.g., `/var/run/docker.sock` is not mounted correctly), an error message will be displayed.

## Automated Tests

The tests for the `monitor.sh` script are self-contained and use mocks to simulate Docker daemon responses, ensuring deterministic and offline execution.

To run the tests locally (requires `bash`):

```bash
bash tests/test_monitor.sh
```

This will execute a series of test cases, verifying the script's ability to correctly identify recently started, long-running, and normally operating containers, as well as handling cases where the Docker daemon is inaccessible.
