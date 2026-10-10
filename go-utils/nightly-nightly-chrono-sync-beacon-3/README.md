# Nightly Chrono-Sync Beacon

## Overview

The `nightly-chrono-sync-beacon` is a whimsical yet practical utility designed to help disparate systems in the post-apocalyptic landscape maintain synchronized time. It operates as a network beacon, broadcasting highly accurate (but delightfully phrased) time signals across a local multicast network. Clients can listen for these signals to synchronize their internal clocks, ensuring that all your temporal devices are aligned with the cosmic rhythm.

## Features

*   **Whimsical Time Broadcasts**: The server periodically sends out the current UTC time, embedded within a selection of poetic and evocative messages.
*   **Multicast Communication**: Utilizes UDP multicast for efficient one-to-many communication on a local network.
*   **Server/Client Modes**: Can run as a beacon server to broadcast time or as a client to receive and display synchronized time.
*   **Go-powered Concurrency**: Built with Go, leveraging its concurrency features for robust network operations.

## Installation

To install the `nightly-chrono-sync-beacon`, ensure you have Go (version 1.16 or higher) installed.

1.  Navigate to the `src` directory:
    ```bash
    cd go-utils/nightly-chrono-sync-beacon/src
    ```
2.  Build the executable:
    ```bash
    go build -o ../nightly-chrono-sync-beacon .
    ```
3.  The executable will be created in the parent directory (`go-utils/nightly-chrono-sync-beacon/`). You can move it to your `$PATH` if desired.

## Usage

The utility can be run in two modes: `server` or `client`.

### Running the Server

To start the Chrono-Sync Beacon server, which broadcasts time signals:

```bash
./nightly-chrono-sync-beacon server
```

The server will start broadcasting time messages every 5 seconds on the multicast address `224.0.0.1:9000`.

### Running the Client

To start a client that listens for and displays the synchronized time signals:

```bash
./nightly-chrono-sync-beacon client
```

The client will continuously listen for incoming time broadcasts and print the received whimsical message along with the extracted synchronized UTC time.

### Example Output (Server)

```
2023/10/27 10:30:05 Chrono-Sync Beacon Server starting on 224.0.0.1:9000...
2023/10/27 10:30:10 Broadcasted: "The cosmic clock ticks, marking the current epoch: 2023-10-27T10:30:10Z"
2023/10/27 10:30:15 Broadcasted: "A temporal ripple confirms the true time: 2023-10-27T10:30:15Z"
```

### Example Output (Client)

```
2023/10/27 10:30:06 Chrono-Sync Beacon Client listening on 224.0.0.1:9000...
2023/10/27 10:30:10 Received: "The cosmic clock ticks, marking the current epoch: 2023-10-27T10:30:10Z"
2023/10/27 10:30:10   Synchronized Time: 2023-10-27T10:30:10Z (UTC)
2023/10/27 10:30:15 Received: "A temporal ripple confirms the true time: 2023-10-27T10:30:15Z"
2023/10/27 10:30:15   Synchronized Time: 2023-10-27T10:30:15Z (UTC)
```

## Configuration

*   **Multicast Address**: `224.0.0.1:9000` (can be changed in `src/main.go`)
*   **Broadcast Interval**: 5 seconds (can be changed in `src/main.go`)

## Development

To run tests:

```bash
cd go-utils/nightly-chrono-sync-beacon/tests
go test .
```
