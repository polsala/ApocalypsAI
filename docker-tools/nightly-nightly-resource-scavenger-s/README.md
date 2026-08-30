# nightly-resource-scavenger-sim

A whimsical-yet-useful containerized utility that simulates a resource-scavenging bot in a post-apocalyptic world. Configure your scavenging zones and simulation duration, and let the bot report on its findings! This tool is great for demonstrating Docker containerization, environment variable usage, and basic simulation logic.

## Usage

1.  **Build the Docker image:**
    ```bash
    docker build -t scavenger-sim .
    ```

2.  **Run the simulation:**
    You can configure the simulation using environment variables.

    *   `SIMULATION_DAYS`: Number of days the bot will scavenge (default: 7).
    *   `ZONES`: Comma-separated list of scavenging zones (default: "Ruined City,Abandoned Factory,Overgrown Forest").
    *   `RESOURCES_PER_ZONE`: Maximum resources a bot can find per zone per day (default: 5).
    *   `RESOURCE_TYPES`: Comma-separated list of possible resource types (default: "Water,Food,Scrap Metal,Medical Supplies,Fuel").

    **Example 1: Default simulation**
    ```bash
    docker run scavenger-sim
    ```

    **Example 2: Custom simulation**
    ```bash
    docker run \
      -e SIMULATION_DAYS=14 \
      -e ZONES="Old Mall,Collapsed Bridge" \
      -e RESOURCES_PER_ZONE=10 \
      -e RESOURCE_TYPES="Rare Parts,Ancient Tech,Survival Manuals" \
      scavenger-sim
    ```

3.  **Using `docker-compose` (recommended for easier configuration):**
    Create a `docker-compose.yml` file (example provided in `docker-compose.yml`):
    ```yaml
    version: '3.8'
    services:
      scavenger-bot:
        build: .
        environment:
          SIMULATION_DAYS: 10
          ZONES: "Deserted Outpost,Sunken Ship,Forgotten Bunker"
          RESOURCES_PER_ZONE: 7
          RESOURCE_TYPES: "Canned Goods,Ammunition,Tools,Maps"
        # Optional: if you want to see the output immediately
        # tty: true 
        # stdin_open: true
    ```
    Then run:
    ```bash
    docker-compose up --build
    ```

## Development

The core logic is a Python script (`src/scavenger_sim.py`).
Tests are located in `tests/test_scavenger_sim.py`.

To run tests locally (without Docker):
```bash
pip install -r src/requirements.txt
python -m pytest tests/test_scavenger_sim.py
```

## How it works

The Python script simulates daily scavenging. For each day and each configured zone, it randomly determines if resources are found and how many, then assigns a random resource type. The final output is a summary of all collected resources.
