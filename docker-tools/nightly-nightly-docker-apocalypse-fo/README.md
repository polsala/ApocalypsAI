# Apocalypse Fortune Docker

A tiny Docker container that prints a random apocalypse‑themed fortune. Perfect for a quick morale boost in the terminal.

## Build

```sh
docker build -t apocalypse-fortune .
```

## Run

```sh
docker run --rm apocalypse-fortune
```

You can also force a specific fortune by setting the `FORTUNE_INDEX` environment variable:

```sh
docker run --rm -e FORTUNE_INDEX=2 apocalypse-fortune
```

## How it works

The container ships a Bash script that reads `fortunes.txt` and selects a line either randomly or by the provided index.
