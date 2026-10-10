# Nightly Temporal Echo Chamber

## Overview

The `nightly-temporal-echo-chamber` is a whimsical-yet-useful Go-based utility designed to introduce controlled temporal distortions into your message flows. It acts as a proxy, receiving HTTP POST messages, holding onto them for a specified 'temporal distortion' period, and then re-broadcasting them to a designated output URL.

This tool is invaluable for:

*   **Simulating Network Latency:** Test how your distributed systems behave under various network delays.
*   **Asynchronous Processing Testing:** Verify the resilience of services expecting delayed or out-of-order messages.
*   **Debugging Race Conditions:** Introduce predictable delays to expose time-sensitive bugs.
*   **Chaos Engineering Lite:** A gentle way to inject temporal chaos into your development or staging environments.

## Features

*   **Concurrent Handling:** Processes multiple incoming messages simultaneously using Go goroutines.
*   **Configurable Delay:** Easily set the delay duration in milliseconds.
*   **HTTP POST Support:** Listens for and re-broadcasts HTTP POST requests, preserving headers like `Content-Type`.
*   **Lightweight:** A single Go executable with minimal dependencies.

## Usage

### Build

To build the executable, navigate to the `src` directory and run:

```bash
go build -o temporal-echo-chamber main.go
```

This will create an executable named `temporal-echo-chamber` in the current directory.

### Run

Run the utility from the command line, specifying the listening port, the output URL, and the desired delay:

```bash
./temporal-echo-chamber --port 8080 --output-url http://localhost:8081/receiver --delay 5000
```

**Command-line Flags:**

*   `--port <int>`: The port on which the echo chamber will listen for incoming POST requests. (Default: `8080`)
*   `--output-url <string>`: **(Required)** The full URL where delayed messages will be re-broadcasted. This must be an HTTP or HTTPS endpoint.
*   `--delay <int>`: The delay in milliseconds before a received message is re-broadcasted. (Default: `5000`)

### Example Scenario

1.  **Start your message receiver:**
    Imagine you have a simple HTTP server listening on `http://localhost:8081/receiver` that just logs incoming messages.

2.  **Start the Temporal Echo Chamber:**
    ```bash
    ./temporal-echo-chamber --port 8080 --output-url http://localhost:8081/receiver --delay 3000
    ```
    The echo chamber is now listening on port `8080` and will delay messages by 3 seconds.

3.  **Send a message to the Echo Chamber:**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello from the past!"}' http://localhost:8080/echo
    ```

4.  **Observe the delay:**
    You will immediately get an `HTTP 202 Accepted` response from the echo chamber. After approximately 3 seconds, your `http://localhost:8081/receiver` will receive the message.

## Development

### Prerequisites

*   Go (1.16 or higher)

### Project Structure

```
.gitignore
README.md
src/
  main.go
tests/
  main_test.go
```

### Running Tests

To run the automated tests, navigate to the `tests` directory and execute:

```bash
go test -v
```

Tests are designed to be deterministic and offline, using Go's `httptest` package to mock network interactions and a custom mock for `os.Exit` to test error handling.
