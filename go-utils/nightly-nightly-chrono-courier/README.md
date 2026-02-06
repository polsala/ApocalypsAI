# Nightly Chrono-Courier

The Nightly Chrono-Courier is a whimsical-yet-useful Go service designed to simulate temporal communication delays. It acts as a message relay, receiving HTTP POST requests with a payload, holding them for a specified (or default) duration, and then forwarding them to a designated destination URL.

This utility is perfect for:
*   Testing the resilience of systems against network latency.
*   Simulating asynchronous communication patterns.
*   Adding a touch of "temporal distortion" to your development environment.
*   Ensuring your post-apocalyptic message delivery system can handle the occasional time-warp.

## Usage

### Running the Courier

1.  **Build:**
    ```bash
    go build -o chrono-courier src/main.go
    ```
2.  **Run:**
    ```bash
    ./chrono-courier
    ```
    The courier will listen on port `8080` by default.

### Configuration

You can configure the courier using environment variables:

*   `PORT`: The port the courier service will listen on (default: `8080`).
*   `DEFAULT_DELAY_SECONDS`: The default delay in seconds if not specified in the request (default: `5`).

Example:
```bash
PORT=8081 DEFAULT_DELAY_SECONDS=10 ./chrono-courier
```

### Sending a Message

Send an HTTP POST request to the courier's `/relay` endpoint with a JSON body:

```json
{
    "destination_url": "http://localhost:9000/receive-message",
    "message_body": {
        "sender": "Wasteland Wanderer",
        "content": "Supplies low, send help!",
        "timestamp": "2024-07-30T12:34:56Z"
    },
    "delay_seconds": 10
}
```

*   `destination_url` (required): The URL where the message will be relayed after the delay.
*   `message_body` (required): The JSON payload to be sent to the `destination_url`.
*   `delay_seconds` (optional): The delay in seconds before relaying. If omitted, `DEFAULT_DELAY_SECONDS` will be used.

**Example using `curl`:**

```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{
           "destination_url": "http://localhost:9000/receive-message",
           "message_body": {
             "sender": "Vault Dweller 76",
             "content": "Greetings from the bunker!",
             "sequence": 1
           },
           "delay_seconds": 3
         }' \
     http://localhost:8080/relay
```

The courier will acknowledge receipt immediately, and the message will be forwarded to `http://localhost:9000/receive-message` after 3 seconds.

## Development

### Running Tests

```bash
go test ./tests/...
```
