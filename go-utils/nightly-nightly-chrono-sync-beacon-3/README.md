# Nightly Chrono-Sync Beacon

The wasteland's temporal anomalies can wreak havoc on coordinated efforts. The Nightly Chrono-Sync Beacon provides a reliable, synchronized "apocalyptic epoch" timestamp to any connected outpost, ensuring all systems operate on a consistent timeline.

This utility is a simple Go-based TCP server that listens for connections and, upon receiving a "TIME" request, responds with the current UTC timestamp.

## Usage

### 1. Build the Server

Navigate to the `src` directory and build the executable:

```bash
cd src
go build -o chrono-sync-beacon .
```

### 2. Run the Server

Execute the compiled binary. By default, it listens on port `8080`. You can specify a different port using the `PORT` environment variable.

```bash
./chrono-sync-beacon
# Or, to specify a port:
PORT=8081 ./chrono-sync-beacon
```

The server will start and log messages indicating it's listening.

### 3. Connect a Client

You can connect using `netcat` or any TCP client.

```bash
# Using netcat (assuming server is on port 8080)
echo "TIME" | nc localhost 8080
```

The server will respond with a UTC timestamp in RFC3339 format, e.g.:
`2023-10-27T10:30:00Z`

## Development & Testing

### Running Tests

Navigate to the `tests` directory and run the Go tests:

```bash
cd tests
go test -v .
```

The tests will start a temporary server, connect to it, request the time, and verify the response.
