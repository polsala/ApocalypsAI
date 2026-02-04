# Nightly Temporal Replay Box

A whimsical-yet-useful containerized HTTP proxy that records incoming requests and allows you to view their 'echoes' (recorded details) with timestamps. This utility is perfect for debugging API integrations, understanding request flows, or simply capturing a historical log of interactions without needing a full-fledged database.

## Features

*   **Echo Endpoint (`/echo`)**: Acts as a simple HTTP endpoint that captures the method, URL, headers, body, and timestamp of any incoming request.
*   **History Endpoint (`/history`)**: Returns a JSON array of all recorded requests, providing a 'temporal echo' of past interactions.
*   **Containerized**: Easily deployable and runnable using Docker.

## How to Use

### 1. Build the Docker Image

Navigate to the `nightly-temporal-replay-box` directory and build the Docker image:

```bash
docker build -t temporal-replay-box .
```

### 2. Run the Container

Run the container, mapping port `8080` from the container to your host machine (e.g., `8080`):

```bash
docker run -d --name temporal-replay-box-instance -p 8080:8080 temporal-replay-box
```

### 3. Send Requests to the Echo Endpoint

Send any HTTP request to `http://localhost:8080/echo`. The server will record the request details and respond with a simple confirmation.

**Example (GET request):**

```bash
curl http://localhost:8080/echo/some/path?query=param
```

**Example (POST request with JSON body):**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello from the past!"}' http://localhost:8080/echo/data
```

### 4. View the History (Echoes)

To see all recorded requests, make a GET request to the `/history` endpoint:

```bash
curl http://localhost:8080/history
```

This will return a JSON array containing all the 'echoes' captured by the server.

### 5. Clean Up

When you're done, stop and remove the container:

```bash
docker stop temporal-replay-box-instance
docker rm temporal-replay-box-instance
```

Optionally, remove the Docker image:

```bash
docker rmi temporal-replay-box
```
