# Nightly Void Whisper Echo

A whimsical-yet-useful UDP echo server crafted in Go, designed to listen for incoming UDP packets and echo them back to the sender with a mysterious 'void whisper' prefix.

This utility can be used for:
- **Network Testing**: Verify UDP connectivity and basic packet flow.
- **Debugging**: Inspect what data is being sent over UDP to a specific port.
- **Mock Services**: Simulate a UDP service for development or testing other applications.
- **Whimsical Fun**: Just enjoy the void whispering back to you!

## How it Works

The server listens on a specified UDP port (defaulting to `8080`). When it receives a UDP packet, it prepends the string "The void echoes: " to the received message and sends the modified message back to the originating client.

## Installation

To build the utility, ensure you have Go (version 1.16 or higher) installed.

1.  Navigate to the `src` directory:
    ```bash
    cd go-utils/nightly-void-whisper-echo/src
    ```
2.  Build the executable:
    ```bash
    go build -o ../nightly-void-whisper-echo .
    ```
    This will create an executable named `nightly-void-whisper-echo` in the parent directory.

## Usage

Run the server from the utility's root directory:

```bash
./nightly-void-whisper-echo
```

The server will start listening on UDP port `8080` by default.

### Custom Port

You can specify a different port using the `PORT` environment variable:

```bash
PORT=9000 ./nightly-void-whisper-echo
```

### Sending Messages (Client Example)

You can use `netcat` (nc) or any UDP client to send messages to the server.

**Example using `netcat` (Linux/macOS):**

1.  Open a new terminal and run the server.
2.  Open another terminal and send a message:
    ```bash
    echo "Hello, Void!" | nc -u -w 1 127.0.0.1 8080
    ```
    (Replace `127.0.0.1` with the server's IP if running remotely, and `8080` with the server's port if changed.)

    You should see the echoed message in your `netcat` terminal (or the server's log):
    ```
    The void echoes: Hello, Void!
    ```

**Example using `netcat` (Windows - may require `ncat` from Nmap):**

```bash
(echo Hello, Void!) | ncat --udp 127.0.0.1 8080
```

## Development

### Running Tests

To run the automated tests, navigate to the `tests` directory and execute `go test`:

```bash
cd go-utils/nightly-void-whisper-echo/tests
go test -v .
```

The tests will start a temporary local UDP server and client to simulate network interactions, ensuring deterministic and offline validation of the echo logic.
