# Nightly Chrono-Sync Beacon

## Summary
A Go-based network beacon for resilient time synchronization across unreliable post-apocalyptic networks.

## Description
In the fractured timelines of the apocalypse, precise timekeeping is paramount. The Chrono-Sync Beacon offers a simple, robust mechanism for systems to attune to a central temporal pulse. Operating via UDP multicast, it's designed to cut through network interference, ensuring that even the most isolated outposts can maintain a semblance of synchronized reality.

Run it as a **beacon (server)** to broadcast the current "Apocalyptic Epoch" time, or as an **attuner (client)** to listen and report temporal drift. Its lightweight, concurrent design makes it ideal for environments where traditional NTP might be unavailable or untrustworthy.

## Features
*   **Beacon Mode**: Broadcasts current system time (Unix nanoseconds) and source ID over UDP multicast.
*   **Attuner Mode**: Listens for beacon pulses, calculates, and reports temporal drift against its local clock.
*   **Resilient**: Uses UDP multicast for simple, fire-and-forget broadcasting, suitable for lossy networks.
*   **Whimsical**: Embrace the "Apocalyptic Epoch" with a tool designed for temporal stability in chaos.

## Usage

### Build
To build the utility, navigate to the `src` directory and run:
```bash
go build -o chrono-sync-beacon ./src
```
This will create an executable named `chrono-sync-beacon` in the current directory.

### Beacon (Server) Mode
To start the Chrono-Sync Beacon as a server, broadcasting temporal pulses:
```bash
./chrono-sync-beacon -mode server -port 8080 -multicast 224.0.0.1:9999
```
*   `-mode server`: Specifies server operation.
*   `-port`: The UDP port the beacon will listen on (for its own operations, not for clients).
*   `-multicast`: The multicast IP address and port to broadcast to. Clients must listen on this address.

### Attuner (Client) Mode
To start the Chrono-Sync Attuner as a client, listening for temporal pulses and reporting drift:
```bash
./chrono-sync-beacon -mode client -port 8080 -multicast 224.0.0.1:9999
```
*   `-mode client`: Specifies client operation.
*   `-port`: The UDP port the attuner will listen on.
*   `-multicast`: The multicast IP address and port to listen on. Must match the beacon's broadcast address.

## Configuration

| Flag        | Default Value      | Description                                                               |
| :---------- | :----------------- | :------------------------------------------------------------------------ |
| `-mode`     | `client`           | Operation mode: `server` (beacon) or `client` (attuner).                  |
| `-port`     | `8080`             | UDP port for local binding (server) or listening (client).                |
| `-multicast`| `224.0.0.1:9999`   | Multicast address and port for broadcasting/listening.                    |

## Tests
To run the automated tests, navigate to the root of the utility directory and run:
```bash
go test ./tests
```
