# nightly-cryptic-quote-docker

**What it does**

A whimsical, self‑contained Docker image that prints a random cryptic quote about the apocalypse (or any other mysterious event) each time you run it. Perfect for a quick morale boost in CI logs, terminal splash screens, or just for fun.

**How it works**

The image is built from a tiny Go program that selects a quote from an internal list using a pseudo‑random generator. The binary is compiled statically in a multi‑stage Docker build, so the final image is only ~5 MB.

**Usage**

```bash
# Pull the image (once it is published) or build locally
docker build -t nightly-cryptic-quote .

# Run the container – it will print a single quote and exit
docker run --rm nightly-cryptic-quote
```

**Example output**

```
When the last candle flickers, the shadows will write the next chapter.
```

**Development**

The source lives under `src/`. To run the program locally without Docker:

```bash
cd src
go run .
```

**Testing**

The repository includes deterministic unit tests under `tests/`. Run them with:

```bash
go test ./...
```

The tests seed the random number generator to guarantee repeatable output.
