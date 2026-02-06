# Nightly Docker Quote Server

A whimsical containerized Flask API that serves a random post‑apocalyptic quote on each request.

## How it works

The server holds a short list of themed quotes. When you hit the `/quote` endpoint it picks one at random and returns it as JSON:

```json
{"quote": "The ashes whisper, \"Tomorrow is a myth.\""}
```

## Build & Run

```sh
docker build -t nightly-docker-quote-server .
docker run -p 5000:5000 nightly-docker-quote-server
```

## Example

```sh
curl http://localhost:5000/quote
```

## Testing

```sh
pip install -r requirements.txt pytest
pytest
```
