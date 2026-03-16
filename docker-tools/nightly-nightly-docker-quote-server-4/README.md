# nightly-docker-quote-server

A whimsical Dockerized HTTP server that returns a random post‑apocalyptic quote on each request.

## Usage

```sh
docker build -t quote-server .

docker run -p 8080:8080 quote-server
```

Then:

```sh
curl http://localhost:8080
```

Will output a random quote.

## How it works

The container runs a tiny Python script that selects a quote from a built‑in list and serves it via the built‑in `http.server` module.

## Testing

```sh
cd utils/docker-tools/nightly-docker-quote-server
./tests/test_server.sh
```
