# Nightly Resource Scavenger Bot

## Summary
`nightly-resource-scavenger-bot` is a whimsical-yet-useful containerized utility designed to simulate the act of scavenging for vital post-apocalyptic resources. It periodically 'searches' a predefined list of fantastical resources and reports its findings, or lack thereof, to the console. This tool serves as an excellent example for demonstrating scheduled, containerized processes and basic service orchestration using Docker.

## Whimsical Purpose
In the desolate future, every scrap counts! This bot helps keep spirits high by reporting on the 'discoveries' made in the vast, unknown territories. Whether it's "Glimmering Gears" or "Temporal Taffy", every find is a small victory.

## Technical Utility
Beyond its whimsical facade, this utility showcases:
- **Docker Containerization**: Packaging a Python script into a lightweight, portable container.
- **Scheduled Tasks**: Demonstrating how a simple script can be run within a container, ready for orchestration (e.g., via `cron` inside the container or external schedulers).
- **Mock Data Interaction**: Reading from a static 'resource manifest' file, which can be easily extended to interact with real APIs or databases.
- **Self-contained Deployment**: Easy to build and run on any system with Docker installed.

## How It Works
The bot is a Python script (`scavenger_bot.py`) that reads a list of potential resources from `resources.txt`. Upon execution, it randomly selects a few (or none) of these resources and prints a report to standard output. The `entrypoint.sh` script simply executes the Python bot.

## Usage

### 1. Build the Docker Image
Navigate to the utility's root directory (where `Dockerfile` is located) and build the image:

```bash
docker build -t nightly-resource-scavenger-bot .
```

### 2. Run the Container
Execute the bot in a new container. Each run will simulate a scavenging mission:

```bash
docker run --rm nightly-resource-scavenger-bot
```

**Example Output (may vary due to randomness):**

```
Scavenger Bot reports: Found 2 valuable items!
- Quantum Quinoa
- Echoing Embers
```

Or, if nothing is found:

```
Scavenger Bot reports: A thorough search yielded nothing but echoes of the past.
```

### 3. Running Periodically (Advanced)
To run the bot periodically, you could integrate it with a system's cron scheduler or a container orchestration tool like Kubernetes or Docker Compose. For example, to run it every hour on a Linux system:

```bash
(crontab -l; echo "0 * * * * docker run --rm nightly-resource-scavenger-bot") | crontab -
```

## Testing
To ensure the bot is functioning correctly, run the provided test script:

```bash
bash tests/test_scavenger_bot.sh
```

This script builds the Docker image, runs the container, and verifies that the output matches expected patterns, including the report header and the presence of known resources if any are reported as found.
