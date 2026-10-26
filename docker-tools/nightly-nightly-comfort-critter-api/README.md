# Nightly Comfort Critter API

## Summary
In the ever-challenging landscape of the apocalypse, even the most hardened survivors need a moment of peace. The `nightly-comfort-critter-api` is a whimsical, containerized micro-service designed to provide just that: a quick, comforting image URL and a soothing quote to brighten your day.

It's a small beacon of calm, easily deployed and integrated into any dashboard, monitoring system, or personal script that needs a gentle reminder that things can be okay.

## How it Works
The Comfort Critter API is a simple Flask application packaged in a Docker container. When you hit its `/comfort` endpoint, it randomly selects a comforting image URL and a soothing quote from its internal collection and returns them as a JSON object.

It also includes a `/health` endpoint to ensure the critter is purring happily.

## Getting Started

### Prerequisites
- Docker installed on your system.

### Build the Docker Image
Navigate to the `nightly-comfort-critter-api` directory and build the Docker image:

```bash
docker build -t comfort-critter-api .
```

### Run the Docker Container
Once the image is built, you can run the container. It will expose the API on port `5000`.

```bash
docker run -p 5000:5000 --name comfort-critter comfort-critter-api
```

### Access the API

#### Health Check
To check if the critter is alive and well, open your browser or use `curl`:

```bash
curl http://localhost:5000/health
```

Expected output:
```json
{
  "status": "Critter is purring!"
}
```

#### Get Comfort
To receive your daily dose of comfort, hit the `/comfort` endpoint:

```bash
curl http://localhost:5000/comfort
```

Example output:
```json
{
  "image_url": "https://i.imgur.com/example1.jpg",
  "message": "May this bring a moment of peace to your apocalyptic day!",
  "quote": "Even the darkest night will end and the sun will rise."
}
```

(Note: The image URLs are placeholders. In a real-world scenario, you'd replace them with actual URLs to comforting images.)

## Development

### Local Setup
If you want to run the Flask app directly without Docker for development:

1.  **Install dependencies:**
    ```bash
pip install -r src/requirements.txt
    ```
2.  **Run the application:**
    ```bash
python src/app.py
    ```
    The API will be available at `http://127.0.0.1:5000`.

### Testing
Tests are written using `pytest` and can be run as follows:

```bash
pip install pytest
pip install -e .
pytest tests/
```

## Contributing
Feel free to add more comforting images (ensure they are publicly accessible URLs) or soothing quotes to the `src/app.py` file! Just submit a pull request.
