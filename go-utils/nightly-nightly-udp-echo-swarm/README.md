# nightly-udp-echo-swarm

A whimsical yet useful Go CLI that sends a UDP echo message to multiple targets concurrently and reports latency statistics.

## Build

```sh
go build -o udp-echo-swarm ./src/main.go
```

## Usage

```sh
./udp-echo-swarm -hosts=127.0.0.1:9000,192.168.1.10:9000 -msg=ping -timeout=2s
```

- `-hosts` comma‑separated list of `host:port` to ping.
- `-msg` message to send (default `"ping"`).
- `-timeout` per‑host timeout (default `2s`).

The tool prints each host with its round‑trip time or an error.
