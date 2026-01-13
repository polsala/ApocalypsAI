# nightly-docker-quote-of-the-day

A whimsical Docker utility that prints a random quote each time it runs.

## Features

- Zero‑runtime dependencies – just Alpine Linux and a shell script.
- Deterministic output when the `SEED` environment variable is set (useful for testing).
- Small image size (~5 MB).

## Build the image

```sh
docker build -t nightly-docker-quote-of-the-day .
```

## Run the container

```sh
# Random quote
docker run --rm nightly-docker-quote-of-the-day

# Deterministic quote (useful for scripts)
docker run --rm -e SEED=0 nightly-docker-quote-of-the-day
```

## How it works

The container copies a tiny shell script (`src/quote.sh`) into `/usr/local/bin/quote.sh` and sets it as the entrypoint. The script selects a quote from a hard‑coded array. If `SEED` is provided, the index is calculated as `SEED % number_of_quotes`; otherwise a random index is used via the shell's `$RANDOM` variable.

## Testing

The repository includes a Bash test that builds the image and verifies deterministic output when `SEED=0`. Run it with:

```sh
bash tests/test_container.sh
```

## License

MIT
