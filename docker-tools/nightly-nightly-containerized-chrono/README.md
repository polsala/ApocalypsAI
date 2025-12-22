# Nightly Containerized Chronometer

## Summary
This utility provides a whimsical-yet-useful Dockerized web service that displays countdowns to or count-ups from configurable apocalyptic events. It's perfect for keeping the community informed (and slightly on edge) about the next big temporal anomaly or celebrating past survival milestones.

## How it Works
The Chronometer is a simple Python Flask application packaged within a Docker container. It reads a JSON string of apocalyptic events from an environment variable, calculates the time difference between the current moment (UTC) and each event's specified datetime (assumed UTC if no timezone is provided), and renders these statuses on a basic web page.

- **Countdown**: If an event is in the future, it shows "Countdown to [Event Name]: X days, Y hours, Z minutes, S seconds".
- **Count-up**: If an event is in the past, it shows "Time since [Event Name]: X days, Y hours, Z minutes, S seconds".

## Usage

### 1. Build the Docker Image
Navigate to the `nightly-containerized-chronometer` directory and build the Docker image:

```bash
docker build -t apocalypse-chronometer .
```

### 2. Run the Docker Container
You can run the container, exposing port 5000, and providing your apocalyptic events via the `APOCALYPSE_EVENTS_JSON` environment variable.

**Example with events:**

```bash
docker run -p 5000:5000 \
  -e "APOCALYPSE_EVENTS_JSON=[{\"name\": \"The Great Glitch\", \"datetime\": \"2025-01-01T00:00:00Z\"}, {\"name\": \"The First Whisper\", \"datetime\": \"2023-06-15T14:30:00Z\"}]" \
  apocalypse-chronometer
```

**Example without events (default):**

```bash
docker run -p 5000:5000 apocalypse-chronometer
```

### 3. Access the Chronometer
Open your web browser and navigate to `http://localhost:5000`.

## Configuration
The utility is configured via the `APOCALYPSE_EVENTS_JSON` environment variable. This variable must contain a JSON array of objects, where each object represents an apocalyptic event.

Each event object must have:
- `name`: A string representing the name of the event (e.g., "The Great Glitch").
- `datetime`: A string in ISO 8601 format (e.g., "YYYY-MM-DDTHH:MM:SSZ" for UTC, or "YYYY-MM-DDTHH:MM:SS" which will be treated as UTC). Ensure consistency for accurate calculations.

**Example `APOCALYPSE_EVENTS_JSON` value:**

```json
[
  {
    "name": "The Great Glitch",
    "datetime": "2025-01-01T00:00:00Z"
  },
  {
    "name": "The First Whisper",
    "datetime": "2023-06-15T14:30:00Z"
  },
  {
    "name": "Temporal Rift Stabilization",
    "datetime": "2024-07-25T08:00:00"
  }
]
```

## Development and Testing

### Prerequisites
- Python 3.9+
- `pip`
- `docker`

### Local Setup
1. Install dependencies:
   ```bash
   pip install -r src/requirements.txt
   ```
2. Run the Flask app directly (for development):
   ```bash
   python src/app.py
   ```

### Running Tests
Tests are located in `tests/test_app.py`. They use `unittest` and `unittest.mock` to ensure deterministic results by patching `datetime.datetime.now()`.

```bash
python -m unittest tests/test_app.py
```
