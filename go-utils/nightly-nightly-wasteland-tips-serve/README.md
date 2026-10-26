# Wasteland Tips Server

A whimsical Go utility that serves random post‑apocalypse survival tips over HTTP. Run the server and query `http://localhost:8080/tip` to receive a tip. The server logs each request concurrently and rotates tips every minute.

## Build

```sh
go build -o wasteland-tips ./src
```

## Run

```sh
./wasteland-tips
```

## Endpoints

- `GET /tip` – returns JSON `{ "tip": "..." }`
- `GET /health` – returns `OK`

## Testing

```sh
go test ./...
```
