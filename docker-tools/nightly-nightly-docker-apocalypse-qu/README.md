# Apocalypse Quote Docker

A tiny Docker container that prints a random post‑apocalyptic quote each time it starts. Perfect for adding a bit of flavor to your CI logs or terminal.

## Build

```sh
docker build -t apocalypse-quote .
```

## Run

```sh
docker run --rm apocalypse-quote
```

## How it works

The container is based on Alpine Linux and runs a small Bash script that selects a quote from a built‑in list.
