# Apocalypse Radio Server

**nightly‑apocalypse‑radio‑server** is a tiny Go utility that acts like a retro‑style radio broadcast from the wasteland.  When you run the server, it listens on a TCP port and, for every client that connects, streams a random post‑apocalyptic quote every few seconds.

## Features
- Concurrent handling of unlimited client connections (goroutine per client).
- Built‑in list of whimsical quotes; easy to extend.
- Configurable listen address and broadcast interval via command‑line flags.
- Zero external dependencies – pure Go standard library.

## Build
```bash
# Clone the repository (or copy the generated folder) and build
cd nightly-apocalypse-radio-server
go build -o radio-server ./src/main.go
```

## Run
```bash
# Start the server on the default address (0.0.0.0:8080) and 5‑second interval
./radio-server

# Custom address and interval (e.g., 127.0.0.1:9090, 2‑second interval)
./radio-server -addr 127.0.0.1:9090 -interval 2s
```

## Connect
You can connect with any TCP client (netcat, telnet, custom program):
```bash
nc localhost 8080
```
You will see a new quote printed every interval until you close the connection.

## Testing
```bash
go test ./tests
```
The test suite checks the quote‑selection logic and that the server can accept a client and deliver at least one quote.

## Extending
Add or modify quotes in `src/main.go` – the `quotes` slice is public‑ish and can be edited directly.

---
*Enjoy the static‑crackle of the wasteland!*
