# nightly-docker-emoji-logger

A Dockerized CLI that logs a whimsical emoji message based on an environment variable.

## Usage

```bash
docker build -t nightly-docker-emoji-logger .
docker run -e EMOJI=🚀 nightly-docker-emoji-logger
```

If `EMOJI` is not set, it defaults to 😃.

## Example

```bash
$ docker run nightly-docker-emoji-logger
Logging: 😃
```
