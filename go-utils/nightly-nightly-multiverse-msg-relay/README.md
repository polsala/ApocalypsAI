# Nightly Multiverse Message Relay

The `nightly-multiverse-msg-relay` is a whimsical-yet-useful Go utility designed to broadcast messages across various "dimensions" (network endpoints) concurrently. Think of it as a cosmic switchboard for your data, ensuring your vital communiques reach every corner of your distributed reality.

## Features

*   **Concurrent Broadcasting**: Utilizes Go's goroutines to send messages to multiple destinations simultaneously.
*   **Configurable Dimensions**: Easily specify a list of TCP addresses where messages should be relayed.
*   **Simple TCP Interface**: Listens for incoming messages on a designated TCP port.

## How to Use

### Prerequisites

*   Go (version 1.18 or higher)

### Build

Navigate to the `src` directory and build the executable:

```bash
cd go-utils/nightly-multiverse-msg-relay/src
go build -o multiverse-relay .
```

### Run the Relay Server

The relay server requires a listening address and a comma-separated list of destination addresses.

```bash
./multiverse-relay --listen ":8080" --destinations ":8081,:8082,:8083"
```

*   `--listen`: The TCP address (e.g., `:8080` for all interfaces on port 8080) where the relay will listen for incoming messages.
*   `--destinations`: A comma-separated list of TCP addresses (e.g., `:8081,:8082`) to which the relay will broadcast received messages.

### Send a Message to the Relay

You can use `netcat` or a simple Go client to send a message to the relay.

**Example using `netcat`:**

First, ensure your destination "dimensions" are listening. For testing, you can run multiple `netcat` instances in separate terminals:

```bash
nc -l -p 8081
nc -l -p 8082
nc -l -p 8083
```

Then, send a message to the relay:

```bash
echo "Hello, Multiverse!" | nc localhost 8080
```

You should see "Hello, Multiverse!" appear in the `netcat` terminals listening on ports 8081, 8082, and 8083.

## Development & Testing

### Running Tests

Navigate to the `tests` directory and run the tests:

```bash
cd go-utils/nightly-multiverse-msg-relay/tests
go test -v .
```

The tests simulate network interactions locally to ensure the relay broadcasts messages correctly to all specified destinations.
