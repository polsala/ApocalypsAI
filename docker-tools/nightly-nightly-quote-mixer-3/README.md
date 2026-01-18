# Quote Mixer Docker Service

A whimsical Dockerized HTTP service that returns a randomly blended quote from an inspirational list and an apocalyptic list.

## Usage

```sh
docker build -t quote-mixer .
docker run -p 8080:8080 quote-mixer
```

Then request a quote:

```sh
curl http://localhost:8080/quote
```

Response:

```json
{"quote":"..."}
```

## How it works

The service picks one quote from each list and concatenates them, delivering a fresh, quirky mash‑up each time you call `/quote`.
