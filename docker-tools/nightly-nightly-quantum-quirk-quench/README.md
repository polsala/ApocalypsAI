# Nightly Quantum Quirk Quencher

## Summary
A containerized log anomaly detector and self-healing agent for other Docker services, designed to 'quench' quantum quirks by monitoring logs for predefined patterns and taking automated actions like restarting services.

## Whimsical Purpose
In the chaotic post-apocalyptic landscape, services often develop 'quantum quirks' – unexpected errors, glitches, or temporal distortions in their log streams. The Quantum Quirk Quencher acts as a vigilant sentinel, listening to the whispers of your containers. When a quirk is detected, it swiftly intervenes, either by gently nudging the service back to stability (restarting it) or by broadcasting an urgent 'Quirk Alert' to the community.

## How It Works
1.  **Log Monitoring**: The Quencher connects to the Docker daemon and streams logs from all running containers that are explicitly labeled for monitoring.
2.  **Quirk Detection**: It scans each log line against a set of configurable regular expression patterns (the 'Quirk Patterns').
3.  **Quench Action**: Upon detecting a quirk, it performs a predefined 'Quench Action' – either restarting the problematic container or logging a notification.
4.  **Configurable**: Quirk patterns, quench actions, and monitored container labels are all configurable via environment variables.

## Usage
To deploy the Quantum Quirk Quencher, you'll typically use Docker Compose. It needs access to the Docker socket to monitor other containers.

1.  **Create a `Dockerfile`** (provided in `src/Dockerfile`) and `src/main.py` (provided).
2.  **Create a `docker-compose.yml`** (see `docker-compose.yml.example` for a template).
3.  **Label your services**: Add the `apocalypsai.monitor=true` label (or your custom label) to any service you want the Quencher to observe.

### Example `docker-compose.yml`
```yaml
version: '3.8'

services:
  # The Quantum Quirk Quencher itself
  quirk-quencher:
    build: .
    image: apocalypsai/quantum-quirk-quencher:latest
    container_name: quirk-quencher
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock # Mount Docker socket to allow monitoring
    environment:
      - QUIRK_PATTERNS=error|fail|exception|critical
      - QUENCH_ACTION=restart # or 'notify'
      - MONITORED_LABELS=apocalypsai.monitor=true # Only monitor containers with this label
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Example service to be monitored
  my-critical-app:
    image: alpine/git
    container_name: my-critical-app
    command: sh -c "while true; do echo 'INFO: App is running fine.'; sleep 2; echo 'ERROR: Something went wrong!'; sleep 3; done"
    labels:
      - apocalypsai.monitor=true # This label makes it discoverable by the quencher
      - env=prod # Additional label for more specific monitoring
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Another example service, not monitored by default
  my-other-app:
    image: busybox
    container_name: my-other-app
    command: sh -c "while true; do echo 'INFO: Other app is doing its thing.'; sleep 5; done"
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Running the Example
1.  Save the `Dockerfile`, `src/main.py`, `src/requirements.txt` in a directory.
2.  Save the `docker-compose.yml.example` content as `docker-compose.yml` in the same directory.
3.  Run `docker compose up --build -d`.

You will see `my-critical-app` logs showing errors, and the `quirk-quencher` will detect them and restart `my-critical-app`.

## Configuration
Environment variables for the `quirk-quencher` service:

*   `QUIRK_PATTERNS`: A pipe-separated list of regular expression patterns to search for in logs. Case-insensitive. Default: `error|fail|exception|denied`.
    *   Example: `QUIRK_PATTERNS=oom|timeout|connection refused`
*   `QUENCH_ACTION`: The action to take when a quirk is detected. Can be `restart` or `notify`. Default: `restart`.
    *   `restart`: Restarts the container where the quirk was found.
    *   `notify`: Logs a warning message. (In a more advanced version, this could trigger webhooks, emails, etc.)
*   `MONITORED_LABELS`: A comma-separated list of `key=value` pairs. Only containers possessing *all* these labels will be monitored. Default: `apocalypsai.monitor=true`.
    *   Example: `MONITORED_LABELS=apocalypsai.monitor=true,env=prod`

## Development

### Prerequisites
*   Python 3.8+
*   Docker and Docker Compose

### Local Testing
1.  Install dependencies: `pip install -r src/requirements.txt`
2.  Run tests: `python -m unittest tests/test_main.py`

## License
This utility is released under the MIT License.
