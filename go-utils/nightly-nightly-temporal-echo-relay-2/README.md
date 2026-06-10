# Nightly Temporal Echo Relay

## Summary

The `nightly-temporal-echo-relay` is a whimsical-yet-useful Go-based HTTP service designed to simulate network instability and temporal distortions. It accepts messages, applies a configurable delay, and then introduces a specified level of 'corruption' before returning the altered message. This utility is ideal for testing the fault tolerance and resilience of other systems, or simply for observing how messages might degrade across the spacetime continuum.

## Features

*   **Configurable Delay**: Introduce latency to message delivery.
*   **Simulated Corruption**: Messages can be randomly altered (case changes, character swaps, character replacements) to mimic data degradation or transmission errors.
*   **Concurrent Handling**: Built with Go's concurrency model to handle multiple echo requests simultaneously.
*   **Simple HTTP API**: Easy to integrate and use with `curl` or any HTTP client.

## How to Run

1.  **Prerequisites**: Ensure you have Go (version 1.16 or higher) installed.
2.  **Navigate**: Change into the `nightly-temporal-echo-relay/src` directory.
3.  **Build**: Compile the Go application:
    ```bash
    go build -o temporal-echo-relay main.go
    ```
4.  **Run**: Execute the compiled binary. The service will listen on port `8080` by default, or on the port specified by the `PORT` environment variable.
    ```bash
    ./temporal-echo-relay
    # Or, to specify a port:
    PORT=9000 ./temporal-echo-relay
    ```

The service will log its startup and incoming requests to the console.

## How to Use

The service exposes a single endpoint: `/echo` which accepts `POST` requests with a JSON payload.

### Request Format

Send a `POST` request to `http://localhost:8080/echo` (or your configured port) with a JSON body:

```json
{
  "message": "Your message to echo",
  "delay_ms": 1000,        // Optional: Delay in milliseconds (default 0)
  "corruption_level": 0.5  // Optional: Level of corruption (0.0 to 1.0, default 0.0)
}
```

*   `message` (string, required): The string message to be processed.
*   `delay_ms` (integer, optional): The time in milliseconds the service should wait before responding. If 0 or omitted, no delay is applied.
*   `corruption_level` (float, optional): A value between `0.0` (no corruption) and `1.0` (maximum corruption). This determines the probability of each character being altered. If 0.0 or omitted, no corruption is applied.

### Response Format

The service will respond with a JSON object containing the original and (potentially) corrupted message, and the delay applied.

```json
{
  "original_message": "Your message to echo",
  "corrupted_message": "Y0ur m3ss@g3 t0 3ch0",
  "delay_applied_ms": 1000
}
```

### Example using `curl`

1.  **Start the service** (if not already running):
    ```bash
    cd src
    go run main.go
    ```

2.  **Send an echo request with delay and corruption**:
    ```bash
    curl -X POST -H "Content-Type: application/json" \
         -d '{"message": "Hello ApocalypsAI Integrator!", "delay_ms": 2000, "corruption_level": 0.7}' \
         http://localhost:8080/echo
    ```

    You will observe a 2-second delay, and the response message will likely be garbled.

3.  **Send a simple echo request (no delay, no corruption)**:
    ```bash
    curl -X POST -H "Content-Type: application/json" \
         -d '{"message": "This message should be pristine."}' \
         http://localhost:8080/echo
    ```

    The response should be immediate and the message unchanged.

## Development

### Running Tests

To run the automated tests, navigate to the `nightly-temporal-echo-relay/tests` directory and execute:

```bash
cd tests
go test -v .
```

Tests are designed to be deterministic and offline, using mock objects for `time.Sleep` and a fixed random seed for the corruption logic.
