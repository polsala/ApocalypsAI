# nightly-timezone-teleporter

A tiny Go HTTP service that returns the current time for a requested IANA timezone.

## Features

- **Whimsical**: "teleport" yourself to any timezone with a single request.
- **Concurrent**: Handles many requests simultaneously using Go's built‑in concurrency.
- **Deterministic tests**: Time source can be mocked for reliable unit testing.

## Build

```bash
go build -o tz-teleporter ./src/main.go
```

## Run

```bash
./tz-teleporter -port 8080
```

The server will listen on `http://localhost:8080`.

## API

- `GET /now?tz=<IANA timezone>` – Returns JSON with the current time in the requested timezone.
  - If `tz` is omitted, a random timezone is chosen.
  - Example response:
    ```json
    {"timezone":"America/New_York","time":"2025-12-14T09:30:00-05:00"}
    ```

## Testing

```bash
go test ./tests
```

The test suite uses a mocked time source, so it runs offline and deterministically.
