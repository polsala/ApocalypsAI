# nightly-whispernet-beacon

## WhisperNet Beacon: Ephemeral Communication for the Apocalypse

The `nightly-whispernet-beacon` is a lightweight, concurrent Go service designed to facilitate basic, ephemeral communication across a network of distributed nodes. In a world of unreliable infrastructure, these beacons act as resilient points for broadcasting status updates ("heartbeats") and sending short, one-way messages ("whispers") to designated peers.

### Features

*   **Concurrent Operations**: Utilizes Go's goroutines for efficient handling of multiple peer communications and incoming requests.
*   **Periodic Heartbeats**: Automatically broadcasts its online status to configured peers at a specified interval.
*   **Ephemeral Whispers**: Allows sending short, one-time messages to individual peers or broadcasting to all known peers.
*   **Simple HTTP API**: Exposes a minimal HTTP endpoint for receiving whispers.
*   **Self-contained**: Compiles into a single, portable binary.

### How to Build

1.  Ensure you have Go (version 1.16 or higher) installed.
2.  Navigate to the utility's directory:
    ```bash
    cd nightly-whispernet-beacon
    ```
3.  Build the executable:
    ```bash
    go build -o whispernet-beacon src/*.go
    ```

### How to Run

Each beacon requires a unique ID, a listening port, and optionally a list of peer URLs.

**Example: Running three beacons**

First, open three separate terminal windows.

**Terminal 1 (Beacon Alpha):**
```bash
./whispernet-beacon -id alpha -port 8081 -peers http://localhost:8082,http://localhost:8083
```

**Terminal 2 (Beacon Beta):**
```bash
./whispernet-beacon -id beta -port 8082 -peers http://localhost:8081,http://localhost:8083
```

**Terminal 3 (Beacon Gamma):**
```bash
./whispernet-beacon -id gamma -port 8083 -peers http://localhost:8081,http://localhost:8082
```

Once running, you will see heartbeats being sent and received. Incoming whispers will be printed to the console.

### How to Send a Whisper Manually

You can send a whisper to any running beacon using `curl` or a similar HTTP client. The beacon listens for POST requests to `/whisper`.

**Example: Sending a whisper from an external source to Beacon Alpha:**

```bash
curl -X POST -H "Content-Type: text/plain" -d "Hello Alpha from the outside!" http://localhost:8081/whisper
```

**Example: Sending a whisper from Beacon Alpha's CLI (not implemented in this version, but could be added):**

This version focuses on the beacon service itself. To send a whisper *from* one beacon *to* another, you would typically use a separate CLI client that interacts with the beacon's internal `SendWhisper` or `BroadcastWhisper` logic, or extend the beacon to have a command-line interface for sending. For now, the `BroadcastStatus` function demonstrates internal sending.

### Configuration

*   `-id <string>`: Unique identifier for this beacon (e.g., `alpha`).
*   `-port <int>`: The port this beacon will listen on (e.g., `8081`).
*   `-peers <comma-separated-urls>`: A comma-separated list of URLs for other beacons (e.g., `http://localhost:8082,http://localhost:8083`).
*   `-heartbeat-interval <duration>`: How often to send heartbeats (e.g., `5s`, `1m`). Default is `10s`.

### Internal Working

Each `Beacon` instance runs an HTTP server to receive messages. It also periodically sends heartbeats to its configured peers. When a whisper is received, it's pushed onto an internal channel and then printed to the console. Sending whispers to multiple peers is done concurrently using goroutines, ensuring that a slow peer doesn't block communication with others.
