# Radio Static Simulator

A whimsical Go utility that simulates a post‑apocalyptic radio. It accepts messages via HTTP **POST** and streams them back to connected clients with simulated static noise using Server‑Sent Events (SSE). This project demonstrates Go concurrency, channels, and HTTP handling.

## Build

```sh
go build -o radio-static ./src
```

## Run

```sh
./radio-static
# Server listens on :8080
```

## API

- `POST /broadcast` with JSON `{"msg":"your message"}` – broadcast a message to all listeners.
- `GET /stream` – SSE endpoint; receives messages with static.

## Example

```sh
curl -X POST -H "Content-Type: application/json" -d '{"msg":"Hello"}' http://localhost:8080/broadcast
curl http://localhost:8080/stream
```

The stream will emit lines like:

```
data: H~l~o
```

where random static characters (`~`, `*`, `#`) replace about 30% of the original characters.

## Testing

Run the test suite with:

```sh
go test ./...
```

---

Enjoy the crackle of the wasteland radio!
