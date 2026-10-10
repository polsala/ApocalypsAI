# Nightly Zen Garden in a Box

## 🌌 A Pocket of Peace in the Digital Wasteland 🌌

This utility provides a self-contained, containerized web server that hosts a simple, calming 'Zen Garden'. Spin it up whenever you need a moment of digital tranquility, a visual breathing exercise, or just a peaceful background presence amidst the chaos of the apocalypse (or your daily dev cycle).

It's designed to be lightweight and easy to deploy, demonstrating the power of Docker for even the simplest, most whimsical applications.

## ✨ Features

*   **Containerized Serenity**: Runs entirely within a Docker container, ensuring isolation and easy setup.
*   **Minimalist Design**: A simple HTML page with a CSS-animated 'breathing sphere' for visual meditation.
*   **Instant Calm**: Accessible via your web browser for a quick escape.
*   **Lightweight**: Built on a tiny Nginx Alpine image.

## 🚀 How to Use

### Prerequisites

Make sure you have Docker installed and running on your system.

### 1. Build the Docker Image

Navigate to the `nightly-zen-garden-in-a-box` directory and build the Docker image:

```bash
docker build -t nightly-zen-garden .
```

### 2. Run the Container

Once the image is built, you can run the container. This will map port `8080` on your host machine to port `80` inside the container (where Nginx serves the content):

```bash
docker run -d -p 8080:80 --name zen-garden-container nightly-zen-garden
```

*   `-d`: Runs the container in detached mode (in the background).
*   `-p 8080:80`: Maps host port 8080 to container port 80.
*   `--name zen-garden-container`: Assigns a memorable name to your container.

### 3. Access Your Zen Garden

Open your web browser and navigate to:

```
http://localhost:8080
```

You should see your Nightly Zen Garden!

### 4. Stop and Remove the Container (When Peace is Achieved)

When you're done with your moment of tranquility, you can stop and remove the container:

```bash
docker stop zen-garden-container
docker rm zen-garden-container
```

To also remove the Docker image:

```bash
docker rmi nightly-zen-garden
```

## 🧪 Automated Tests

This utility includes shell scripts to verify the Docker image can be built and the container can be run successfully.

To run the tests, ensure you have Docker installed and navigate to the utility's root directory:

```bash
bash tests/test_docker_build.sh
bash tests/test_docker_run.sh
```

Both scripts should exit with a status code of `0` for success.

## 🛠️ Development Notes

*   The web content is served by a lightweight Nginx server within the container.
*   The 'breathing sphere' is a simple CSS animation, demonstrating basic web content delivery.
