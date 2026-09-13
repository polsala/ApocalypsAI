# Nightly Docker Survival Tip Server

A tiny Dockerized HTTP server that serves random post‑apocalyptic survival tips.

## Build

```sh
docker build -t nightly-survival-tip .
```

## Run

```sh
docker run -p 8080:8080 -e TIP_INDEX=0 nightly-survival-tip
```

Visit `http://localhost:8080` to see the tip.

## Custom tip

Set `TIP_INDEX` (0‑based) to select a specific tip.

## Whimsical note

Even in the wasteland, a good tip can be a lifesaver!
