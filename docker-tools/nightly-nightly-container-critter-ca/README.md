# Nightly Container Critter Caretaker

## Summary
A Docker-based utility that provides whimsical 'care instructions' and health checks for your running Docker containers, treating them like digital pets.

## How it Works
This utility runs as a Docker container, mounting the host's Docker socket to interact with the Docker daemon. It lists all containers (running, stopped, unhealthy, etc.) and, for each, determines a 'whimsical status' and generates a corresponding 'care tip' along with a suggested Docker command to address its needs.

## Usage

1.  **Ensure Docker is running** on your host machine.
2.  **Navigate to the utility's directory**:
    ```bash
    cd docker-tools/nightly-container-critter-caretaker
    ```
3.  **Run the caretaker**: The `docker-compose.yml` is configured to build the image and run the script once, then exit.
    ```bash
    docker-compose up --build --force-recreate
    ```
    This command will:
    *   Build the Docker image (if not already built or if changes are detected).
    *   Create and start the `caretaker` service.
    *   Execute the `critter_caretaker.py` script inside the container.
    *   Print the care report to your console.
    *   Stop and remove the `caretaker` container after execution.

### Example Output
```
--- Container Critter Care Report ---

Critter: my-healthy-app
  Status: Purring happily
  Care Tip: Your my-healthy-app critter is purring happily! Keep an eye on its joyful antics.
  Suggested Action: docker logs my-healthy-app

Critter: database-critter
  Status: Looking a bit green
  Care Tip: Oh dear, your database-critter critter is looking a bit green. It might need a vet visit!
  Suggested Action: docker inspect database-critter --format '{{json .State.Health}}'

Critter: old-service-critter
  Status: Wandered off
  Care Tip: Your old-service-critter critter has wandered off. Time to coax it back into action!
  Suggested Action: docker start old-service-critter

--- End of Report ---
```

## Development and Testing

To develop or test the Python script independently of Docker:

1.  **Install dependencies**:
    ```bash
    pip install -r src/requirements.txt
    ```
2.  **Run tests**:
    ```bash
    python -m unittest tests/test_critter_caretaker.py
    ```
    The tests use `unittest.mock` to simulate Docker client interactions, ensuring they are deterministic and do not require a running Docker daemon.
