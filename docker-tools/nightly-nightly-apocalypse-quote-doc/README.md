# Nightly Apocalypse Quote Docker

A tiny Docker image that prints a post‑apocalyptic motivational quote each time it runs.  By default the quote is chosen at random, but you can force a specific quote for testing or scripting via the `QUOTE_INDEX` environment variable.

## Build the image
```sh
docker build -t apoc-quote .
```

## Run the container (random quote)
```sh
docker run --rm apoc-quote
```

## Run the container with a deterministic quote
```sh
docker run --rm -e QUOTE_INDEX=2 apoc-quote
```
The above will always output:
```
Even in ruins, hope can be recycled.
```

## Testing
The repository includes a Python unittest that mocks Docker commands to verify deterministic output.
```sh
python -m unittest discover -v tests
```

## Files
- `Dockerfile` – builds a minimal Alpine image with the quote script.
- `src/quote.sh` – the Bash script that selects and prints a quote.
- `tests/test_quote_container.py` – unit tests using `unittest.mock` to simulate Docker.
