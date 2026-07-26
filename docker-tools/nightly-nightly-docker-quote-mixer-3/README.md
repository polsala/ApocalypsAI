# Nightly Docker Quote Mixer

A whimsical Dockerized HTTP service that returns a randomly mixed post‑apocalyptic and inspirational quote. Useful for adding flavor to CI logs, chat bots, or terminal prompts.

## Usage

```sh
docker build -t quote-mixer .
docker run -p 8080:8080 quote-mixer
```

Then request:

```sh
curl http://localhost:8080/quote
```

Response:

```json
{"quote":"..."}
```

## How it works

The container runs a tiny Flask app. On each request it selects a random line from a curated list of mixed quotes.

## Testing

```sh
pytest -q
```
