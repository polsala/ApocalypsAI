# nightly-udp-broadcast-relay

Utility that can act as a UDP broadcast relay or a simple sender. In a post‑apocalyptic setting you can use it to forward short status beacons between scattered outposts.

## Build

```sh
go build -o udp-relay ./src/main.go
```

## Usage

### Relay mode

```sh
./udp-relay -mode=relay -listen=:9000 -targets=localhost:9001,localhost:9002
```

Listens on UDP port 9000 and forwards any incoming packet to the target addresses.

### Send mode

```sh
./udp-relay -mode=send -addr=localhost:9000 -msg="Supplies arriving"
```

Sends a single UDP packet with the given message to the relay.

## Testing

```sh
go test ./tests
```
