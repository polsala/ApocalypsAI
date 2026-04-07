# nightly-docker-ghost-haiku

A whimsical Docker container that reads any text from stdin and returns a post‑apocalyptic haiku. The haiku is chosen deterministically by hashing the input, so the same input always yields the same poem.

## Build

```sh
docker build -t ghost-haiku .
```

## Run

```sh
echo "your prompt" | docker run -i ghost-haiku
```

Example:

```sh
echo "test" | docker run -i ghost-haiku
```

Outputs:

```
Moonlight cracks the stone
Shadows dance on cracked glass
Tomorrow sings soft
```

## How it works

The Go program reads stdin, sums the byte values, takes the remainder modulo the number of haikus, and prints the selected haiku.
