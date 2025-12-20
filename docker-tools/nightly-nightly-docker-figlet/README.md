# nightly-docker-figlet

A tiny Dockerized CLI that turns text into ASCII art using Figlet.

## Usage

```sh
# Build the Docker image
docker build -t nightly-docker-figlet .

# Run the container with the text you want to render
docker run --rm nightly-docker-figlet "Hello World"
```

Or run locally without Docker:

```sh
python src/main.py "Hello World"
```

## How it works

The utility uses the `pyfiglet` library to render text in Figlet style. The Docker image is based on `python:3.11-slim` and installs only the required dependency.

## Testing

Run the tests with:

```sh
python -m unittest discover -s tests
```
