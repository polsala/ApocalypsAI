# nightly-portal-traffic-simulator

## Overview

`nightly-portal-traffic-simulator` is a tiny Go web service that pretends to be a mystical portal gateway.  It serves two endpoints:

* **`/greet`** – Returns a random whimsical greeting in JSON format.
* **`/stats`** – Returns the total number of `/greet` requests served since the process started.

The service is fully concurrent, using atomic counters and the standard library only.  It can be used for:

* Load‑testing reverse proxies or API gateways.
* Demonstrating Go’s lightweight concurrency.
* Adding a bit of fun to local development environments.

## Build & Run

```bash
# Clone the repository (or copy the utility folder) and cd into it
cd utils/nightly-portal-traffic-simulator

# Build the binary
go build -o portal-simulator ./src/main.go

# Run the server (listens on port 8080)
./portal-simulator
```

The server will log a startup message and then listen for HTTP requests.

## Example Requests

```bash
# Get a random greeting
curl http://localhost:8080/greet
# => {"message":"Your destiny awaits beyond the portal."}

# Check how many greetings have been served
curl http://localhost:8080/stats
# => {"total_requests":1}
```

## Testing

Run the unit tests with the standard Go toolchain:

```bash
go test ./tests/...
```

All tests are deterministic and do not require network access.

## License

MIT © ApocalypsAI Community
