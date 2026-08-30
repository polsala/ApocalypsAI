# Nightly Docker Chrono-Compressor

A whimsical yet powerful containerized utility to temporarily throttle CPU or I/O resources for a target Docker container. This tool is designed to help engineers simulate resource scarcity, stress-test applications, and observe their resilience under constrained conditions, all with a touch of temporal flair!

## Features

*   **CPU Throttling**: Reduce a container's allocated CPU shares.
*   **I/O Throttling**: Limit a container's block I/O weight.
*   **Temporary Application**: Throttling is applied for a specified duration and then automatically restored to original values.
*   **Containerized**: Runs as a Docker container, requiring only Docker daemon access.

## How it Works

The Chrono-Compressor leverages Docker's built-in resource control mechanisms (`--cpu-shares` and `--blkio-weight`) to temporarily adjust a running container's resource limits. It first inspects the target container to retrieve its current resource settings, applies the "compression" (throttling), waits for the specified duration, and then restores the original settings.

## Usage

### 1. Build the Docker Image

First, build the `nightly-docker-chrono-compressor` Docker image:

```bash
docker build -t nightly-docker-chrono-compressor .
```

### 2. Run the Chrono-Compressor

To use the utility, you need to run its container with access to the Docker daemon socket (`/var/run/docker.sock`). This allows the Chrono-Compressor to interact with other containers on your host.

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  nightly-docker-chrono-compressor <target_container> <resource_type> <value> <duration_seconds>
```

**Arguments**:

*   `<target_container>`: The name or ID of the Docker container you wish to throttle.
*   `<resource_type>`: The type of resource to compress. Choose `cpu` or `io`.
*   `<value>`:
    *   For `cpu`: An integer representing CPU shares (e.g., `100`). Docker's default is `1024`. A lower value means the container gets a smaller proportion of available CPU cycles.
    *   For `io`: An integer representing block I/O weight (e.g., `100`). Docker's default is `500`. A lower value means the container gets less I/O bandwidth.
*   `<duration_seconds>`: An integer specifying how long (in seconds) the throttling should be applied.

### Examples

#### Example 1: Throttle CPU

Throttle a container named `my-web-app` to 100 CPU shares for 30 seconds:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  nightly-docker-chrono-compressor my-web-app cpu 100 30
```

#### Example 2: Throttle I/O

Throttle a container named `data-processor` to 50 I/O weight for 60 seconds:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  nightly-docker-chrono-compressor data-processor io 50 60
```

## Development and Testing

### Automated Tests

The tests for this utility are written in Bash and use a mocked `docker` command to ensure determinism and offline execution.

To run the tests:

```bash
bash tests/test_chrono_compressor.sh
```

### Mock Rationale

The `docker` command is an external dependency that interacts directly with the Docker daemon. For robust, deterministic, and offline testing, its behavior is mocked within `tests/test_chrono_compressor.sh`. This mock captures all arguments passed to `docker` and simulates its output (e.g., for `docker inspect` or `docker update`), allowing the test suite to verify that `chrono_compressor.sh` constructs and executes the correct Docker commands without requiring a live Docker environment. The `sleep` command is also mocked to speed up test execution.
