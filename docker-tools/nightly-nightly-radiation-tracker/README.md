# nightly-radiation-tracker

A lightweight Dockerized Flask API that records and reports radiation level readings for post‑apocalyptic settlements.

## Features

- `POST /reading` – submit a radiation reading (JSON `{ "value": <float> }`).
- `GET /average` – retrieve the average of all submitted readings.

## Running with Docker

```sh
docker build -t radiation-tracker .
docker run -p 5000:5000 radiation-tracker
```

## API Example

```sh
curl -X POST -H "Content-Type: application/json" -d '{"value": 3.7}' http://localhost:5000/reading
curl http://localhost:5000/average
```

## Testing

```sh
pip install pytest
pytest -q
```
