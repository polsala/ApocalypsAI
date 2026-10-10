# Nightly Chrono-Container Gardener

## Summary

The `nightly-chrono-container-gardener` is a whimsical-yet-useful utility designed to help you manage ephemeral Docker development environments. Think of it as your personal digital gardener: it "plants" (spins up) a containerized environment for a specific task or duration, nurtures it, and then "prunes" (stops and removes) it automatically. This ensures a clean slate for each development cycle, testing session, or quick experiment, preventing container sprawl and resource exhaustion.

## Features

*   **Ephemeral Environments**: Easily launch temporary Docker Compose-based environments.
*   **Time-Based Pruning**: Automatically shuts down and removes containers after a specified duration.
*   **Clean Slate**: Guarantees a fresh environment for every use.
*   **Whimsical Output**: Enjoy gardening-themed messages as your containers are managed.

## Usage

1.  **Prepare your `docker-compose.yml`**: Create or locate a `docker-compose.yml` file that defines your desired development environment. An example is provided in `src/docker-compose.example.yml`.

2.  **Run the Gardener**: Execute the `chrono-gardener.sh` script with the path to your Docker Compose file and the desired duration.

    ```bash
    ./src/chrono-gardener.sh --compose-file /path/to/your/docker-compose.yml --duration <minutes> [--project-name <name>]
    ```

    *   `--compose-file <path>`: **Required**. Path to your `docker-compose.yml` file.
    *   `--duration <minutes>`: **Required**. The number of minutes the environment should run before being pruned. (e.g., `30` for 30 minutes).
    *   `--project-name <name>`: **Optional**. A custom project name for your Docker Compose environment. If not provided, a default name will be generated based on the directory name and a timestamp.

### Example:

Let's say you have a `my-dev-env/docker-compose.yml` and `my-dev-env/nginx.conf`:

```yaml
# my-dev-env/docker-compose.yml
version: '3.8'
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: mydatabase
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
```

To run this environment for 15 minutes:

```bash
./src/chrono-gardener.sh --compose-file my-dev-env/docker-compose.yml --duration 15 --project-name my-ephemeral-project
```

## Development & Testing

To run the tests, navigate to the utility's directory and execute:

```bash
./tests/test_chrono-gardener.sh
```

The tests use mocks for `docker-compose` and `sleep` to ensure deterministic and fast execution without actual Docker operations or time delays.
