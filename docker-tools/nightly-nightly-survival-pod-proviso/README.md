# Nightly Survival Pod Provisor

## Overview

The `nightly-survival-pod-provisor` is a whimsical-yet-useful containerized utility designed to help the community manage their "survival pods" (Docker Compose applications) in the post-apocalyptic landscape. It ensures your pods are properly provisioned by validating and generating `docker-compose.yml` files from Jinja2 blueprints and JSON/YAML manifests.

Think of it as your personal pod architect, making sure your critical services (web servers, databases, communication relays) are always built to spec, even when resources are scarce and documentation is fragmented.

## Features

*   **Blueprint Templating**: Uses Jinja2 to render flexible `docker-compose.yml` blueprints.
*   **Manifest-driven Configuration**: Injects dynamic values from JSON or YAML manifests into your blueprints.
*   **Basic Validation**: Performs sanity checks on the generated `docker-compose.yml` to ensure essential sections are present.
*   **Containerized**: Runs as a self-contained Docker image, ensuring consistent execution across different environments.

## Usage

1.  **Build the Provisor Image**:
    ```bash
    docker build -t nightly-survival-pod-provisor .
    ```

2.  **Prepare your Blueprint and Manifest**:
    *   **Blueprint**: A Jinja2-templated `docker-compose.yml` file (e.g., `src/blueprints/basic_pod.yml`).
    *   **Manifest**: A JSON or YAML file containing the variables to inject into the blueprint (e.g., `src/manifests/example_manifest.json`).

3.  **Run the Provisor**:
    Mount your blueprint and manifest files into the container and specify their paths.
    ```bash
    docker run --rm \
      -v "$(pwd)/src/blueprints/basic_pod.yml:/app/blueprint.yml" \
      -v "$(pwd)/src/manifests/example_manifest.json:/app/manifest.json" \
      nightly-survival-pod-provisor \
      python /app/app.py --blueprint /app/blueprint.yml --manifest /app/manifest.json > generated-docker-compose.yml
    ```
    This command will output the generated `docker-compose.yml` to `stdout`, which you can redirect to a file.

    **Example with custom paths (assuming you copy them to the current directory)**:
    ```bash
    cp src/blueprints/basic_pod.yml my_web_pod.yml.j2
    cp src/manifests/example_manifest.json my_web_pod_config.json

    docker run --rm \
      -v "$(pwd)/my_web_pod.yml.j2:/app/blueprint.yml" \
      -v "$(pwd)/my_web_pod_config.json:/app/manifest.json" \
      nightly-survival-pod-provisor \
      python /app/app.py --blueprint /app/blueprint.yml --manifest /app/manifest.json > my_web_pod_compose.yml
    ```

4.  **Deploy your Survival Pod**:
    ```bash
    docker compose -f generated-docker-compose.yml up -d
    ```

## Development and Testing

### Local Testing (Python Logic)

To test the core Python logic without Docker:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/test_app.py
```

### Docker Build Test

To verify the Docker image builds correctly:

```bash
bash tests/test_docker_build.sh
```

## Files

*   `README.md`: This documentation.
*   `Dockerfile`: Defines the container image for the Provisor.
*   `src/app.py`: The Python script that handles templating and validation.
*   `src/blueprints/basic_pod.yml`: An example Jinja2-templated Docker Compose blueprint.
*   `src/manifests/example_manifest.json`: An example JSON manifest with configuration variables.
*   `requirements.txt`: Python dependencies for `app.py`.
*   `tests/test_app.py`: Unit tests for `src/app.py`.
*   `tests/test_docker_build.sh`: Script to test the Docker image build process.
