# nightly-docker-quote-espresso

**What it does**

A tiny Go web server packaged in a Docker image that returns a random coffee‑themed inspirational quote on each request to `GET /quote`.  Perfect for a quick morale boost on a post‑apocalyptic terminal.

**Features**

- Zero external dependencies – all quotes are baked into the binary.
- Multi‑stage Docker build (tiny final image ~5 MB).
- Deterministic unit‑style test that builds the image, runs it, and validates the response.

**Build the image**

```bash
docker build -t quote-espresso ./docker-tools/nightly-docker-quote-espresso
```

**Run the container**

```bash
# Expose port 8080 on the host
docker run -d --name quote-espresso -p 8080:8080 quote-espresso
```

**Get a quote**

```bash
curl http://localhost:8080/quote
```

You should see a JSON payload, e.g.:

```json
{"quote":"Coffee is the gasoline of the soul."}
```

**Run the tests**

```bash
cd docker-tools/nightly-docker-quote-espresso/tests
bash test.sh
```

The script builds the image, starts a container, fetches a quote, verifies it matches one of the known quotes, and then cleans up.
