# nightly-docker-rot13

A tiny Dockerized ROT13 encoder. Pass a string as an argument or pipe input to get the ROT13 transformation.

## Usage

```bash
docker run --rm polsala/nightly-docker-rot13 "Hello, World!"
# Output: Uryyb, Jbeyq!
```

You can also pipe input:

```bash
echo "Hello" | docker run --rm polsala/nightly-docker-rot13
# Output: Uryyb
```

## Build

```bash
docker build -t polsala/nightly-docker-rot13 .
```

## Test

Run the included tests:

```bash
bash tests/test_run.sh
```
