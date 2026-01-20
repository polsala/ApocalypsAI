# Apocalyptic Echo Chamber

A whimsical yet useful Go utility that runs a concurrent TCP echo server. Every line received is echoed back with a random post‑apocalyptic prefix (e.g., `WASTELAND`, `RUINS`). The same binary can also act as a client to send a single message and print the server’s response.

## Build

```sh
go build -o apocalypse-echo ./src
```

## Usage

### Server

```sh
./apocalypse-echo -mode=server -port=8080
```

The server listens on the given port and handles multiple connections concurrently.

### Client

```sh
./apocalypse-echo -mode=client -port=8080 -msg="Hello, survivors!"
```

The client connects to the server, sends the message, prints the prefixed echo, and exits.

## Testing

```sh
go test ./...
```

The tests start an in‑process server and verify that the echoed response contains a valid prefix.
