# Nightly Chronal Chatterbox

## Summary

The `nightly-chronal-chatterbox` is a whimsical-yet-useful Go-based network utility that simulates communication with a distant, glitchy future or past by introducing configurable network latency, packet loss, and temporal distortion to messages.

It operates as a server, listening for incoming messages. Upon receiving a message, it applies the configured temporal effects before echoing a (potentially distorted) response back to the sender. This can be used for testing application resilience under adverse network conditions, simulating unreliable remote services, or simply for a bit of fun with 'temporal echoes'.

## Features

*   **Configurable Latency**: Introduce a delay before processing and responding to messages.
*   **Configurable Packet Loss**: Simulate unreliable connections by randomly dropping incoming messages.
*   **Temporal Distortion**: Apply subtle (or not-so-subtle) alterations to the message content, mimicking data corruption or temporal interference.
*   **Client Mode**: A simple built-in client to easily test the server.

## How it Works

The utility runs in two primary modes: server and client.

*   **Server Mode**: Listens on a specified port. When a client connects and sends a line of text, the server applies the configured `latency`, `packet-loss-prob`, and `distortion-intensity` before sending a response. Each client connection is handled concurrently using Go goroutines.
*   **Client Mode**: Connects to a running `chronal-chatterbox` server, sends a specified message, and prints the (potentially distorted) response.

## Installation

To build the `nightly-chronal-chatterbox`, you need Go (version 1.18 or higher) installed.

1.  **Clone the repository (if not already done):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/go-utils/nightly-chronal-chatterbox
    ```
2.  **Build the executable:**
    ```bash
    go build -o chronal-chatterbox src/main.go
    ```
    This will create an executable named `chronal-chatterbox` in the current directory.

## Usage

### Server Mode

Run the server with desired parameters:

```bash
./chronal-chatterbox server \
  --port 8080 \
  --latency "200ms" \
  --packet-loss-prob 0.1 \
  --distortion-intensity 1
```

**Server Flags:**

*   `--port <int>`: The port for the server to listen on (default: `8080`).
*   `--latency <duration>`: The simulated delay for each message (e.g., `100ms`, `2s`). (default: `0ms`)
*   `--packet-loss-prob <float>`: Probability (0.0 to 1.0) of a message being 'lost' (not responded to). (default: `0.0`)
*   `--distortion-intensity <int>`: Level of temporal distortion (0 = none, 1 = light, 2 = moderate, 3 = heavy). (default: `0`)

### Client Mode

Send a message to a running server:

```bash
./chronal-chatterbox client \
  --host localhost \
  --port 8080 \
  --message "Greetings from the present!"
```

**Client Flags:**

*   `--host <string>`: The hostname or IP address of the server (default: `localhost`).
*   `--port <int>`: The port of the server (default: `8080`).
*   `--message <string>`: The message to send to the server.

### Examples

1.  **Server with 500ms latency and light distortion:**
    ```bash
    ./chronal-chatterbox server --port 8081 --latency "500ms" --distortion-intensity 1
    ```

2.  **Client sending a message to the above server:**
    ```bash
    ./chronal-chatterbox client --port 8081 --message "Is anyone there?"
    ```
    *Expected (example) output:* `sI anyone there?` (character swap)

3.  **Server with 20% packet loss:**
    ```bash
    ./chronal-chatterbox server --port 8082 --packet-loss-prob 0.2
    ```

4.  **Client sending multiple messages (some might be lost):**
    ```bash
    for i in $(seq 1 5); do
      echo "Sending message $i..."
      ./chronal-chatterbox client --port 8082 --message "Ping $i"
      sleep 0.5
    done
    ```

## Development & Testing

To run the tests, navigate to the utility's directory and execute:

```bash
go test ./src/main_test.go
```

Tests are designed to be deterministic and offline, utilizing Go's `net.Pipe` for network simulation and custom mock implementations for `time.Sleep` and `math/rand` to ensure predictable outcomes.
