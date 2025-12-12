# Survival Tip Docker

A tiny Docker container that prints a random whimsical survival tip when run. Perfect for post‑apocalypse morale boosts.

## Build

```sh
docker build -t survival-tip .
```

## Run

```sh
docker run --rm survival-tip
```

Example output:

```
Never trust a cactus with a secret.
```

## How it works

The container uses a lightweight Python 3.11 Alpine image, copies a small script that selects a tip at random from an embedded list.
