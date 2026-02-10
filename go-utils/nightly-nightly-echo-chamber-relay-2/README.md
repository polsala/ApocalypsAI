# Nightly Echo Chamber Relay

## Overview
`nightly-echo-chamber-relay` is a whimsical Go utility designed to simulate broadcasting a 'whisper' message across a distributed network of 'listening posts'. It takes a message, applies a light 'temporal distortion' (simple obfuscation), and then concurrently attempts to send it to several predefined (mocked) network endpoints. This tool showcases Go's concurrency features like goroutines, channels, and `sync.WaitGroup` for managing asynchronous operations.

It's useful for understanding basic concurrent network communication patterns, error handling in distributed systems, and simulating unreliable message delivery in a fun, post-apocalyptic context.

## Features
*   **Concurrent Broadcasting**: Sends messages to multiple 'listening posts' simultaneously.
*   **Temporal Distortion**: Applies a simple ROT13-like obfuscation to the message and introduces random delays for each transmission.
*   **Simulated Network**: Uses an HTTP client (mocked in tests) to simulate sending data to endpoints.
*   **Result Aggregation**: Collects and reports the outcome of each broadcast attempt.

## How to Run

1.  **Prerequisites**: Ensure you have Go (version 1.16 or higher) installed.

2.  **Navigate to the utility directory**:
    ```bash
    cd go-utils/nightly-echo-chamber-relay
    ```

3.  **Run the utility**: Provide the message you wish to broadcast as a command-line argument.
    ```bash
    go run src/main.go "The void whispers back..."
    ```

    The utility will output the obfuscated message and the results of each broadcast attempt to the console.

## How to Test

1.  **Navigate to the utility directory**:
    ```bash
    cd go-utils/nightly-echo-chamber-relay
    ```

2.  **Run the tests**:
    ```bash
    go test ./tests/...
    ```

    The tests use a mock HTTP client to simulate network interactions, ensuring deterministic and offline execution. They verify the message obfuscation, concurrent broadcasting logic, and correct handling of success and failure scenarios without making actual network calls.
