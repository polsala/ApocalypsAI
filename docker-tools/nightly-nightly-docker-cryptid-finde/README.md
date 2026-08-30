# nightly-docker-cryptid-finder

A tiny Rust‑based command‑line tool packaged as a Docker image.  Given a location keyword (e.g. `forest`, `desert`, `mountain`, `swamp`, `urban`) it returns a cryptid that fits the environment.  The selection is deterministic – it hashes the location string, so the same input always yields the same cryptid.  Perfect for adding a splash of mythic flavor to your post‑apocalyptic narratives.

## Build the Docker image
```bash
docker build -t cryptid-finder .
```

## Run the container
```bash
# Replace <location> with your keyword
docker run --rm cryptid-finder <location>
```
Example:
```bash
docker run --rm cryptid-finder forest
# => "The Wendigo"
```

## How it works
1. The Rust library (`src/lib.rs`) contains a static list of cryptids paired with habitat tags.
2. `get_cryptid` hashes the supplied location string, picks an index modulo the list length, and returns the matching cryptid.
3. The binary (`src/main.rs`) simply forwards the first CLI argument to `get_cryptid` and prints the result.
4. Tests (`tests/cryptid_test.rs`) verify deterministic output for a few sample locations.

## License
MIT © ApocalypsAI
