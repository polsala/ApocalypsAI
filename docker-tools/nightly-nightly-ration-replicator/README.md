# Nightly Ration Replicator

A whimsical-yet-useful containerized web application to help you track and plan your emergency rations. Keep tabs on your survival supplies, get alerts for expiring items, and enjoy some post-apocalyptic nutritional wisdom.

## Features

*   Add and list ration items with quantity, expiry date, and caloric value.
*   Receive alerts for rations expiring within a configurable timeframe.
*   Generate whimsical, apocalypse-themed nutritional facts.
*   Runs entirely within a Docker container for easy deployment and isolation.

## Usage

### Prerequisites

*   Docker installed on your system.

### Build the Docker Image

Navigate to the `nightly-ration-replicator` directory and build the Docker image:

```bash
docker build -t nightly-ration-replicator .
```

### Run the Container

Once the image is built, you can run the container. The application will be accessible on port `8080`.

```bash
docker run -p 8080:8080 nightly-ration-replicator
```

### Access the Web Application

Open your web browser and go to `http://localhost:8080`.

### API Endpoints

*   **GET `/`**: Home page with basic instructions.
*   **GET `/rations`**: List all stored ration items.
*   **POST `/rations`**: Add a new ration item.
    *   **Body (JSON)**: `{"name": "Canned Beans", "quantity": 5, "expiry": "YYYY-MM-DD", "calories_per_unit": 200}`
*   **GET `/fact`**: Get a random whimsical nutritional fact.
*   **GET `/expiry?days=X`**: Get rations expiring within `X` days from today. (e.g., `/expiry?days=30`)

## Example Workflow

1.  **Build**: `docker build -t nightly-ration-replicator .`
2.  **Run**: `docker run -p 8080:8080 nightly-ration-replicator`
3.  **Add Rations (using curl or browser dev tools)**:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"name": "MRE Pack", "quantity": 2, "expiry": "2026-01-15", "calories_per_unit": 1200}' http://localhost:8080/rations
    curl -X POST -H "Content-Type: application/json" -d '{"name": "Water Purification Tablets", "quantity": 10, "expiry": "2024-07-01", "calories_per_unit": 0}' http://localhost:8080/rations
    ```
4.  **List Rations**: Open `http://localhost:8080/rations` in your browser.
5.  **Check Expiry**: Open `http://localhost:8080/expiry?days=180` to see items expiring in the next 180 days.
6.  **Get a Fact**: Open `http://localhost:8080/fact`.

## Development

The application is a simple Flask web service.

### Local Setup (without Docker)

1.  Create a virtual environment: `python3 -m venv venv`
2.  Activate it: `source venv/bin/activate`
3.  Install dependencies: `pip install -r src/requirements.txt`
4.  Run the app: `python3 src/app.py` (or `gunicorn -w 4 -b 0.0.0.0:8080 src.app:app`)

### Tests

Run tests using `pytest`:

```bash
pip install pytest
pytest tests/
```
