# nightly-radio-chatter-api

A whimsical Go HTTP server that serves random post‑apocalyptic radio chatter messages. Useful for testing chat‑bot integrations, demos, or just adding a bit of flavor to your projects.

## Usage

```sh
# Run directly (requires Go 1.18+)
go run src/main.go
```

The server listens on `localhost:8080`.

### Endpoints

- `GET /chatter?seed=<int>` – Returns a JSON payload with a deterministic message when a `seed` is supplied, otherwise the seed is derived from the current time.

Example response:

```json
{
  "seed": 123,
  "message": "radio static chant the names of heroes."
}
```

## Build

```sh
go build -o radio-chatter src/main.go
```

## Test

```sh
go test ./...
```

---

### Why this utility?

* **Whimsical** – The messages are crafted from a pool of post‑apocalyptic fragments.
* **Deterministic** – Supplying a `seed` yields the same message, making it perfect for automated tests.
* **Concurrent** – The Go HTTP server can handle many simultaneous requests out of the box.
