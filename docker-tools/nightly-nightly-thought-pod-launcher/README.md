# Nightly Ephemeral Thought-Pod Launcher

## 🧐 What is the Thought-Pod?

In the chaotic expanse of the post-apocalyptic digital wasteland, sometimes you just need a quiet, isolated corner to gather your thoughts, jot down a brilliant survival strategy, or prototype a quick web component without the clutter of your main system. The `nightly-thought-pod-launcher` is your personal, ephemeral sanctuary: a lightweight, containerized web server that springs to life with a simple command, offering a dedicated space for your digital musings.

It's perfect for:
*   **Quick Notes & Ideas:** Drop `.txt`, `.md`, or `.html` files into the `src/thoughts/` directory and access them instantly via your browser.
*   **Static Site Prototyping:** Test a small HTML/CSS/JS snippet in an isolated environment.
*   **Temporary File Sharing:** Need to quickly serve a file to another local machine or a specific application? The Thought-Pod has you covered.
*   **Focus & Isolation:** A dedicated browser tab for your current task, free from other development distractions.

## 🚀 Getting Started

This utility uses Docker Compose to orchestrate a simple Nginx web server.

### Prerequisites

*   [Docker](https://docs.docker.com/get-docker/) installed and running on your system.

### Usage

1.  **Navigate to the utility directory:**
    ```bash
    cd docker-tools/nightly-thought-pod-launcher
    ```

2.  **Launch your Thought-Pod:**
    This command will build the Nginx image (if not already built) and start the web server in the background.
    ```bash
    docker compose up -d
    ```

3.  **Enter your Thought-Pod:**
    Open your web browser and navigate to:
    ```
    http://localhost:8080
    ```
    You should see the default `index.html` content.

4.  **Add your thoughts:**
    Any files you place inside the `src/thoughts/` directory will be served by the Nginx web server. For example, create `src/thoughts/my-brilliant-idea.html`:
    ```html
    <!-- src/thoughts/my-brilliant-idea.html -->
    <h1>My Brilliant Idea!</h1>
    <p>We should build a giant, self-sustaining hamster wheel powered by existential dread.</p>
    ```
    Then, access it in your browser:
    ```
    http://localhost:8080/my-brilliant-idea.html
    ```

5.  **Exit your Thought-Pod:**
    When you're done, stop and remove the container and its associated network:
    ```bash
    docker compose down
    ```

## 🛠️ Technical Details

*   **Service:** `thought-pod` (Nginx web server)
*   **Port:** Exposed on `8080` on your host, mapping to port `80` inside the container.
*   **Volume:** The `src/thoughts/` directory on your host is mounted into the Nginx web root (`/usr/share/nginx/html`) inside the container. This means changes to files in `src/thoughts/` are immediately reflected in the web server.
*   **Network:** A dedicated Docker network `nightly-thought-pod-network` is created for isolation.

## ⚠️ Important Notes

*   The Thought-Pod is ephemeral. While your `src/thoughts/` content persists on your host, the container itself is removed when you run `docker compose down`. Any changes made *inside* the container (e.g., installing software) will be lost.
*   This is a basic web server. For more complex applications or production use, consider more robust solutions.
