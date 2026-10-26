# nightly-dockerized-quote-mixer

A whimsical Dockerized Go utility that mixes two random quotes into a single mashup. It can be used for fun messages in CI logs, chat bots, or as a tiny micro‑service.

## Build

```sh
docker build -t nightly-dockerized-quote-mixer .
```

## Run

```sh
# Random output (different each run)
docker run --rm nightly-dockerized-quote-mixer

# Deterministic output using a seed (useful for testing)
docker run --rm -e SEED=42 nightly-dockerized-quote-mixer
```

## How it works

The Go program contains two hard‑coded quote lists. With a seed (either via the `--seed` flag or the `SEED` environment variable) it selects one quote from each list and prints them concatenated.
