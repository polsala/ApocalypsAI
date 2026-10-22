# Chrono Portal

`nightly-chrono-portal` is a tiny Go HTTP service that accepts a timestamp and a target IANA timezone, then returns the converted time wrapped in a dramatic, apocalyptic‑style message.

## Build & Run
```bash
# Clone the repository (or copy the utility folder)
cd utils/nightly-chrono-portal

# Build the binary
go build -o chrono-portal ./src/main.go

# Run (listens on port 8080)
./chrono-portal
```
The server will start and listen on `http://localhost:8080`.

## API
### `POST /convert`
Accepts a JSON payload:
```json
{
  "timestamp": "2023-10-10T12:00:00Z",   // RFC3339 format
  "timezone": "America/New_York"       // IANA timezone name
}
```
Responds with:
```json
{
  "message": "The sands of time now read: 2023-10-10 08:00:00 (America/New_York)"
}
```
If the request is malformed or uses a non‑POST method, the service returns an appropriate HTTP error code.

## Example
```bash
curl -X POST http://localhost:8080/convert \
  -H "Content-Type: application/json" \
  -d '{"timestamp":"2023-10-10T12:00:00Z","timezone":"America/New_York"}'
```

## Testing
Run the unit tests with:
```bash
go test ./tests/...
```
All tests are deterministic and use the standard library's `httptest` package, so no external network calls are made.
