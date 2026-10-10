# Nightly Broadcast Beacon

A containerized web server designed to broadcast pre-recorded messages, survival tips, or ambient sounds to a local network. Think of it as your personal, resilient post-apocalyptic radio station, ready to deliver vital (or whimsical) information to your community.

## Features

*   **Static File Serving**: Easily serve text messages, audio files, or any other static content.
*   **Containerized**: Runs in an isolated Docker container, making it portable and easy to deploy.
*   **Simple Web Interface**: A basic web page lists available broadcasts, and each can be accessed directly.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-broadcast-beacon` directory and build the Docker image:

```bash
docker build -t nightly-broadcast-beacon .
```

### 2. Run the Container

Run the container, mapping a local port (e.g., 8080) to the container's exposed port (8080):

```bash
docker run -p 8080:8080 --name broadcast-beacon-instance nightly-broadcast-beacon
```

The beacon will now be accessible at `http://localhost:8080`.

### 3. Access Broadcasts

Open your web browser and navigate to `http://localhost:8080`. You will see a list of available broadcasts. Click on a link to view/listen to a specific broadcast.

### 4. Customize Broadcast Content

To add your own messages or sounds:

1.  Place your files (e.g., `.txt`, `.mp3`, `.ogg`) into the `src/static/` directory *before* building the Docker image.
2.  Rebuild the Docker image as shown in step 1.
3.  Run the container again. Your new content will appear on the web interface.

**Example `src/static/` content:**

```
src/static/
├── message_from_the_void.txt
├── survival_tip_01.txt
└── ambient_wasteland_winds.mp3
```

## Development and Testing

### Running Tests

Tests are executed within a separate Docker container to ensure a consistent environment.

1.  Navigate to the `nightly-broadcast-beacon` directory.
2.  Run the test script:

    ```bash
    ./tests/run_tests.sh
    ```

This script will build a test-specific Docker image and execute the Python unit tests for the Flask application.
