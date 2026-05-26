# Nightly Chrono-Compass Oracle

## Overview

The `nightly-chrono-compass-oracle` is a whimsical, containerized microservice designed to provide the ApocalypsAI community with a daily 'temporal alignment' or 'focus point'. Each day, it generates a unique, deterministically random message offering guidance, perspective, or a challenge, drawing from the vast, shifting currents of time and existence.

This utility is built using Python and Flask, encapsulated within a Docker container for easy deployment and isolation.

## Features

- **Daily Whimsical Guidance**: Fetches a new, inspiring, or thought-provoking 'temporal alignment' message each day.
- **Deterministic Output**: The alignment message for any given date is consistent, ensuring that everyone receives the same guidance for that specific day.
- **Containerized**: Easily deployable as a Docker container, making it simple to integrate into various environments.
- **Simple API**: Exposes a single HTTP endpoint to retrieve the daily alignment.

## How to Use

### Prerequisites

- Docker installed on your system.

### 1. Build the Docker Image

Navigate to the `nightly-chrono-compass-oracle` directory and build the Docker image:

```bash
docker build -t chrono-compass-oracle .
```

### 2. Run the Docker Container

Run the container, mapping port `5000` from the container to a port on your host (e.g., `8080`):

```bash
docker run -p 8080:5000 --name chrono-oracle -d chrono-compass-oracle
```

- `-p 8080:5000`: Maps host port 8080 to container port 5000.
- `--name chrono-oracle`: Assigns a memorable name to your container.
- `-d`: Runs the container in detached mode (in the background).

### 3. Access the Daily Alignment

Once the container is running, you can access the daily temporal alignment by making an HTTP GET request to the `/align` endpoint. Open your web browser or use `curl`:

```bash
curl http://localhost:8080/align
```

You will receive a JSON response similar to this:

```json
{
  "alignment": "Today's Temporal Alignment: Align with the Resilience amidst the Crystalized Memories of the Temporal Flux. Let your path be guided by the unseen currents.",
  "date": "2023-10-27",
  "oracle_name": "Chrono-Compass Oracle"
}
```

### Stopping the Container

To stop the running container:

```bash
docker stop chrono-oracle
```

To remove the container:

```bash
docker rm chrono-oracle
```

## Development and Testing

### Running Tests

Tests are included and can be run inside a dedicated test Docker container. From the `nightly-chrono-compass-oracle` directory:

```bash
bash tests/run_tests.sh
```

This script will build a test-specific Docker image and execute the Python unit tests within it, ensuring a consistent testing environment.

### Local Development

If you wish to run the Flask application locally without Docker (for development):

1. Install dependencies:
   ```bash
   pip install Flask
   ```
2. Run the application:
   ```bash
   python src/app.py
   ```
   The server will typically run on `http://127.0.0.1:5000/`.
