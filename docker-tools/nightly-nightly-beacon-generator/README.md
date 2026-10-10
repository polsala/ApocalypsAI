# Nightly Beacon Generator

A containerized service designed to generate unique, whimsical, and cryptographically-derived "beacon" identifiers along with evocative descriptions. Perfect for marking locations in a post-apocalyptic wasteland, generating unique IDs for resources, or simply adding a touch of mystery to your data.

## Features

*   **Unique Identifiers**: Generates SHA256-based IDs from input parameters, ensuring high uniqueness.
*   **Whimsical Descriptions**: Pairs IDs with randomly generated, evocative descriptions.
*   **Containerized**: Easy to deploy and run using Docker.
*   **Simple API**: Exposes a straightforward HTTP endpoint for beacon generation.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-beacon-generator` directory and build the Docker image:

```bash
docker build -t nightly-beacon-generator .
```

### 2. Run the Container

You can run the container in detached mode, mapping port `5000` (inside the container) to `8080` (on your host, or any available port):

```bash
docker run -d -p 8080:5000 --name beacon-service nightly-beacon-generator
```

### 3. Generate a Beacon

Once the service is running, you can make HTTP GET requests to generate beacons.

**Basic Beacon (no parameters):**

```bash
curl http://localhost:8080/generate_beacon
```

Example Response:
```json
{
  "id": "a1b2c3d4e5f67890...",
  "description": "The Whispering Spire of Forgotten Echoes",
  "timestamp": "2023-10-27T10:30:00Z"
}
```

**Beacon with Location:**

```bash
curl "http://localhost:8080/generate_beacon?location=Old%20Water%20Tower"
```

Example Response:
```json
{
  "id": "f9e8d7c6b5a43210...",
  "description": "The Rusting Sentinel of the Aqueduct",
  "timestamp": "2023-10-27T10:31:00Z"
}
```

**Beacon with Location and Purpose:**

```bash
curl "http://localhost:8080/generate_beacon?location=Abandoned%20Mine&purpose=Resource%20Cache"
```

Example Response:
```json
{
  "id": "1234567890abcdef...",
  "description": "The Veiled Cavern of Gleaming Scraps",
  "timestamp": "2023-10-27T10:32:00Z"
}
```

### 4. Stop and Remove the Container

```bash
docker stop beacon-service
docker rm beacon-service
```

### 5. Clean up the Image (Optional)

```bash
docker rmi nightly-beacon-generator
```

## Development

The service is a simple Flask application. You can run it locally without Docker for development:

```bash
pip install -r src/requirements.txt
python src/app.py
```

Then access it at `http://127.0.0.1:5000/generate_beacon`.

## Tests

Automated tests are provided to ensure the service functions as expected. See `tests/test_beacon_generator.sh`.
