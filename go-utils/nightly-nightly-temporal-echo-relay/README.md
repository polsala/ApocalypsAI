# Nightly Temporal Echo Relay

## Summary

The `nightly-temporal-echo-relay` is a Go-based utility designed to simulate an unreliable, time-distorted message relay. It's perfect for testing the resilience of your communication systems against network latency and packet loss, mimicking the challenging conditions of a post-apocalyptic network. Whether you're building a robust data transfer protocol or just want to see how your application handles chaos, this tool provides a configurable environment to introduce delays and message drops.

## Features

*   **Server Mode**: Listens for incoming TCP connections and echoes messages back after applying configurable distortions.
*   **Client Mode**: Sends messages to the relay server and reports on successful deliveries and latency.
*   **Configurable Delay**: Introduce artificial latency to messages.
*   **Configurable Packet Loss**: Simulate message drops with a specified probability.
*   **Concurrent**: Built with Go's goroutines for efficient handling of multiple connections.

## Build Instructions

1.  **Prerequisites**: Ensure you have Go (version 1.16 or higher) installed.
2.  **Navigate**: Change into the `nightly-temporal-echo-relay/src` directory.
    ```bash
    cd nightly-temporal-echo-relay/src
    ```
3.  **Build**: Compile the application.
    ```bash
    go build -o ../bin/echo-relay main.go
    ```
    This will create an executable named `echo-relay` in the `bin` directory one level up.

## Usage

### Running the Server

To start the Temporal Echo Relay server, specify the `server` command and optional parameters for port, delay, and loss probability.

```bash
./bin/echo-relay server [OPTIONS]
```

**Options:**

*   `-port <number>`: The port to listen on (default: `8080`).
*   `-delay <duration>`: Artificial delay to introduce before echoing messages, e.g., `100ms`, `1s` (default: `0s`).
*   `-loss <probability>`: Probability of dropping a message (0.0 to 1.0, default: `0.0`).

**Example:**

```bash
./bin/echo-relay server -port 8081 -delay 500ms -loss 0.2
```
This starts a server on port 8081, adding a 500ms delay and a 20% chance of dropping messages.

### Running the Client

To send messages to a running server, specify the `client` command and the server address.

```bash
./bin/echo-relay client [OPTIONS]
```

**Options:**

*   `-addr <host:port>`: The address of the echo relay server (default: `localhost:8080`).
*   `-messages <number>`: Number of messages to send (default: `5`).
*   `-interval <duration>`: Interval between sending messages, e.g., `200ms`, `1s` (default: `1s`).

**Example:**

```bash
./bin/echo-relay client -addr localhost:8081 -messages 10 -interval 200ms
```
This client will send 10 messages to `localhost:8081` with a 200ms interval between each.

## Development & Testing

To run the tests, navigate to the `nightly-temporal-echo-relay/tests` directory and execute:

```bash
cd nightly-temporal-echo-relay/tests
go test .
```
