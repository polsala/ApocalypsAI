# Nightly Digital Bugout Bag

Ever feel like your essential digital tools are scattered across different machines, or you're stuck on a fresh system without your favorite CLI utilities? The `nightly-digital-bugout-bag` is here to help!

This utility generates a Docker-Compose setup that creates a portable, self-contained "digital bugout bag" – a containerized environment pre-loaded with your chosen command-line tools. Just build it once, and you can carry your personalized toolkit wherever Docker runs.

## Features

*   **Customizable Tools**: Specify a list of common CLI tools (e.g., `git`, `jq`, `curl`, `vim`, `python3`, `node`).
*   **Portable Environment**: Generates a `Dockerfile` and `docker-compose.yml` to encapsulate your tools.
*   **Persistent Data**: Automatically sets up a volume for any data you create inside the bag.
*   **Easy Access**: Provides a simple script to build and enter your digital sanctuary.

## Usage

1.  **Run the generator**:
    ```bash
    ./src/generate_bag.sh [OPTIONS]
    ```

    **Options**:
    *   `-t <tools>`: Comma-separated list of tools to include (e.g., `git,jq,curl,vim`).
    *   `-n <name>`: Name for your bugout bag (default: `my-digital-bag`).
    *   `-o <output_dir>`: Output directory for the generated files (default: `./my-digital-bag`).
    *   `-h`: Display help message.

    **Example**:
    ```bash
    ./src/generate_bag.sh -t "git,jq,curl,python3" -n "dev-bag" -o "./dev-bag-project"
    ```

2.  **Navigate to your generated bag directory**:
    ```bash
    cd ./dev-bag-project
    ```

3.  **Build and run your bag**:
    ```bash
    ./run_bag.sh
    ```
    This script will build the Docker image and then drop you into a shell inside your container.

## Generated Files

The generator will create a directory (e.g., `my-digital-bag`) containing:

*   `Dockerfile`: Defines the container image with your specified tools.
*   `docker-compose.yml`: Orchestrates the container, setting up volumes and services.
*   `run_bag.sh`: A convenience script to build the image and start a shell session in the container.
*   `README.md`: A basic README for your specific bag.

## Example `Dockerfile` (simplified)

```dockerfile
FROM alpine/git:latest

# Install specified tools
RUN apk add --no-cache git jq curl python3

WORKDIR /app

CMD ["/bin/bash"]
```

## Example `docker-compose.yml` (simplified)

```yaml
version: '3.8'
services:
  my-digital-bag:
    build: .
    volumes:
      - ./data:/app/data # Persistent storage for your bag's contents
    stdin_open: true # Keep stdin open even if not attached
    tty: true        # Allocate a pseudo-TTY
```

## Development & Testing

See `tests/test_generate_bag.sh` for how the generator is tested.
