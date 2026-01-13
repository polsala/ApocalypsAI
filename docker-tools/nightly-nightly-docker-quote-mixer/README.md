# Nightly Docker Quote Mixer

## Overview

`nightly-docker-quote-mixer` is a tiny, containerized web service that returns a randomly mixed quote each time you hit the `/quote` endpoint. It blends an inspirational quote with a post‑apocalyptic tagline, giving you a daily dose of hopeful doom.

## Features

- **Zero‑config**: Just build the image and run it.
- **Lightweight**: Based on `python:3.11‑slim` and Flask.
- **Deterministic tests**: Uses mocked randomness for reliable CI.

## Build the Docker image

```bash
docker build -t nightly-docker-quote-mixer .
```

## Run the container

```bash
docker run -p 8080:8080 nightly-docker-quote-mixer
```

The service will be reachable at `http://localhost:8080/quote`.

## API

- **GET `/quote`** – Returns JSON:

```json
{
  "quote": "Your future is bright – The wasteland whispers your name."
}
```

## Testing

Run the test suite with:

```bash
pytest
```

The tests execute the Flask app directly (no Docker needed) and mock the random selection to guarantee deterministic output.

