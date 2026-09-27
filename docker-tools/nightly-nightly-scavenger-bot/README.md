# Nightly Scavenger Bot

## Summary

The `nightly-scavenger-bot` is a whimsical, Docker-containerized utility that simulates a small autonomous bot venturing into the post-apocalyptic wasteland to scavenge for resources. Each run, the bot reports its findings, demonstrating a simple, isolated process within a Docker container.

This utility serves as a basic example of how to package a simple application into a Docker image and orchestrate it with `docker-compose`, making it useful for learning containerization concepts or as a template for more complex simulated environments.

## How it Works

The bot is a Python script (`scavenger_bot.py`) that randomly selects a resource (e.g., "rusty gears", "mutated berries") and a quantity, then prints a report to standard output. The `Dockerfile` packages this script into a lightweight Python environment. The `docker-compose.yml` defines the service, allowing you to easily build and run the bot.

## Setup and Usage

1.  **Prerequisites**: Ensure you have Docker and Docker Compose installed on your system.
    *   [Install Docker Engine](https://docs.docker.com/engine/install/)
    *   [Install Docker Compose](https://docs.docker.com/compose/install/)

2.  **Navigate to the utility directory**:
    ```bash
    cd nightly-scavenger-bot/src
    ```

3.  **Build the Docker image**:
    ```bash
    docker-compose build
    ```

4.  **Run the Scavenger Bot**:
    ```bash
    docker-compose run scavenger
    ```
    You will see output similar to:
    ```
    Scavenger Bot 734: Initiating scavenging protocol...
    Scavenger Bot 734 found 7 units of Ancient Data Chips!
    Scavenger Bot 734: Scavenging complete. Returning to base.
    ```
    Each run will yield a different resource and quantity.

## Automated Tests

To run the automated tests, navigate to the utility's root directory and execute the test script:

```bash
cd nightly-scavenger-bot
./tests/test_scavenger_bot.sh
```

The test script will build the Docker image, run the scavenger bot, capture its output, and verify that the output matches the expected pattern, ensuring the container runs correctly and produces a report.
