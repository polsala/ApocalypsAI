# Nightly Container Aura Reader

## Overview

The `nightly-container-aura-reader` is a whimsical yet practical utility designed to give your Docker containers a personality! It runs as its own container, connects to your Docker daemon, and inspects the status and health of all other running containers. Based on these observations, it assigns a unique "aura" to each container, providing a quick, human-readable, and fun overview of your containerized ecosystem's mood.

## Auras Explained

*   **Vibrant**: Running smoothly and reported as healthy.
*   **Anxious**: Running, but its health check indicates issues.
*   **Pondering**: Currently starting up, restarting, or in a 'created' state.
*   **Serene**: Exited gracefully (status code 0).
*   **Grumpy**: Exited with an error or is in a 'dead' state.
*   **Mysterious**: Any other unexpected or unknown state.

## Usage

1.  **Ensure Docker is running**: This utility needs access to the Docker daemon.
2.  **Run the container**: Execute the following command. The `-v /var/run/docker.sock:/var/run/docker.sock` part is crucial as it allows the `aura-reader` container to communicate with your Docker daemon.

    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-container-aura-reader
    ```

    (Note: Replace `nightly-container-aura-reader` with the actual image name if you build it locally, e.g., `my-aura-reader:latest`)

3.  **Interpret the output**: The utility will print a list of your containers and their assigned auras.

    ```
    Container 'my-web-app' is Vibrant.
    Container 'database' is Anxious.
    Container 'old-service' is Serene.
    ```

## Development & Building

To build the Docker image locally:

```bash
docker build -t nightly-container-aura-reader .
```

Then run as described above.

## Automated Tests

The `test_aura_reader.py` script contains unit tests that mock the Docker client interactions to ensure aura assignments are correct under various simulated container states.
