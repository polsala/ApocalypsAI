# nightly-tcp-tunnel-keeper

A concurrent TCP tunnel that forwards traffic from a local port to a remote address, optionally injecting artificial latency for each direction. Perfect for testing network‑dependent applications in a post‑apocalyptic sandbox.

## Build

```sh
go build -o tcp-tunnel ./src/main.go
```

## Usage

```sh
./tcp-tunnel -l <local_port> -r <remote_host:remote_port> [-d <delay_ms>]
```

- `-l` local listening port (e.g., `8080`).
- `-r` remote target (e.g., `example.com:80`).
- `-d` optional artificial latency in milliseconds applied to each read/write.

The program logs each new connection with timestamps.

## Example

```sh
./tcp-tunnel -l 8080 -r example.com:80 -d 100
```

Will listen on port 8080, forward to example.com:80, and add 100 ms latency to every packet.

## License

MIT
