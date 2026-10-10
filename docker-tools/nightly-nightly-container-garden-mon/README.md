# ApocalypsAI Nightly Container Garden Monitor

A whimsical Dockerized dashboard that visualizes the "health" and "mood" of your running containers as a digital garden, helping you quickly spot issues.

## 🌻 Overview

The Container Garden Monitor transforms your mundane Docker containers into a vibrant (or sometimes wilting) digital garden. Each container is represented as a "plant" card, displaying its status with a colorful emoji and inferring its "mood" from recent logs. This provides an at-a-glance, fun way to keep an eye on your container ecosystem.

## ✨ Features

*   **Container-as-Plant Visualization**: Each running or stopped container gets its own "plant card".
*   **Whimsical Mood Detection**: Analyzes recent container logs to assign a mood (Vibrant 🌿, Droopy 💧, Wilting 🥀, Sprouting 🌱, Content 🌼).
*   **Status Emojis**: Clear visual cues for container status (Running 🟢, Exited 🔴, Paused ⏸️, Restarting 🔄).
*   **Real-time Updates**: Automatically refreshes container data every 10 seconds.
*   **Self-contained Docker Image**: Easy to deploy and run alongside your other containers.

## 🚀 How to Use

1.  **Build the Docker Image (Optional, if you want to modify):**
    ```bash
    docker build -t container-garden-monitor .
    ```

2.  **Run the Container Garden Monitor:**
    The monitor needs access to the Docker daemon to list and inspect other containers. This is typically done by mounting the `/var/run/docker.sock` into the monitor's container.

    ```bash
    docker run -d \
      --name container-garden-monitor \
      -p 5000:5000 \
      -v /var/run/docker.sock:/var/run/docker.sock \
      container-garden-monitor
    ```
    *   `-d`: Runs the container in detached mode (in the background).
    *   `--name container-garden-monitor`: Assigns a memorable name to the monitor container.
    *   `-p 5000:5000`: Maps port 5000 of your host to port 5000 inside the container, where the web UI runs.
    *   `-v /var/run/docker.sock:/var/run/docker.sock`: **Crucial!** This mounts the Docker daemon's Unix socket into the container, allowing the monitor to communicate with the Docker API.

3.  **Access the Dashboard:**
    Open your web browser and navigate to `http://localhost:5000`. You should see your container garden!

## 🛠️ Development & Testing

### Prerequisites

*   Python 3.9+
*   `pip`
*   `docker` SDK for Python (installed via `requirements.txt`)
*   `Flask` (installed via `requirements.txt`)

### Local Development

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Flask application:**
    ```bash
    python src/app.py
    ```
    Then open `http://localhost:5000` in your browser.

### Running Tests

Tests are written using `unittest` and `unittest.mock` to ensure they are deterministic and do not require a running Docker daemon.

```bash
python -m unittest tests/test_app.py
```

The tests mock the `docker.from_env()` client and container objects, as well as their `logs()` method, to simulate various container states and log outputs.

## 📜 License

This project is licensed under the MIT License.
