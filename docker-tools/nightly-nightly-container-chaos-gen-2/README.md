## nightly-container-chaos-gen

This utility generates whimsical yet functional `docker-compose.yml` files designed to introduce controlled chaos into your development or testing environments. It's perfect for simulating unpredictable network conditions, resource contention, or simply creating a fun, dynamic setup for your applications.

### Philosophy

Embrace the delightful unpredictability of the digital apocalypse! This tool helps you prepare for the unexpected by building environments that are just as chaotic as the world outside.

### Usage

1.  **Build the Docker image:**
    ```bash
    docker build -t container-chaos-gen .
    ```

2.  **Run the generator:**
    The tool takes a few optional arguments to customize the chaos.

    *   `--services <count>`: Number of services to include (default: 3).
    *   `--network-latency <ms>`: Base network latency to introduce (default: 50).
    *   `--network-loss <percent>`: Packet loss percentage (default: 5).
    *   `--resource-cpu <cores>`: CPU cores to allocate per service (default: 0.5).
    *   `--resource-memory <mb>`: Memory to allocate per service (default: 128).
    *   `--output <filename>`: Output file name (default: docker-compose.yml).

    **Example:** Generate a compose file with 5 services, 100ms latency, 10% packet loss, and 1 CPU core per service:
    ```bash
    docker run --rm container-chaos-gen --services 5 --network-latency 100 --network-loss 10 --resource-cpu 1 --output chaotic-dev.yml
    ```

3.  **Use the generated `docker-compose.yml`:**
    Once generated, you can use it with Docker Compose:
    ```bash
    docker compose -f <generated-file>.yml up -d
    ```

### How it Works

The generator creates a `docker-compose.yml` file. For each service, it adds a `network_mode: "service:<service_name>"` and a `depends_on` relationship to a dedicated "chaos" service. This "chaos" service uses `network_mode: "service:main_service"` and applies `tc` (traffic control) commands within its container to manipulate the network and resource allocation for the main service it's attached to. This creates a layered chaos effect.

### Testing

Tests are included to verify the structure and content of the generated `docker-compose.yml` file. They mock the generation logic and assert on the output.
