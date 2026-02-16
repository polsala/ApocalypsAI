# Whimsy Quote Docker Server

A tiny Dockerized HTTP server that serves a random whimsical quote on each request.

## Build

```sh
docker build -t whimsy-quote .
```

## Run

```sh
docker run -p 8080:8080 whimsy-quote
```

## Use

```sh
curl http://localhost:8080/
```

Will return JSON like:

```json
{"quote":"..."}
```
