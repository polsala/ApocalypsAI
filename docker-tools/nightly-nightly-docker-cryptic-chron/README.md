# Cryptic Chronicle Docker

A whimsical Dockerized HTTP server that serves random apocalyptic prophecies.

## Build

```sh
docker build -t cryptic-chronicle .
```

## Run

```sh
docker run -p 8080:8080 cryptic-chronicle
```

Visit `http://localhost:8080` to receive a prophecy in JSON.

## Deterministic testing

Set the `FORTUNE_SEED` environment variable to control the output.

```sh
docker run -p 8080:8080 -e FORTUNE_SEED=5 cryptic-chronicle
```

Will always return the same prophecy.
