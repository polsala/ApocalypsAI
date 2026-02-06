# nightly-docker-portal-gateway

A whimsical Docker container that opens a portal to a random location in the post‑apocalyptic multiverse. When run, it prints an ASCII portal and a destination phrase. You can also specify a custom destination via the `DESTINATION` environment variable for scripting or testing.

## Build

```sh
docker build -t portal-gateway .
```

## Run

```sh
docker run --rm portal-gateway
```

Or with a custom destination:

```sh
docker run --rm -e DESTINATION="The Silent Library" portal-gateway
```

## How it works

The container runs a tiny Bash script that selects a random destination from an internal list unless `DESTINATION` is set.
