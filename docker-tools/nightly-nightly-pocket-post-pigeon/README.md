# Nightly Pocket Post-Pigeon

A whimsical-yet-useful containerized utility for sending ephemeral, self-destructing messages across the ApocalypsAI community. Think of it as a digital carrier pigeon that delivers your message and then vanishes into the void, ensuring privacy and reducing clutter.

## How It Works

The Pocket Post-Pigeon runs as a lightweight Docker container, hosting a simple Flask web API. Messages are stored in-memory with a specified Time-To-Live (TTL). Once a message is retrieved by its intended recipient, or if its TTL expires, it is automatically purged from the system. This ensures that messages are truly ephemeral and only seen by their intended audience, mimicking a one-time-read 'pigeon post' system.

## Features

*   **Ephemeral Messaging**: Messages self-destruct after retrieval or TTL expiration.
*   **Containerized**: Easy deployment and isolation using Docker.
*   **Simple API**: Straightforward HTTP endpoints for sending and receiving messages.
*   **Whimsical**: Embrace the spirit of post-apocalyptic communication with digital carrier pigeons.

## Setup and Usage

### 1. Build the Docker Image

Navigate to the `nightly-pocket-post-pigeon` directory and build the Docker image:

```bash
docker build -t pocket-post-pigeon .
```

### 2. Run the Container

Run the container, mapping port 5000 (inside the container) to a port on your host (e.g., 8080):

```bash
docker run -d -p 8080:5000 --name post-pigeon-service pocket-post-pigeon
```

The service will now be accessible at `http://localhost:8080`.

### 3. API Endpoints

#### A. Send a Message (POST /send)

Send a message to a recipient with a specified Time-To-Live (in seconds).

*   **Method**: `POST`
*   **URL**: `/send`
*   **Content-Type**: `application/json`
*   **Body**: 
    ```json
    {
        "sender": "YourName",
        "recipient": "TargetUser",
        "message": "Hello from the wasteland!",
        "ttl_seconds": 600  // Message will expire in 10 minutes if not read
    }
    ```

**Example using `curl`:**

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"sender": "ScavengerBot", "recipient": "BaseAlpha", "message": "Found rare components near Sector 7!", "ttl_seconds": 300}' \
     http://localhost:8080/send
```

#### B. Receive Messages (GET /receive/<recipient>)

Retrieve all unread and unexpired messages for a specific recipient. Messages are deleted upon successful retrieval.

*   **Method**: `GET`
*   **URL**: `/receive/<recipient>`

**Example using `curl`:**

```bash
curl http://localhost:8080/receive/BaseAlpha
```

**Example Response (if messages exist):**

```json
[
    {
        "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "sender": "ScavengerBot",
        "message": "Found rare components near Sector 7!",
        "received_at": "2023-10-27T10:30:00.123456"
    }
]
```

If no messages are found, an empty JSON array `[]` is returned.

## Development and Testing

To run tests, ensure `pytest` is installed (`pip install pytest`).

```bash
pytest tests/
```

## License

This project is licensed under the MIT License.
