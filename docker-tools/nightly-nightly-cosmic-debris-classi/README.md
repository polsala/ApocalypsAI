# Nightly Cosmic Debris Classifier

## Summary
This utility provides a whimsical, containerized web service to classify descriptions of mysterious objects found in the wasteland, affectionately termed 'cosmic debris'. It offers a category, a whimsical name, and a survival tip for each classified item.

## How It Works
The service runs a simple Flask application within a Docker container. Upon receiving a POST request with a text description, it uses keyword matching to assign the debris to one of several whimsical categories (e.g., Temporal Fragment, Eldritch Goo, Stellar Shard, Void-Touched Relic, Mundane Misdirection). Each category comes with a unique, often humorous, survival tip.

## Usage

### Prerequisites
- Docker installed and running.

### 1. Build the Docker Image
Navigate to the `nightly-cosmic-debris-classif` directory and build the Docker image:

```bash
docker build -t cosmic-debris-classifier .
```

### 2. Run the Docker Container
Run the container, mapping port 5000 from the container to your host machine:

```bash
docker run -p 5000:5000 cosmic-debris-classifier
```

The service will now be accessible at `http://localhost:5000`.

### 3. Use the API
Send a POST request to the `/classify` endpoint with a JSON body containing a `description` field.

**Example using `curl`:**

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"description": "A shimmering crystal that hums with a faint, ancient melody."}' \
     http://localhost:5000/classify
```

**Example Response:**

```json
{
  "category": "Stellar Shard",
  "survival_tip": "Hold it to your ear; it might hum the location of the nearest potable water source, or just a catchy tune.",
  "whimsical_name": "Harmonic Star-Splinter"
}
```

### API Reference

*   **Endpoint**: `/classify`
*   **Method**: `POST`
*   **Request Body**: `application/json`
    ```json
    {
      "description": "string" // A textual description of the cosmic debris
    }
    ```
*   **Response Body (Success 200)**: `application/json`
    ```json
    {
      "category": "string",       // The classified category of the debris
      "whimsical_name": "string", // A whimsical name for the debris
      "survival_tip": "string"    // A humorous survival tip related to the debris
    }
    ```
*   **Response Body (Error 400)**: `application/json`
    ```json
    {
      "error": "string" // Error message, e.g., "Missing 'description' in request body"
    }
    ```

## Development and Testing

To run tests, ensure you have `Flask` and `unittest` (standard library) installed in your Python environment. Navigate to the utility's root directory and run:

```bash
python -m unittest tests/test_app.py
```
