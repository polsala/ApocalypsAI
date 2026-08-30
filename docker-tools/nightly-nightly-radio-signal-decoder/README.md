# Nightly Radio Signal Decoder

Utility to decode base64‑encoded "radio signals" inside a tiny Docker container. Perfect for post‑apocalyptic comms or just for fun.

## Usage

```bash
# Build the image (once)
docker build -t radio-decoder .

# Decode a signal (provide base64 via the SIGNAL env var)
# Example: "Hello world" => SGVsbG8gd29ybGQ=

docker run --rm -e SIGNAL=SGVsbG8gd29ybGQ= radio-decoder
```

The container will output something like:

```
🔊 Decoded signal: Hello world
```

If the `SIGNAL` variable is missing or not valid base64, the program will emit an error message and exit with a non‑zero status.

## Testing

Run the provided test script:

```bash
chmod +x tests/test_docker.sh
./tests/test_docker.sh
```

All tests should pass on any system with Docker installed.
