# Nightly Docker Quote Mixer

## Overview
A tiny Docker container that runs a Flask web service. When you hit `/quote` it returns a whimsical quote that blends a post‑apocalyptic and inspirational saying.

## Build
```sh
docker build -t nightly-docker-quote-mixer .
```

## Run
```sh
docker run -p 8080:8080 nightly-docker-quote-mixer
```

## Usage
```sh
curl http://localhost:8080/quote
```
Response:
```json
{"quote":"..."}
```

## Testing
```sh
python -m pytest -q
```
