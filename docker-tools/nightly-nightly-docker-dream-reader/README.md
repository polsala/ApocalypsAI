# Nightly Docker Dream Reader

## Unveiling the Subconscious of Your Containers

The `nightly-docker-dream-reader` is a whimsical, containerized utility designed to bring a touch of the mystical to your daily DevOps routine. Instead of dry log analysis, this tool interprets the "dreams" (patterns and events) within your Docker container logs, offering playful insights into their operational state. Are your containers having nightmares, or are they basking in serene slumber? Let the Dream Reader tell you!

## Features

*   **Whimsical Interpretations:** Translates common log patterns (errors, restarts, startups, high activity) into imaginative "dream reports."
*   **Containerized:** Runs as a standalone Docker container, making it easy to integrate into any environment where Docker logs are accessible.
*   **Pattern-Based Analysis:** Uses simple regex patterns to identify key events within log files.
*   **Lightweight:** Built on Python, it's efficient and has minimal dependencies.

## How it Works

The Dream Reader scans a specified log file for predefined patterns. Each pattern corresponds to a "dream archetype." Based on the most prominent or critical patterns found, it generates a unique, whimsical interpretation of your container's "state of mind."

## Usage

1.  **Build the Docker Image (if not using a pre-built one):**
    ```bash
    docker build -t nightly-docker-dream-reader .
    ```

2.  **Run the Dream Reader:**
    You need to mount your container's log file (or the directory containing it) into the Dream Reader container.

    ```bash
    # Example: Analyzing logs from a container named 'my_app_container'
    # First, find the log path for your container. This often depends on your Docker logging driver.
    # For 'json-file' driver, logs are usually in /var/lib/docker/containers/<container_id>/<container_id>-json.log
    # Let's assume you have a log file at /path/to/your/app.log on the host.

    docker run --rm \
      -v /path/to/your/app.log:/app/logs/target.log \
      nightly-docker-dream-reader /app/logs/target.log
    ```

    Replace `/path/to/your/app.log` with the actual path to the log file you want to analyze on your host system. The `/app/logs/target.log` is the path *inside* the `nightly-docker-dream-reader` container where your log file will be accessible.

    **Example with a mock log file:**
    ```bash
    # Create a dummy log file
    echo "INFO: Application started successfully." > dummy.log
    echo "ERROR: Database connection failed." >> dummy.log
    echo "INFO: Processing request 123." >> dummy.log

    docker run --rm \
      -v $(pwd)/dummy.log:/app/logs/target.log \
      nightly-docker-dream-reader /app/logs/target.log

    rm dummy.log # Clean up
    ```

## Development & Testing

To run tests locally without Docker:

```bash
python -m unittest tests/test_dream_reader.py
```

## Contributing

Feel free to add more dream archetypes, refine interpretations, or suggest new features!
