# Nightly Mood Beacon

A whimsical, containerized web utility designed to broadcast a community's current "mood" or status. Perfect for small, distributed teams or post-apocalyptic settlements needing a simple, visual way to communicate.

## Features

*   **Customizable Message**: Set a short status message via an environment variable.
*   **Customizable Color**: Choose a background color to visually represent the mood (e.g., "green" for calm, "red" for alert).
*   **Lightweight**: Built with Flask and Gunicorn, packaged in a small Docker image.
*   **Simple Web Interface**: A single page displaying the message and color.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-mood-beacon` directory and build the image:

```bash
docker build -t nightly-mood-beacon .
```

### 2. Run the Container

You can run the beacon with default settings or customize it using environment variables.

**Default Run:**

```bash
docker run -p 8080:8080 nightly-mood-beacon
```
Access it at `http://localhost:8080`.

**Customizing Message and Color:**

Use `BEACON_MESSAGE` and `BEACON_COLOR` environment variables. `BEACON_COLOR` accepts any valid CSS color name or hex code (e.g., `red`, `green`, `blue`, `#FFD700`).

```bash
docker run -p 8080:8080 \
  -e BEACON_MESSAGE="All clear, foraging party successful!" \
  -e BEACON_COLOR="forestgreen" \
  nightly-mood-beacon
```

Or for a more urgent status:

```bash
docker run -p 8080:8080 \
  -e BEACON_MESSAGE="Anomaly detected! Seek shelter!" \
  -e BEACON_COLOR="darkred" \
  nightly-mood-beacon
```

Access your beacon at `http://localhost:8080` in your web browser.

## Development

### Project Structure

```
.
├── Dockerfile              # Defines the Docker image
├── README.md               # This file
├── src/
│   ├── app.py              # Flask application logic
│   └── templates/
│       └── index.html      # HTML template for the beacon
└── tests/
    ├── test_app.py         # Unit tests for the Flask application
    └── run_tests.sh        # Script to run the unit tests
```

### Running Tests

To run the unit tests for the Flask application:

```bash
./tests/run_tests.sh
```

This script will install `Flask` and `pytest` in a temporary Python environment and execute `test_app.py`.
