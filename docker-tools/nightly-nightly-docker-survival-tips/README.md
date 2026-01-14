# nightly‑docker‑survival‑tips

A tiny Docker image that prints a post‑apocalyptic survival tip each time it runs.

## How it works
The image contains a small Go binary. When executed it selects a tip from a built‑in list.

* Without any environment variables it picks a random tip.
* Set the `SEED` environment variable to an integer to get a deterministic tip (useful for testing).

## Build the image
```bash
docker build -t nightly-docker-survival-tips .
```

## Run the container
```bash
# Random tip
docker run --rm nightly-docker-survival-tips

# Deterministic tip (e.g., seed 42)
docker run --rm -e SEED=42 nightly-docker-survival-tips
```

## Testing
A simple shell test is provided under `tests/test.sh`. It builds the image, runs it with a known seed, and checks the output.

```bash
cd tests && bash test.sh
```

## License
MIT © ApocalypsAI
