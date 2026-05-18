# Nightly Temporal Echo Relay

A Go-based HTTP service that acts as a 'Temporal Echo Relay', introducing configurable delays to messages before forwarding them to a target URL. This utility is designed to simulate unreliable network conditions, such as those found in a post-apocalyptic wasteland, making it useful for testing the resilience and latency tolerance of distributed systems.

## Features

*   **Configurable Delay**: Specify a delay in milliseconds for each message.
*   **HTTP-based**: Simple RESTful API for sending messages.
*   **Asynchronous Forwarding**: Responds immediately to the client while forwarding the message in the background after the specified delay.
*   **Error Logging**: Logs forwarding attempts and any errors encountered.

## How to Run

1.  **Prerequisites**: Ensure you have Go (1.16 or higher) installed.
2.  **Navigate to the utility directory**:
    ```bash
    cd go-utils/nightly-temporal-echo-relay
    ```
3.  **Build the executable**:
    ```bash
    go build -o temporal-echo-relay src/main.go
    ```
4.  **Run the server**:
    ```bash
    ./temporal-echo-relay
    ```
    The relay will start listening on `http://localhost:8080`.

## Usage

Send a POST request to the `/relay` endpoint with a JSON payload.

**Endpoint**: `POST /relay`

**Request Body (JSON)**:

```json
{
  "message": "Your message content here",
  "target_url": "http://your-target-service.com/endpoint",
  "delay_ms": 500 // Optional: delay in milliseconds. Defaults to 100ms if not provided or <= 0.
}
```

**Example using `curl`**:

```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello from the past!", "target_url": "http://localhost:9000/receive-echo", "delay_ms": 2000}' \
     http://localhost:8080/relay
```

This will immediately return a success message, and after 2 seconds, the `{"echo_message": "Hello from the past!"}` payload will be POSTed to `http://localhost:9000/receive-echo`.

### Setting up a simple target service for testing (e.g., using Python Flask):

```python
# target_service.py
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/receive-echo', methods=['POST'])
def receive_echo():
    data = request.get_json()
    print(f"[{datetime.datetime.now()}] Received echo: {data.get('echo_message')}")
    return jsonify({"status": "received", "message": data.get('echo_message')}), 200

if __name__ == '__main__':
    app.run(port=9000, debug=True)
```

Run this Python script (`python target_service.py`) in a separate terminal, then send requests to the `temporal-echo-relay` as shown above.

## How to Test

1.  **Navigate to the utility directory**:
    ```bash
    cd go-utils/nightly-temporal-echo-relay
    ```
2.  **Run tests**:
    ```bash
    go test ./tests/...
    ```

The tests use `httptest.NewServer` to create in-memory HTTP servers for mocking the target URL and a custom mock for `time.Sleep` to ensure deterministic and fast execution without actual network calls or delays.
