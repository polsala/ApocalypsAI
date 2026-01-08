# Dockerized Quote of the Day Server

A tiny Flask web server that returns a random inspirational quote on each request. Packaged as a Docker image for easy deployment.

## Build

```sh
docker build -t quote-server .
```

## Run

```sh
docker run -p 8080:8080 quote-server
```

## Use

```sh
curl http://localhost:8080/
```

Will return a plain‑text quote.
