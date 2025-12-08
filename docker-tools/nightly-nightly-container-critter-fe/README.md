# Nightly Container Critter Feeder

## Whimsical Purpose
In the post-apocalyptic digital wasteland, even our most resilient containerized applications can get a bit peckish or simply wander off into the void. The `nightly-container-critter-feeder` is your dedicated digital pet-sitter, diligently monitoring your Docker 'critters' and ensuring they are well-fed (restarted) if they become unwell (exited, stopped, or unhealthy). Keep your container garden thriving, one restart at a time!

## Classifier: `docker-tools`
This utility is designed to run as a Docker container, interacting with the Docker daemon to manage other containers.

## How it Works
The Critter Feeder runs in a Docker container and requires access to the host's Docker socket. It periodically inspects other running containers. If it finds a container that has exited, stopped, or is reported as unhealthy (via Docker's health check), it attempts to restart it. You can configure it to monitor specific containers or automatically discover all non-feeder containers.

## Setup and Usage

1.  **Build the Docker Image:**
    ```bash
    docker build -t nightly-container-critter-feeder .
    ```

2.  **Run the Critter Feeder:**
    The feeder needs access to the Docker daemon. Mount the Docker socket to allow it to interact with other containers.

    ```bash
    docker run -d \
      --name critter-feeder \
      -v /var/run/docker.sock:/var/run/docker.sock \
      nightly-container-critter-feeder
    ```

3.  **Configuration (Environment Variables):**
    *   `FEED_INTERVAL`: The interval (in seconds) between monitoring rounds. Default is `10` seconds.
        Example: `docker run ... -e FEED_INTERVAL=30 ...`
    *   `CRITTER_NAMES`: A space-separated list of container names or IDs to explicitly monitor. If not set, the feeder will automatically discover and monitor all containers except itself.
        Example: `docker run ... -e "CRITTER_NAMES=my-web-app my-db-service" ...`

## Example Scenario
Imagine you have a `my-web-app` container that occasionally crashes. With the Critter Feeder running, it will detect the `exited` state of `my-web-app` and automatically restart it, keeping your whimsical web service alive.

## Development and Testing

### Running Tests
To run the automated tests, execute the `tests/test_feeder.sh` script. This script uses mocks to simulate Docker commands, ensuring deterministic and offline testing.

```bash
./tests/test_feeder.sh
```

### Test Rationale
The tests mock the `docker` command to simulate various container states (`running`, `exited`, `unhealthy`) and `docker restart` outcomes (success/failure). This allows for comprehensive testing of the `feeder.sh` script's logic without requiring a live Docker daemon or actual containers to be manipulated.
