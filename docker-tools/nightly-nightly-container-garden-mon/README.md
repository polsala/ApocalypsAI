# Nightly Container Garden Monitor 🌻

A whimsical Docker-based utility that monitors the health and resource usage of your other Docker containers, presenting them as "plants" in a vibrant "container garden" with emoji-rich reports.

Each container is a unique "plant" in your digital ecosystem, and its vital signs are translated into garden metaphors:
- **CPU Usage**: Your plant's "Sunlight" ☀️
- **Memory Usage**: Your plant's "Water" 💧
- **Disk I/O**: Your plant's "Soil Nutrients" 🪱
- **Network Activity**: Your plant's "Pollination" 🐝

Keep an eye on your garden to ensure all your digital flora are thriving!

## 🚀 Usage

To run the Container Garden Monitor, you need to mount your Docker daemon's socket into the monitor container. This allows the monitor to access information about other running containers.

1.  **Build the Docker image (optional, or use a pre-built one if available):**
    ```bash
    docker build -t apocalypsai-garden-monitor .
    ```

2.  **Run the monitor container:**
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai-garden-monitor
    ```
    -   `--rm`: Automatically remove the container when it exits.
    -   `-v /var/run/docker.sock:/var/run/docker.sock`: Mounts the Docker daemon socket, giving the monitor access to other containers. **This is crucial for the utility to function.**

### Example Output

```
--- ApocalypsAI Container Garden Report ---
Report generated: 2023-10-27 10:00:00

🌱 my-web-app (Thriving)
  Sunlight: 50.00% CPU
  Water: 9.77% MEM (100.00MB)
  Soil Nutrients: R:0.00MB W:0.00MB
  Pollination: RX:0.95MB TX:0.48MB

💧 my-db (Parched)
  Sunlight: 50.00% CPU
  Water: 92.77% MEM (950.00MB)
  Soil Nutrients: R:0.00MB W:0.00MB
  Pollination: RX:0.95MB TX:0.48MB

☀️ high-cpu-worker (Sun-scorched)
  Sunlight: 950.00% CPU
  Water: 9.77% MEM (100.00MB)
  Soil Nutrients: R:0.00MB W:0.00MB
  Pollination: RX:0.95MB TX:0.48MB

🪱 data-processor (Soil-churning)
  Sunlight: 50.00% CPU
  Water: 9.77% MEM (100.00MB)
  Soil Nutrients: R:120.00MB W:10.00MB
  Pollination: RX:0.95MB TX:0.48MB

🐝 api-gateway (Buzzing with Pollinators)
  Sunlight: 50.00% CPU
  Water: 9.77% MEM (100.00MB)
  Soil Nutrients: R:0.00MB W:0.00MB
  Pollination: RX:15.00MB TX:10.00MB

🥀 failed-container (Wilted (No Data))
  Sunlight: N/A
  Water: N/A
  Soil Nutrients: N/A
  Pollination: N/A

-------------------------------------------
```

## 🛠️ Development and Testing

### Prerequisites

-   Docker
-   Python 3.9+
-   `pip install docker` (for local testing/development)

### Running Tests

To run the automated tests, navigate to the utility's directory and execute:

```bash
python -m unittest tests/test_monitor.py
```

The tests use `unittest.mock` to simulate Docker API responses, ensuring deterministic and offline testing.

### Local Development

You can run the `monitor.py` script directly if you have `docker-py` installed and access to the Docker socket:

```bash
python src/monitor.py
```
(This will likely fail unless you set DOCKER_HOST or similar, or run it inside a container with the socket mounted).
The primary way to use this utility is via its Docker container.

## ⚠️ Important Note on Docker Socket

Mounting `/var/run/docker.sock` gives the container the same level of access as the Docker daemon itself. Be cautious when using this in production environments or with untrusted images, as it can pose a security risk. This utility is designed for monitoring and does not perform any destructive actions.
