# Nightly Gossip Relay Beacon

## Overview

The `nightly-gossip-relay-beacon` is a whimsical yet robust utility designed to facilitate decentralized message relay in a post-apocalyptic network. Built with Go, it leverages concurrency to act as a 'gossip' node, receiving short messages (whispers) and forwarding them to a configured list of peer beacons. This ensures that vital information, no matter how small, can propagate through a resilient, distributed network, even if some nodes are temporarily offline.

Think of it as a digital carrier pigeon service, but with more goroutines and less actual pigeons.

## Features

*   **Decentralized Message Relay:** Each beacon operates independently, forwarding messages to known peers.
*   **Concurrent Handling:** Utilizes Go's goroutines to efficiently handle multiple incoming connections and outgoing relays simultaneously.
*   **Simple Protocol:** Expects newline-terminated messages, making it easy to integrate with other tools.
*   **Configurable Peers:** Define other beacon addresses to create your gossip network.
*   **Resilient:** Attempts to relay messages to all known peers, tolerating temporary connection failures.

## Installation

To install the `nightly-gossip-relay-beacon`, ensure you have Go (1.16 or higher) installed.

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/go-utils/nightly-gossip-relay-beacon
go build -o gossip-beacon src/main.go
```

This will create an executable named `gossip-beacon` in the current directory.

## Usage

Run the beacon executable, specifying its listening port and a comma-separated list of peer addresses.

```bash
./gossip-beacon -port 8080 -peers "localhost:8081,localhost:8082"
```

### Command-line Arguments:

*   `-port <port>`: The port this beacon will listen on for incoming messages (e.g., `8080`).
*   `-peers <addresses>`: A comma-separated list of `host:port` addresses of other gossip beacons to which messages should be relayed (e.g., `"localhost:8081,192.168.1.10:8083"`).

### Example Scenario:

1.  **Start Beacon A:**
    ```bash
    ./gossip-beacon -port 8080 -peers "localhost:8081,localhost:8082"
    ```

2.  **Start Beacon B:**
    ```bash
    ./gossip-beacon -port 8081 -peers "localhost:8080,localhost:8082"
    ```

3.  **Start Beacon C:**
    ```bash
    ./gossip-beacon -port 8082 -peers "localhost:8080,localhost:8081"
    ```

4.  **Send a message to Beacon A (using `netcat` or similar):**
    ```bash
    echo "The raiders are coming from the east!" | nc localhost 8080
    ```

    You should see the message logged by Beacon A, and then subsequently by Beacon B and Beacon C as it's relayed.

## Development

### Running Tests

```bash
cd go-utils/nightly-gossip-relay-beacon
go test ./tests/...
```

## Contributing

Feel free to fork, modify, and submit pull requests. All contributions are welcome, especially those that enhance the resilience and whimsy of our post-apocalyptic communication infrastructure.
