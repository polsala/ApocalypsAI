# Nightly Apocalypse Affirmation

A tiny Docker container that prints a whimsical post‑apocalypse affirmation. Useful for a daily morale boost in your CI pipelines or terminal.

## Usage

```sh
docker run --rm -e AFFIRM_INDEX=3 nightly-apocalypse-affirmation
```

If `AFFIRM_INDEX` is not set, a random affirmation is chosen.

## How it works

The image is based on Alpine Linux and runs a small Bash script that selects a line from a built‑in list.

## Building locally

```sh
docker build -t nightly-apocalypse-affirmation .
```

## Testing

Run the provided test script:

```sh
./tests/test_docker.sh
```
