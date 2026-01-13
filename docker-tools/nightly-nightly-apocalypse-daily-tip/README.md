# Apocalypse Daily Tip

A tiny Dockerized utility that prints a random post‑apocalyptic survival tip each time the container runs. Great for a daily morale boost in the wasteland.

## Usage

```sh
docker build -t apocalypse-tip .
docker run --rm apocalypse-tip
```

The container will output one tip, e.g.:

```
Always keep a spare bottle of water in your boot.
```

## How it works

The container runs a small Python module (`src.tip`) that selects a tip at random from a built‑in list.

