# Nightly Temporal Message Bottle

## Summary

The `nightly-temporal-message-bottle` is a whimsical-yet-useful containerized Flask web service that allows you to "bottle" messages with a specific future (or past) timestamp. When queried, it reveals messages whose bottled time has arrived (or passed), acting as a digital message in a bottle sent through the temporal currents.

Ever wanted to send a note to your future self? Or leave a historical marker for those who might uncork it later? This utility provides a simple API for just that.

## How it Works

The service exposes two primary endpoints:

1.  `POST /bottle`: Stores a message along with a specified UTC timestamp.
2.  `GET /uncork`: Retrieves all messages whose specified timestamp is less than or equal to the current UTC time.

Messages are stored in-memory within the Flask application. For persistence across container restarts, you would need to integrate a database (e.g., SQLite, PostgreSQL), but for this standalone utility, in-memory storage keeps it light and easy to demonstrate.

## Setup and Usage

This utility is designed to run using Docker and Docker Compose.

### Prerequisites

*   Docker installed on your system.
*   Docker Compose installed on your system.

### 1. Build and Run the Service

Navigate to the `nightly-temporal-message-bottle` directory and use Docker Compose to build and start the service:

```bash
docker-compose up --build -d
```

This command will:
*   Build the Docker image for the `temporal-bottle` service.
*   Start the service in detached mode (`-d`).
*   Map port `5000` of your host to port `5000` inside the container.

### 2. Bottle a Message

Send a POST request to the `/bottle` endpoint with your message and a UTC timestamp in ISO 8601 format (e.g., `YYYY-MM-DDTHH:MM:SSZ`).

**Example: Bottle a message for 1 minute from now**

First, get the current UTC time and add a minute:

```bash
FUTURE_TIME=$(date -u -v+1M "+%Y-%m-%dT%H:%M:%SZ")
curl -X POST -H "Content-Type: application/json" \
     -d '{"message": "Remember to feed the cat!", "timestamp": "'$FUTURE_TIME'"}' \
     http://localhost:5000/bottle
```

**Example: Bottle a message for a specific past date**

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"message": "The Great Coffee Shortage of 2023 was tough.", "timestamp": "2023-10-26T10:00:00Z"}' \
     http://localhost:5000/bottle
```

### 3. Uncork Messages

Send a GET request to the `/uncork` endpoint to retrieve messages whose bottled time has arrived or passed.

```bash
curl http://localhost:5000/uncork
```

Initially, if you bottled a future message, you might see an empty list. Wait until the `FUTURE_TIME` has passed, then query again.

**Example Output:**

```json
{
  "messages": [
    {
      "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "message": "The Great Coffee Shortage of 2023 was tough.",
      "timestamp": "2023-10-26T10:00:00Z"
    },
    {
      "id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
      "message": "Remember to feed the cat!",
      "timestamp": "2024-01-01T12:01:00Z"
    }
  ]
}
```

### 4. Stop and Remove the Service

When you're done, you can stop and remove the container and its network:

```bash
docker-compose down
```

## Development and Testing

### Running Tests

Tests are self-contained and can be run using the provided `run_tests.sh` script. This script builds the Docker image and executes the Python unit tests within a temporary container.

```bash
./tests/run_tests.sh
```

This will output the results of the unit tests. All tests are deterministic and offline, using mocks for time-sensitive operations.

### Project Structure

```
. # nightly-temporal-message-bottle
├── README.md
├── src/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
└── tests/
    ├── test_app.py
    └── run_tests.sh
```
