# Nightly Scavenger Drone Simulator (`nightly-scavenger-drone-sim`)

A whimsical-yet-useful Dockerized utility that simulates a scavenger drone reporting on discovered resources and anomalies in a post-apocalyptic wasteland. This tool can be used for:

-   **Testing Monitoring Systems**: Generate a stream of simulated resource reports and anomalies to test how your monitoring or log aggregation systems handle varied data.
-   **Demonstrating Docker**: A simple, self-contained example of packaging a Python script into a Docker image.
-   **Whimsical Background Process**: Run it as a cron job on a server to add a touch of post-apocalyptic flavor to your system logs.

## Classifier

`docker-tools`

## How it Works

The utility runs a Python script inside a Docker container. The script randomly generates a JSON report containing:
-   A timestamp and a drone ID (configurable via `DRONE_ID` environment variable).
-   A simulated location (sector and grid).
-   A list of "findings," which can include:
    -   Discovered resources (e.g., "scrap metal", "purified water") with quantities.
    -   Detected anomalies (e.g., "temporal distortion", "unidentified signal source").
    -   A "no significant findings" status if nothing else is found.

The report is printed to standard output (stdout) as a JSON string.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-scavenger-drone-sim` directory and build the Docker image:

```bash
docker build -t scavenger-drone-sim .
```

### 2. Run the Simulator

You can run the simulator to generate a single report:

```bash
docker run scavenger-drone-sim
```

Example output:

```json
{
  "timestamp": "2023-10-27T10:30:00+00:00",
  "drone_id": "DRONE-ALPHA-7",
  "location": {
    "sector": "Alpha",
    "grid": "42-88"
  },
  "findings": [
    {
      "type": "resource",
      "item": "scrap metal",
      "quantity": 5
    },
    {
      "type": "anomaly",
      "description": "temporal distortion detected"
    }
  ]
}
```

### 3. Customize Drone ID

Set the `DRONE_ID` environment variable to give your drone a unique identifier:

```bash
docker run -e DRONE_ID="DRONE-BETA-9000" scavenger-drone-sim
```

### 4. Continuous Reporting (Example)

To simulate continuous reporting, you could run it in a loop (e.g., every 5 seconds):

```bash
while true; do docker run scavenger-drone-sim; sleep 5; done
```

Or, for a more robust solution, integrate it into a `cron` job or a container orchestration platform.

## Development and Testing

### Prerequisites

-   Python 3.9+
-   Docker

### Running Tests

The tests ensure that the report generation logic works as expected under various conditions, using mocks to make random outcomes deterministic.

```bash
# Ensure you are in the nightly-scavenger-drone-sim directory
python -m unittest tests/test_drone_sim.py
```

## Contributing

Feel free to enhance the drone's findings, add more resource types, or introduce new anomaly categories!
