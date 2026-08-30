# Nightly Starlight Signal Relay

## Summary

The `nightly-starlight-signal-relay` is a whimsical-yet-useful Go-based TCP server designed to act as a central hub for broadcasting messages across a network. When a client sends a message, the relay imbues it with a 'cosmic timestamp' (a precise UTC timestamp) and a unique 'starlight signature' (a short, deterministic hash of the message and its context) before broadcasting it to all other connected clients. It's perfect for low-bandwidth, high-imagination communication networks in the post-apocalyptic era.

## How it Works

1.  **Server Startup**: The Go server listens on a specified TCP port (defaulting to `8080`).
2.  **Client Connection**: Any TCP client can connect to the server.
3.  **Message Reception**: When a client sends a newline-terminated message, the server receives it.
4.  **Cosmic Imbuement**: The server processes the message by:
    *   Adding a `[Cosmic Timestamp]` indicating when the message was received.
    *   Generating a `[Starlight Signature]` – a unique, short hash derived from the message content, timestamp, and sender ID.
5.  **Broadcast**: The newly imbued message is then broadcast to *all* currently connected clients, including the sender.
6.  **Concurrency**: The server handles multiple client connections concurrently using Go's goroutines, ensuring smooth operation even under heavy celestial traffic.

## Usage

### 1. Build the Server

Navigate to the `src` directory and build the Go executable:

```bash
cd nightly-starlight-signal-relay/src
go build -o starlight-relay .
```

### 2. Run the Server

Execute the compiled binary. You can optionally specify a port using the `PORT` environment variable.

```bash
./starlight-relay
# Or to specify a port:
PORT=9000 ./starlight-relay
```

The server will start listening and log its activity.

### 3. Connect Clients

You can use `netcat` (nc) or any other TCP client to connect to the relay.

```bash
nc localhost 8080
```

Once connected, type your message and press Enter. The server will process it and send it back to you, and to any other connected clients, with its cosmic enhancements.

**Example Client Interaction (using `nc` in two separate terminals):**

**Terminal 1 (Client A):**

```
nc localhost 8080
[Starlight Signal] 127.0.0.1:54321 has joined the relay.
Hello from Client A!
[2023-10-27T10:30:00.123456789Z] (From: 127.0.0.1:54321) Hello from Client A! [Signature: a1b2c3d4e5f6]
```

**Terminal 2 (Client B):**

```
nc localhost 8080
[Starlight Signal] 127.0.0.1:54321 has joined the relay.
[Starlight Signal] 127.0.0.1:54322 has joined the relay.
[2023-10-27T10:30:00.123456789Z] (From: 127.0.0.1:54321) Hello from Client A! [Signature: a1b2c3d4e5f6]
Message from Client B!
[2023-10-27T10:30:05.987654321Z] (From: 127.0.0.1:54322) Message from Client B! [Signature: f6e5d4c3b2a1]
```

(Note: IP addresses and timestamps will vary based on your system and connection.)
