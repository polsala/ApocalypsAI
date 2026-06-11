# nightly-docker-apocalypse-tip

Utility: Docker container that prints a random post‑apocalyptic survival tip.

## Usage

```sh
docker build -t apocalypse-tip .
# Random tip (default)
docker run --rm apocalypse-tip
# Specific tip by index (zero‑based)
docker run --rm apocalypse-tip 3
```

## How it works

The container runs a tiny Python script `tip_generator.py` that holds a list of whimsical tips. When invoked without arguments it selects a random tip; when given an integer it returns that tip, which makes testing deterministic.

## Testing

Run the bundled pytest:

```sh
python -m pytest tests
```
