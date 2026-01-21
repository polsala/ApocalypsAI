# nightly-docker-size-estimator

Estimates the compressed size (in MB) of a Docker Hub image tag without pulling the image.

## Usage

```sh
# Build the Docker image
docker build -t docker-size-estimator .

# Run the estimator (replace <image>[:tag] with the desired image)
docker run --rm docker-size-estimator <image>[:tag]
```

If no tag is provided, `latest` is assumed.

## How it works

The tool queries the Docker Hub Registry HTTP API v2 for the manifest metadata of the requested tag and extracts the `full_size` field, which represents the compressed size in bytes. The size is then converted to megabytes and printed.

## Testing

Run the unit tests with:

```sh
# Build the image (if not already built)
docker build -t docker-size-estimator .

# Execute the tests inside the container
docker run --rm docker-size-estimator pytest
```

(Or run locally with `pytest` after installing the requirements.)
