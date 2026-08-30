# Nightly Docker Survival Tip

A tiny Docker container that prints a random whimsical survival tip each time it runs.

## How it works

The container is based on Alpine Linux and includes a small shell script (`tip.sh`) that selects a random line from `tips.txt`. When the container starts, the script runs and outputs the tip to stdout.

## Build the image

```sh
docker build -t nightly-survival-tip .
```

## Run the container

```sh
docker run --rm nightly-survival-tip
```

You will see a random tip like:

```
Carry a rubber duck for morale boosts.
```

## Files

- `src/tip.sh` – the entrypoint script.
- `src/tips.txt` – a list of whimsical survival tips.
- `Dockerfile` – builds the container.

## Testing

Run the provided test script locally:

```sh
sh tests/test_tip.sh
```

It should output `PASS`.
