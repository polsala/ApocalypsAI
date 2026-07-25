# Wasteland Timezone Teleporter

A tiny Go HTTP service that converts a given timestamp to a target timezone and adds a post‑apocalyptic flavor text.

## Usage

```sh
go run src/main.go
```

The server listens on `localhost:8080`. Make a request like:

```
GET /teleport?time=2023-01-01T15:04:05Z&tz=America/New_York
```

### Response

```json
{
  "original": "2023-01-01T15:04:05Z",
  "target": "2023-01-01T10:04:05-05:00",
  "message": "The sun rises over the rusted ruins."
}
```

## Build

```sh
go build -o teleporter src/main.go
```

## Tests

```sh
go test ./...
```
