# Apocalypse Motivation Docker Container

A tiny Docker image that prints a whimsical daily motivation for post‑apocalyptic survivors each time it starts.

## Build

```sh
docker build -t apocalypse-motivation .
```

## Run

```sh
docker run --rm apocalypse-motivation
```

You can force a specific message (useful for testing) by setting the `MOTIVATION_INDEX` environment variable (0‑based):

```sh
docker run --rm -e MOTIVATION_INDEX=2 apocalypse-motivation
```

## How it works

The container ships a small shell script (`entrypoint.sh`) that selects a message from a built‑in list, either randomly or by the provided index, and prints it to stdout.
