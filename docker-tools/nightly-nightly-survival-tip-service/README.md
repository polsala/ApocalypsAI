# Survival Tip Service

A whimsical Dockerized Flask API that provides a random survival tip for a given scenario.

## Usage

Build the image:

```bash
docker build -t survival-tip-service .
```

Run the container:

```bash
docker run -p 5000:5000 survival-tip-service
```

## API

`GET /tip?scenario=...` returns JSON:

```json
{
  "tip": "Always keep a spare bottle of water.",
  "scenario": "rainy day"
}
```

## Example

```bash
curl "http://localhost:5000/tip?scenario=rainy%20day"
```

Will return a tip.
