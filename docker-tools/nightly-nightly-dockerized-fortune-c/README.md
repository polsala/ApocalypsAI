# Nightly Dockerized Fortune Cookie

## Overview

`nightly-dockerized-fortune-cookie` is a minimal Docker image that prints a whimsical fortune‑cookie style message when executed.  It is perfect for adding a splash of post‑apocalyptic optimism to CI logs, terminal sessions, or any automated workflow.

## Build the Image

```sh
docker build -t nightly-fortune-cookie .
```

## Run the Container

```sh
docker run --rm nightly-fortune-cookie
```

Each invocation prints one of several pre‑written fortunes.  The message selection is deterministic when the environment variable `SEED` is set, which makes testing easy.

## Custom Seed

You can control the output by providing a numeric seed:

```sh
SEED=42 docker run --rm -e SEED=42 nightly-fortune-cookie
```

## License

MIT © ApocalypsAI
