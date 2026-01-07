# nightly-docker-emoji-clock

A tiny Docker container that prints the current time using expressive clock emojis.

## Build

```sh
docker build -t emoji-clock .
```

## Run

```sh
docker run --rm emoji-clock
```

You can override the displayed time with the `TIME_OVERRIDE` environment variable (format HH:MM):

```sh
docker run --rm -e TIME_OVERRIDE=23:45 emoji-clock
```

## How it works

The container runs a Bash script that determines the hour (from the system clock or the override) and selects the matching Unicode clock emoji.
