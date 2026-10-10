# Nightly Docker Quote of the Moment

A whimsical, self‑contained Docker container that prints a random (but optionally deterministic) quote each time it runs.

## Features
- Zero‑runtime dependencies – based on Alpine Linux and Bash.
- Deterministic output when the `SEED` environment variable is set.
- Perfect for a quick morale boost in CI logs, terminal sessions, or as a fun health‑check endpoint.

## Usage
```bash
# Build the image (optional – the CI will do this automatically)
docker build -t nightly-docker-quote-of-the-moment .

# Run with a random quote
docker run --rm nightly-docker-quote-of-the-moment

# Run with a deterministic quote (seed = 4)
docker run --rm -e SEED=4 nightly-docker-quote-of-the-moment
```

## How it works
The container ships a tiny Bash script that stores a hard‑coded list of witty sayings. If `SEED` is provided, the script uses it to pick a quote via modulo arithmetic; otherwise it falls back to the current Unix timestamp, ensuring a different quote on each invocation.

## Testing
Run the provided test script:
```bash
chmod +x tests/test_quote.sh
./tests/test_quote.sh
```
The test builds the image, runs it with `SEED=4`, and verifies the output matches the expected quote.
