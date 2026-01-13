# nightly-docker-echo

A tiny Docker‑friendly HTTP echo service for quick connectivity checks.

## Features

- Exposes `/echo` endpoint that returns the `msg` query parameter or a default greeting.
- Simple Go implementation, minimal dependencies.
- Dockerfile included for containerized deployment.

## Usage

```bash
# Build the image
docker build -t nightly-docker-echo .

# Run the container
docker run -d -p 8080:8080 nightly-docker-echo

# Test the service
curl \"http://localhost:8080/echo?msg=Hello\"
# => Hello

curl \"http://localhost:8080/echo\"
# => Hello, world!
```

## Testing

Run the Go tests locally:

```bash
go test ./...
```

The tests are deterministic and do not require Docker.

## License

MIT
