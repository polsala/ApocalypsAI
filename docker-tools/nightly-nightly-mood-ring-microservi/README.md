# Nightly Mood Ring Microservice

A whimsical, containerized microservice that analyzes short text inputs to determine their "mood" or "vibe," assigning a corresponding color and emoji. Perfect for quickly gauging the sentiment of commit messages, daily logs, or any textual snippet without leaving your local environment.

## Features

*   **Offline Sentiment Analysis:** Simple keyword-based analysis, no external APIs needed.
*   **Whimsical Output:** Provides a mood name, a hex color code, and a relevant emoji.
*   **Containerized:** Easy to deploy and run anywhere Docker is available.
*   **Lightweight:** Built with Flask for minimal overhead.

## How to Use

### 1. Build the Docker Image

Navigate to the `nightly-mood-ring-microservice` directory (or the directory containing this README and the `src` folder) and build the Docker image:

```bash
docker build -t mood-ring-microservice .
```

### 2. Run the Microservice

Run the container, mapping port 5000 (inside the container) to port 5000 (on your host machine):

```bash
docker run -p 5000:5000 mood-ring-microservice
```

The service will now be running at `http://localhost:5000`.

### 3. Interact with the API

You can send POST requests to the `/analyze` endpoint with a JSON payload containing your text.

**Example using `curl`:**

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"text": "Fixed a critical bug, feeling much better now!"}' \
     http://localhost:5000/analyze
# Expected output: {"mood": "Sunny Disposition", "color": "#CDDC39", "emoji": "😊", "analysis": "Positive"}

curl -X POST -H "Content-Type: application/json" \
     -d '{"text": "Refactored the logging module. Standard stuff."}' \
     http://localhost:5000/analyze
# Expected output: {"mood": "Calm Current", "color": "#2196F3", "emoji": "😌", "analysis": "Neutral"}

curl -X POST -H "Content-Type: application/json" \
     -d '{"text": "Encountered a major issue, the system is broken."}' \
     http://localhost:5000/analyze
# Expected output: {"mood": "Stormy Seas", "color": "#F44336", "emoji": "⛈️", "analysis": "Very Negative"}

curl -X POST -H "Content-Type: application/json" \
     -d '{"text": "This is a great new feature, but it has a small bug."}' \
     http://localhost:5000/analyze
# Expected output: {"mood": "Rainbow Ripple", "color": "#9C27B0", "emoji": "🌈", "analysis": "Mixed"}
```

### 4. Stop the Microservice

Press `Ctrl+C` in the terminal where the Docker container is running.

## Development

### Running Tests

To run the tests, you can execute them inside the container or locally if you have Python and `pytest` installed.

**Inside the container (after building the image):**

```bash
docker run mood-ring-microservice pytest
```

**Locally (requires Python 3.x and `pytest`):**

```bash
pip install -r src/requirements.txt
pytest tests/test_app.py
```
