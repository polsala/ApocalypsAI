# Nightly Chronosync Compass

A whimsical, containerized web service designed to help communities in a post-apocalyptic world maintain a semblance of synchronized time. It offers a simple API to retrieve a "community-agreed" time, a "temporal stability reading," and cryptic "whispers from the void" to ponder the nature of time itself.

## Features

*   **Community Time API**: Get the current UTC time, presented as the "Community Consensus Time."
*   **Temporal Stability Reading**: A randomized, whimsical indicator of temporal stability.
*   **Whispers from the Void**: Cryptic, time-related messages to inspire or confuse.
*   **Time Reporting**: An endpoint to allow local systems to report their observed time, aiding in potential future consensus algorithms (currently just logs the input).

## How to Use

### Prerequisites

*   Docker installed and running.
*   Docker Compose (optional, but recommended for easy setup).

### Running with Docker Compose (Recommended)

1.  Navigate to the `nightly-chronosync-compass` directory.
2.  Run:
    ```bash
    docker-compose up --build -d
    ```
3.  The service will be available at `http://localhost:5000`.

### Running with Docker CLI

1.  Navigate to the `nightly-chronosync-compass` directory.
2.  Build the Docker image:
    ```bash
    docker build -t chronosync-compass .
    ```
3.  Run the container:
    ```bash
    docker run -p 5000:5000 --name chronosync-compass-instance -d chronosync-compass
    ```
4.  The service will be available at `http://localhost:5000`.

### API Endpoints

*   **GET `/time`**:
    Returns the current "Community Consensus Time" and a "Temporal Stability Reading."
    Example Response:
    ```json
    {
      "community_consensus_time_utc": "2023-10-27T10:30:00.123456Z",
      "temporal_stability_reading": 0.87,
      "stability_status": "Stable as a pre-collapse clockwork"
    }
    ```

*   **GET `/whisper`**:
    Returns a random "Whisper from the Void."
    Example Response:
    ```json
    {
      "whisper": "The past is a ripple, the future a wave. Ride the now."
    }
    ```

*   **POST `/report_time`**:
    Allows a client to report its local time observation.
    Request Body (JSON):
    ```json
    {
      "local_time": "2023-10-27T10:30:05Z",
      "source": "Outpost Alpha-7"
    }
    ```
    Example Response:
    ```json
    {
      "status": "Time observation logged.",
      "received_time": "2023-10-27T10:30:05Z",
      "source": "Outpost Alpha-7"
    }
    ```

## Development & Testing

### Local Development

1.  Install Python dependencies: `pip install Flask`
2.  Run the app: `python src/app.py`
3.  Access at `http://127.0.0.1:5000`.

### Running Tests

1.  Install Python dependencies: `pip install Flask pytest`
2.  Run tests from the root directory: `pytest tests/`
