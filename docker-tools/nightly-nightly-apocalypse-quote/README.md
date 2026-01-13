Nightly Apocalypse Quote
========================

This utility provides a daily apocalypse-themed quote. It can be used as a CLI or as a Dockerized HTTP service.

Usage
-----

### CLI

```bash
python src/main.py --quote
```

### Docker

```bash
docker build -t nightly-apocalypse-quote .
docker run --rm -p 8080:8080 nightly-apocalypse-quote
```

The service will expose `http://localhost:8080/quote` returning a JSON payload:

```json
{ \"date\": \"2025-12-09\", \"quote\": \"...\" }
```

