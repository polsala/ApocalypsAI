# Nightly Container Whisperer

The digital world can be a lonely place for our containerized companions. Are they happy? Are they stressed? Are they silently screaming into the void? The Nightly Container Whisperer is here to help you understand their innermost feelings!

This whimsical utility runs as a Docker container itself, connecting to your Docker daemon to listen to the logs of other specified containers. It then analyzes these logs for keywords, assigning a "mood" to each container and providing a charming, if slightly dramatic, summary of their emotional state.

## Features

*   **Mood Detection**: Identifies "Grumpy" (errors), "Anxious" (warnings), "Chatty" (info), and "Serene" (normal) states.
*   **Real-time Insights**: Continuously monitors logs for changes in mood.
*   **Whimsical Reporting**: Presents container states in an easy-to-digest, emotionally-charged format.
*   **Dockerized**: Runs as a self-contained Docker image, easily deployable alongside your other containers.

## How to Use

1.  **Prerequisites**: Ensure Docker is installed and running on your host. The Whisperer needs access to the Docker daemon socket.

2.  **Build the Image (Optional, or pull from a registry if available)**:
    ```bash
    docker build -t nightly-container-whisperer .
    ```

3.  **Run the Whisperer**:
    You need to mount the Docker socket so the Whisperer can communicate with your Docker daemon. You also need to specify which containers to listen to using the `CONTAINER_NAMES` environment variable (comma-separated).

    ```bash
    docker run -d \
      --name container-whisperer \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -e CONTAINER_NAMES="my-web-app,my-database,another-service" \
      nightly-container-whisperer
    ```
    Replace `my-web-app,my-database,another-service` with the actual names of the containers you want to monitor.

4.  **View the Whispers**:
    The Whisperer will output its emotional reports to its own logs.
    ```bash
    docker logs -f container-whisperer
    ```

    Example Output:
    ```
    [2023-10-27 08:00:01] 🌙 Nightly Container Whisperer Report 🌙
    [2023-10-27 08:00:01] ---------------------------------------
    [2023-10-27 08:00:01] Container 'my-web-app': Feeling Serene 😌. All is calm in its digital garden.
    [2023-10-27 08:00:01] Container 'my-database': Feeling Anxious 😨. A few warnings suggest it's a bit stressed.
    [2023-10-27 08:00:01] Container 'another-service': Feeling Grumpy 😠. Multiple errors indicate it's having a very bad day.
    [2023-10-27 08:00:01] ---------------------------------------
    ```

## Configuration

*   `CONTAINER_NAMES`: (Required) Comma-separated list of Docker container names to monitor.
*   `POLLING_INTERVAL_SECONDS`: (Optional, default: `60`) How often the Whisperer checks for new log lines and updates moods.

## Development

To run locally without Docker (for testing the Python logic):
```bash
pip install docker
python src/app.py
```
(Note: This will attempt to connect to your Docker daemon and requires `CONTAINER_NAMES` to be set in your environment.)

## Contributing

Feel free to add more sophisticated mood detection, new whimsical reports, or support for more log sources!
