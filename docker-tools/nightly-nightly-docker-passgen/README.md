# Nightly Docker Passgen

## Overview

`nightly-docker-passgen` provides a tiny Docker container that runs a Flask web service exposing a `/generate` endpoint.  The endpoint returns a cryptographically‑secure random password in JSON format.  It is useful for scripts, CI pipelines, or any situation where you need a quick, reproducible password generator without installing extra tools on the host.

## Features

- **Zero‑host dependencies** – everything runs inside the container.
- **Configurable length** via the `length` query parameter (default 12, max 64).
- **Stateless** – each request generates a fresh password.
- **Lightweight** – based on `python:3.11‑slim` and Flask.

## Build the image

```bash
docker build -t nightly-passgen .
```

## Run the container

```bash
# Run in detached mode, exposing port 8080
docker run -d -p 8080:8080 nightly-passgen
```

## Use the API

```bash
# Default length (12)
curl http://localhost:8080/generate

# Custom length (e.g., 20)
curl http://localhost:8080/generate?length=20
```

Response example:

```json
{
  "password": "aB3$dE9fGh!2"
}
```

## Development

The source lives under `src/`.  To test locally without Docker:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r src/requirements.txt
python src/app.py
```

Then visit `http://127.0.0.1:8080/generate`.

## Testing

Run the unit tests with:

```bash
python -m unittest discover -s tests
```

The tests verify password length handling and character set constraints without needing Docker to be installed.

