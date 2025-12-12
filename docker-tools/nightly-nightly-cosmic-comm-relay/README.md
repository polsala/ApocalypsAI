## Nightly Cosmic Comm Relay

This utility is a whimsical, containerized tool designed to simulate intergalactic communication. It takes a message, "transmits" it through a simulated cosmic void, and returns it with a chance of delightful corruption or unexpected additions. It's perfect for adding a touch of the absurd to your development environment or for testing message handling with unpredictable inputs.

### Features

*   **Containerized**: Runs in a Docker container for easy deployment and isolation.
*   **Whimsical Errors**: Introduces fun, thematic errors to messages.
*   **Configurable Transmission**: Adjust the probability of message corruption.

### Usage

1.  **Build the Docker image**: 
    ```bash
    docker build -t cosmic-comm-relay .
    ```

2.  **Run the container**: 
    ```bash
    docker run --rm -it cosmic-comm-relay "Hello, fellow sentient beings!"
    ```

    You can also specify a corruption probability (0.0 to 1.0):
    ```bash
    docker run --rm -it cosmic-comm-relay --corruption-chance 0.75 "Greetings from Sector 7G!"
    ```

### Development

The core logic is in `src/relay.py`. The `Dockerfile` sets up the environment and installs dependencies.

### Testing

Tests are located in `tests/` and can be run using `pytest` within the container or after installing dependencies locally.

```bash
docker run --rm -it cosmic-comm-relay pytest
```
