# Nightly Docker Cryptid Generator

Utility that runs in a Docker container and prints a random cryptid (mythical creature) description. Seedable for reproducible output.

## Build

```sh
docker build -t nightly-cryptid-generator .
```

## Run

```sh
# Random cryptid (different each run)
docker run --rm nightly-cryptid-generator

# Deterministic output using a seed
docker run --rm -e CRYPTID_SEED=0 nightly-cryptid-generator
```

## How it works

The container runs a tiny Python script that selects a cryptid from a built‑in list using the `random` module. If the environment variable `CRYPTID_SEED` is set, it seeds the RNG for reproducible results.
