# Nightly Chrono-Echo Pinger

## Overview

The `nightly-chrono-echo-pinger` is a whimsical-yet-useful Go-based network utility designed for the ApocalypsAI community. In a world where stable communication is a luxury, this tool helps detect 'chronal anomalies' (unusual network latency) by sending out 'temporal pings' and listening for 'echoes' from other instances running on the network. It's a simple way to gauge network health and identify potential communication disruptions.

## Features

*   **Temporal Pinging**: Periodically broadcasts UDP packets containing a timestamp.
*   **Echo Reception**: Listens for incoming pings, calculates Round-Trip Time (RTT), and sends back an echo.
*   **Chronal Anomaly Detection**: Flags RTTs that exceed a configurable threshold as 'chronal anomalies'.
*   **Concurrent Operation**: Utilizes Go's goroutines for efficient, concurrent sending and receiving of pings.

## Usage

### Prerequisites

*   Go (version 1.16 or higher)

### Build

```bash
go build -o chrono-echo-pinger src/main.go
```

### Run

To run the pinger, specify the broadcast address and port. You can run multiple instances on the same network to observe echoes.

```bash
./chrono-echo-pinger --address 255.255.255.255:8080 --interval 2s --threshold 500ms
```

**Arguments:**

*   `--address`: The UDP broadcast/multicast address and port to use (e.g., `255.255.255.255:8080` for broadcast, or a multicast address like `224.0.0.1:8080`).
*   `--interval`: The interval at which to send pings (e.g., `1s`, `500ms`). Default is `1s`.
*   `--threshold`: The RTT threshold (e.g., `200ms`, `1s`) above which an 'anomaly' is reported. Default is `200ms`.

### Example Output

```
[INFO] Sending temporal ping to 255.255.255.255:8080...
[INFO] Received echo from 192.168.1.10:54321, RTT: 12ms
[INFO] Received echo from 192.168.1.11:54322, RTT: 25ms
[INFO] Sending temporal ping to 255.255.255.255:8080...
[WARN] Chronal Anomaly Detected! Echo from 192.168.1.12:54323, RTT: 550ms (Threshold: 200ms)
```

## How it Works

Each instance of `chrono-echo-pinger` does two things concurrently:

1.  **Pinger**: Every `--interval`, it sends a UDP packet containing the current Unix timestamp in milliseconds to the specified broadcast/multicast address.
2.  **Echo Listener**: It continuously listens on the specified address. When it receives a packet:
    *   It parses the sender's timestamp.
    *   It calculates the RTT (`current_time - sender_timestamp`).
    *   It logs the RTT.
    *   If the RTT exceeds `--threshold`, it logs a 'Chronal Anomaly'.
    *   It then sends back an 'echo' packet to the sender's address, containing its own current timestamp.

This creates a simple, distributed ping-pong mechanism to monitor network responsiveness.
