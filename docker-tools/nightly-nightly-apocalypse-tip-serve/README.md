# Nightly Apocalypse Tip Server

A tiny Dockerized HTTP server that serves a deterministic post‑apocalyptic survival tip on each request. The tip is chosen based on the `SEED` environment variable, making it reproducible for testing or fun.

## Build

```sh
docker build -t apocalypse-tip .
```

## Run

```sh
docker run -d -p 8080:8080 -e SEED=42 --name tip_server apocalypse-tip
```

Visit `http://localhost:8080/` to see the tip.

## Testing

```sh
cd tests && ./test_server.sh
```
