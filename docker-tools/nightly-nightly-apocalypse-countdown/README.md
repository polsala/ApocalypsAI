# Apocalypse Countdown Service

A whimsical Dockerized HTTP service that tells you how many days are left until the next apocalypse. Each request returns a random number (0‑1000) with a playful message.

## Build

```sh
docker build -t apocalypse-countdown .
```

## Run

```sh
docker run -p 8080:8080 apocalypse-countdown
```

## Use

```sh
curl http://localhost:8080/countdown
# {"days":123,"message":"The world ends in 123 days!"}
```

## How it works

The service is written in Go. It seeds the random number generator with the current time, unless the environment variable `FIXED_SEED` is set (useful for testing).
