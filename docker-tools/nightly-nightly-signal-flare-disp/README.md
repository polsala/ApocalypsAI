# Nightly Signal Flare Dispatcher

The Nightly Signal Flare Dispatcher is a whimsical, containerized web API designed to simulate the dispatch of critical (or not-so-critical) messages across the desolate wastes using an ancient, yet surprisingly effective, signal flare system. Send your urgent pleas, cryptic warnings, or even your dinner plans, and receive a simulated transmission report detailing the flare's journey.

## Features

*   **Whimsical Transmission Reports**: Get creative feedback on your signal's journey, including simulated signal strength and atmospheric interference.
*   **Containerized**: Easily deployable with Docker, ensuring consistent operation even when the world is crumbling.
*   **Simple API**: A single endpoint for all your flare-dispatching needs.

## How to Run (with Docker)

1.  **Build the Docker image**: From the root of this utility's directory (where `Dockerfile` is located):
    ```bash
    docker build -t signal-flare-dispatcher .
    ```

2.  **Run the container**: This will map port `8080` on your host to the container's port `8080`.
    ```bash
    docker run -p 8080:8080 signal-flare-dispatcher
    ```
    The API will be accessible at `http://localhost:8080`.

3.  **Alternatively, use Docker Compose for quick setup**: From the root of this utility's directory:
    ```bash
    docker-compose up --build
    ```
    This will build the image and start the container, mapping port 8080.

## API Usage

### `POST /dispatch_flare`

Dispatches a signal flare with your message to a specified sector.

**Request Body (JSON)**:

```json
{
    "message": "The raiders are approaching from the east! Bring snacks!",
    "sector": "Sector Gamma-7"
}
```

**Example `curl` command**:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"message": "Need more irradiated squirrel jerky!", "sector": "Old Town Ruins"}' \
     http://localhost:8080/dispatch_flare
```

**Response (JSON)**:

```json
{
    "status": "Flare Dispatched",
    "transmission_id": "FLARE-20240729-ABCD1234",
    "target_sector": "Old Town Ruins",
    "message_sent": "Need more irradiated squirrel jerky!",
    "report": "A shimmering crimson flare pierced the twilight, carrying your plea. Atmospheric interference was moderate, but the message appears to have reached the general vicinity. Expect a response in 1-3 solar cycles, or when the wind changes.",
    "signal_strength": "Moderate",
    "estimated_arrival_time_s": 120
}
```

### Error Responses

*   **400 Bad Request**: If `message` or `sector` are missing from the request body.

    ```json
    {
        "error": "Missing 'message' or 'sector' in request body."
    }
    ```

## Development & Testing

### Prerequisites

*   Python 3.8+
*   pip
*   Docker (for containerization)

### Local Development

1.  **Install dependencies**: From the `src/` directory:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Flask app**: From the `src/` directory:
    ```bash
    python app.py
    ```
    The app will run on `http://127.0.0.1:8080`.

### Running Tests

1.  **Install pytest**: From the utility's root directory:
    ```bash
    pip install pytest
    ```

2.  **Run tests**: From the utility's root directory:
    ```bash
    pytest tests/
    ```
