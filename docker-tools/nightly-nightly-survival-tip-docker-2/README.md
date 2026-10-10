# Survival Tip Docker Service

Provides a whimsical random survival tip via HTTP.

## Usage

```sh
# Build the Docker image
docker build -t survival-tip .

# Run the container (exposes port 8080)
docker run -p 8080:8080 survival-tip
```

The service will be available at `http://localhost:8080/tip`.

```sh
curl http://localhost:8080/tip
```

Typical response:

```json
{ "tip": "Always carry a rubber duck for morale." }
```

## How it works

A tiny Flask app selects a random tip from a hard‑coded list each time the `/tip` endpoint is hit.

## Testing

Run the unit tests locally (no Docker required):

```sh
python -m unittest discover -s tests
```

The tests verify that the tip selection logic works and that the Flask endpoint returns the expected JSON structure.
