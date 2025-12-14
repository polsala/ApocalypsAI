# Nightly Wasteland Almanac

A containerized web server offering daily survival wisdom, foraging tips, and wasteland lore for the discerning survivor. This utility provides a quick, offline-accessible reference for those navigating the post-apocalyptic landscape, ensuring you're always equipped with a nugget of knowledge.

## Features

*   **Daily Wisdom**: A new, randomly selected survival quote or tip each day, consistent for that day.
*   **Foraging Guide**: Essential tips for identifying edible (and inedible) flora and fauna.
*   **Wasteland Lore**: Snippets of history, myths, and legends from the shattered world.
*   **Self-contained**: Runs entirely within a Docker container, no external dependencies once built.

## Usage

### Prerequisites

*   Docker installed on your system.

### Build the Docker Image

Navigate to the `nightly-wasteland-almanac` directory and run:

```bash
docker build -t wasteland-almanac .
```

### Run the Container

Once the image is built, you can run the almanac:

```bash
docker run -p 8080:5000 wasteland-almanac
```

This command maps port `8080` on your host machine to port `5000` inside the container (where the Flask app runs).

### Access the Almanac

Open your web browser and navigate to:

```
http://localhost:8080
```

You will see the Nightly Wasteland Almanac homepage with your daily wisdom, foraging tips, and lore.

## Customization

You can easily customize the content by editing the text files in the `src/data/` directory:

*   `src/data/wisdom.txt`: Add or modify daily wisdom quotes (one per line).
*   `src/data/foraging_tips.txt`: Update foraging advice (one per line).
*   `src/data/lore.txt`: Expand the wasteland lore (one per line).

After making changes, rebuild the Docker image for them to take effect.

## Development & Testing

The application is built with Flask. The tests ensure the core logic, such as data loading and daily wisdom selection, functions correctly.

### Running Tests

To run the Python unit tests:

```bash
# First, ensure Flask is installed in your local Python environment
pip install Flask

# Then run the tests
python -m unittest tests/test_app.py
```

The tests mock the current date to ensure deterministic "daily" wisdom selection.
