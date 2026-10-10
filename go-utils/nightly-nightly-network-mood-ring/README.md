# Nightly Network Mood Ring

## Overview

The `nightly-network-mood-ring` is a whimsical yet useful Go-based service designed to track the 'emotional resonance' of your distributed systems. Instead of traditional health checks, components report their 'mood' (e.g., Serene, Anxious, Chaotic), and this central service aggregates them, providing a snapshot of the network's collective emotional state.

It's perfect for gaining a high-level, human-readable understanding of system health, or simply adding a touch of personality to your monitoring dashboards.

## Features

*   **Mood Reporting**: Components send their current mood via a simple HTTP POST request.
*   **Aggregated Status**: Query the service to get a list of all reported component moods.
*   **Ephemeral States**: Moods are updated, reflecting the latest state of each component.
*   **Go Concurrency**: Built with Go's powerful concurrency model for efficient handling of multiple reports.

## Usage

### 1. Run the Mood Ring Server

Navigate to the `src` directory and run the Go application:

```bash
cd src
go run main.go
```

By default, the server will listen on `http://localhost:8080`. You can change the port by setting the `PORT` environment variable:

```bash
PORT=9000 go run main.go
```

### 2. Report a Component's Mood

Send a POST request to the `/report` endpoint with a JSON payload specifying the `source` and `mood`.

**Example (using `curl`):**

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"source": "frontend-service-alpha", "mood": "Optimistic"}' \
     http://localhost:8080/report

curl -X POST -H "Content-Type: application/json" \
     -d '{"source": "database-replica-01", "mood": "Serene"}' \
     http://localhost:8080/report

curl -X POST -H "Content-Type: application/json" \
     -d '{"source": "auth-microservice", "mood": "Anxious"}' \
     http://localhost:8080/report
```

**Available Whimsical Moods (suggestions, but any string is accepted):**

*   `Serene`
*   `Optimistic`
*   `Anxious`
*   `Chaotic`
*   `Melancholy`
*   `Vigilant`
*   `Overwhelmed`
*   `Curious`
*   `Content`

### 3. Check the Network's Overall Mood

Send a GET request to the `/status` endpoint:

**Example (using `curl`):**

```bash
curl http://localhost:8080/status
```

**Example Response:**

```json
{
  "component_moods": [
    {
      "source": "auth-microservice",
      "mood": "Anxious",
      "timestamp": "2023-10-27T10:30:10.555444333Z"
    },
    {
      "source": "database-replica-01",
      "mood": "Serene",
      "timestamp": "2023-10-27T10:30:05.987654321Z"
    },
    {
      "source": "frontend-service-alpha",
      "mood": "Optimistic",
      "timestamp": "2023-10-27T10:30:00.123456789Z"
    }
  ]
}
```

## Development

### Project Structure

```
nightly-network-mood-ring/
├── README.md
├── src/
│   └── main.go
└── tests/
    └── main_test.go
```

### Running Tests

Navigate to the `tests` directory and run:

```bash
cd tests
go test .
```
