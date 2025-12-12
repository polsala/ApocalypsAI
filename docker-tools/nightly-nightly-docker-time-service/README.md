# nightly-docker-time-service

A tiny Dockerized HTTP service that returns the current UTC time (or an overridden time) along with a whimsical message.

## Usage

```sh
# Build the image
docker build -t nightly-docker-time-service .

# Run the container (optional TIME_OVERRIDE)
docker run -d -p 8080:8080 -e TIME_OVERRIDE=2023-01-01T00:00:00Z nightly-docker-time-service

# Query the service
curl http://localhost:8080/
```

The service responds with JSON:

```json
{
  "time": "2023-01-01T00:00:00Z",
  "message": "The stars align in perfect harmony."
}
```

If `TIME_OVERRIDE` is not set, the current UTC time is used.

## Implementation

The service is a single Python script using the built‑in `http.server` module, packaged in an Alpine‑based Docker image.
