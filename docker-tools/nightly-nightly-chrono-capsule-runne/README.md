# Nightly Chrono-Capsule Runner

## Summary

The `nightly-chrono-capsule-runner` is a whimsical-yet-useful utility designed to execute commands within Docker containers while introducing an optional 'temporal drift' to specified environment variables. This allows developers and testers to simulate future or past environments without altering the host system's clock, making it ideal for testing time-sensitive applications, reproducing date-related bugs, or observing system behavior under different temporal conditions.

## Features

*   **Containerized Execution**: Runs any command within a specified Docker image.
*   **Temporal Drift**: Applies a configurable time shift (e.g., `+1d`, `-2h`, `+30m`) to environment variables identified as time-sensitive.
*   **Isolated Testing**: Provides a clean, reproducible environment for each run.
*   **Simple Interface**: Easy to use via a command-line interface.

## How it Works

The utility takes a Docker image, a command, a list of environment variables, and an optional `drift_spec`. If `drift_spec` is provided, it parses the current time, applies the specified drift, and then updates any environment variables matching a predefined pattern (e.g., `CAPSULE_DATE`, `CAPSULE_TIMESTAMP`) with the new, drifted time before executing the `docker run` command.

## Usage

First, ensure you have Docker installed and running on your system.

### Building the Utility's Docker Image (Optional, for running the utility itself in a container)

```bash
docker build -t chrono-capsule-runner .
```

### Running the Utility

The utility is a Python script that orchestrates Docker commands. You can run it directly if Python and `docker` CLI are available, or run it via its own Docker container.

**Direct Execution (requires Python 3.x, `python-dateutil`, and Docker CLI):**

```bash
# Install dependencies
pip install python-dateutil

python src/chrono_capsule.py \
  --image ubuntu:latest \
  --command "bash -c 'echo \"Current date in capsule: $CAPSULE_DATE\"; echo \"Current timestamp in capsule: $CAPSULE_TIMESTAMP\"'" \
  --env CAPSULE_DATE=$(date +%Y-%m-%d) \
  --env CAPSULE_TIMESTAMP=$(date +%s) \
  --drift "+1d"

# Example with negative drift
python src/chrono_capsule.py \
  --image alpine:latest \
  --command "sh -c 'echo \"Time 2 hours ago: $CAPSULE_TIMESTAMP\"'" \
  --env CAPSULE_TIMESTAMP=$(date +%s) \
  --drift "-2h"

# Example without drift
python src/chrono_capsule.py \
  --image busybox \
  --command "echo \"Hello from the capsule!\"" \
```

**Running the Utility via its own Docker Container:**

This method is recommended for consistency and to avoid local dependency issues. You must mount the Docker socket so the utility container can interact with the Docker daemon.

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  chrono-capsule-runner \
  --image ubuntu:latest \
  --command "bash -c 'echo \"Current date in capsule: $CAPSULE_DATE\"; echo \"Current timestamp in capsule: $CAPSULE_TIMESTAMP\"'" \
  --env CAPSULE_DATE=$(date +%Y-%m-%d) \
  --env CAPSULE_TIMESTAMP=$(date +%s) \
  --drift "+1d"
```

**Arguments:**

*   `--image <DOCKER_IMAGE>`: The Docker image to use (e.g., `ubuntu:latest`).
*   `--command <COMMAND>`: The command to execute inside the container. **Remember to properly escape quotes for shell commands.**
*   `--env <KEY=VALUE>`: Environment variables to pass to the container. Can be specified multiple times. These are the variables that can be subject to temporal drift if their names match `CAPSULE_DATE` or `CAPSULE_TIMESTAMP`.
*   `--drift <DRIFT_SPEC>`: (Optional) The temporal drift to apply. Examples: `+1d` (1 day forward), `-2h` (2 hours backward), `+30m` (30 minutes forward). Supported units: `d` (days), `h` (hours), `m` (minutes), `s` (seconds).

## Environment Variable Drift Logic

The utility specifically looks for environment variables named `CAPSULE_DATE` and `CAPSULE_TIMESTAMP` for temporal drift. 

*   `CAPSULE_DATE`: Expected format `YYYY-MM-DD`. Will be shifted by the `drift_spec` and formatted back to `YYYY-MM-DD`.
*   `CAPSULE_TIMESTAMP`: Expected format is a Unix timestamp (seconds since epoch). Will be shifted by the `drift_spec` and formatted back to a Unix timestamp.

If other date/time formats are needed, the script `src/chrono_capsule.py` would need to be extended.

## Development

To develop or contribute, clone the repository and run tests as described below.
