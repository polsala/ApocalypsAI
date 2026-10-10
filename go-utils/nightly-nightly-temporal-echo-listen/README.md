# Nightly Temporal Echo Listener (NTEL)

The Nightly Temporal Echo Listener (NTEL) is a whimsical-yet-useful Go utility designed to capture and log "temporal echoes" – incoming HTTP requests – on a specified network port. Think of it as a sensitive antenna listening for faint signals from across the network, or perhaps even other dimensions!

Beyond its whimsical facade, NTEL serves as a practical tool for:
- **Debugging & Inspection**: Quickly see what HTTP requests are hitting a particular endpoint in a distributed system.
- **Lightweight Mock Server**: Use it as a simple endpoint for testing client applications.
- **Network Traffic Monitoring**: A basic "honeypot" to observe unexpected network activity on a given port.
- **Echo Relay**: Optionally forward all received echoes to another HTTP endpoint, acting as a simple proxy or data duplicator.

## Features

- Listens for HTTP requests (GET, POST, PUT, etc.) on a configurable port.
- Logs detailed information about each request: timestamp, remote address, method, path, headers, and a snippet of the request body.
- Logs are outputted as JSON lines, making them easy to parse and analyze.
- Supports concurrent handling of multiple incoming requests using Go's goroutines.
- Optional forwarding of all received requests to another URL.

## Usage

### Build

To build the executable from the utility's root directory:

```bash
go build -o bin/ntel src/main.go
```

The executable `ntel` will be created in the `bin/` directory.

### Run

Run NTEL from the root of the `nightly-temporal-echo-listener` directory:

```bash
./bin/ntel --port 8080 --log-file echoes.log
```

This will start the listener on port `8080` and log all echoes to `echoes.log`.

**Command-line Flags:**

- `--port <number>`: The port NTEL will listen on. (Default: `8080`)
- `--log-file <path>`: Path to a file where echoes will be logged. If empty, logs to `stdout`. (Default: `""`)
- `--forward-url <url>`: An optional URL to forward all received echoes to. (Default: `""`)

**Examples:**

1.  **Listen on port 9000, log to console:**
    ```bash
    ./bin/ntel --port 9000
    ```

2.  **Listen on port 8081, log to a file, and forward to another service:**
    ```bash
    ./bin/ntel --port 8081 --log-file /var/log/ntel_echoes.json --forward-url http://localhost:5000/collector
    ```

### Sending an Echo

You can send an echo using `curl` or any HTTP client:

```bash
# GET request
curl http://localhost:8080/status

# POST request with JSON body
curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello from the past!"}' http://localhost:8080/api/temporal-rift
```

The NTEL server will respond with a message like: `Temporal echo received and processed at 2023-10-27T10:30:00Z!` and log the request details.

## Log Format

Each logged echo is a single JSON line, for example:

```json
{"timestamp":"2023-10-27T10:30:00.123456789Z","remote_addr":"127.0.0.1:54321","method":"POST","path":"/api/temporal-rift","headers":{"Content-Type":"application/json","User-Agent":"curl/7.81.0"},"body_snippet":"{\"message\": \"Hello from the past!\"}"}
```

## Development

### Running Tests

To run the automated tests from the utility's root directory:

```bash
go test -v ./tests/
```

The tests are self-contained and use `bytes.Buffer` and `httptest.NewServer` to mock external dependencies, ensuring determinism and offline execution.
