# nightly-docker-survival-tip-api

A tiny Docker container that serves a random post‑apocalyptic survival tip at `http://localhost:8080/tip`. Each request returns JSON:

```json
{"tip":"..."}
```

## Build

```sh
docker build -t survival-tip-api .
```

## Run

```sh
docker run -p 8080:8080 survival-tip-api
```

## Example

```sh
curl http://localhost:8080/tip
# {"tip":"Always keep a spare can of beans in your backpack."}
```
