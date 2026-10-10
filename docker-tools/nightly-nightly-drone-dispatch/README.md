# Nightly Drone Delivery Dispatcher

A whimsical, containerized utility that simulates dispatching a drone to deliver vital (or not-so-vital) cargo across a perilous post-apocalyptic landscape. Each dispatch generates a report detailing the destination, cargo, estimated travel time, and the outcome – be it a successful delivery, a delay due to unforeseen anomalies, or a complete loss of drone and precious goods.

## Features

- **Whimsical Destinations & Cargo**: Delivers to places like "The Glowing Grotto" carrying "a vintage pre-fall comic book."
- **Anomaly Simulation**: Random chances of "temporal distortions," "irradiated ravens," or "EMP bursts" affecting delivery.
- **Detailed Reports**: Provides a timestamped report for each dispatch, including outcome and any reasons for delay or loss.
- **Containerized**: Runs entirely within a Docker container, ensuring a consistent environment and easy deployment.

## Classifier

`docker-tools`

## How to Use

### Prerequisites

- Docker installed on your system.

### 1. Build the Docker Image

Navigate to the `nightly-drone-dispatch` directory and build the Docker image:

```bash
docker build -t nightly-drone-dispatch .
```

### 2. Run a Drone Dispatch

Once the image is built, you can run a single drone dispatch simulation:

```bash
docker run nightly-drone-dispatch
```

Each run will output a new, randomized drone dispatch report to your console.

### Example Output

```
--- Drone Dispatch Report ---
Dispatch Time: 2023-10-27 10:30:00 UTC
Destination: Whispering Wastes Outpost
Cargo: a map to a rumored clean water source
Outcome: Delayed
Estimated Travel Time (including delay): 210 minutes
Delay Reason: Encountered unexpected radiation storm.
Status: Cargo is en route, but running late.
-----------------------------
```

## Development & Testing

### Running Tests

To run the unit tests for the Python script, you'll need Python and `unittest`.

1. Ensure you are in the `nightly-drone-dispatch` directory.
2. Run the tests using `python -m unittest`:

```bash
python -m unittest tests/test_drone_dispatcher.py
```

### Project Structure

```
.
├── README.md
├── Dockerfile
├── src/
│   └── drone_dispatcher.py
└── tests/
    └── test_drone_dispatcher.py
```
