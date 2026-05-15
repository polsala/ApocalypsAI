# Nightly Wasteland Courier Dispatcher

## Summary

The `nightly-wasteland-courier-disp` is a containerized Flask application designed to assist post-apocalyptic dispatchers in planning optimal routes for their couriers. It takes a series of waypoints and calculates an estimated danger rating and resource consumption for the proposed path, considering simulated wasteland hazards.

## How it Works

This utility runs as a Docker container, exposing a simple REST API. You provide a starting point, an ending point, and optional waypoints, and the service returns a detailed breakdown of the path, including segment-by-segment danger ratings and resource consumption estimates. It uses a whimsical internal model of "wasteland hazards" (radiation, mutants, resources) to influence its calculations.

## Setup and Installation

1.  **Ensure Docker is installed**: If you don't have Docker, follow the official installation guide for your operating system.

2.  **Clone the repository (if not already in the utility directory)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/docker-tools/nightly-wasteland-courier-disp
    ```

3.  **Build the Docker image**:
    ```bash
    docker build -t wasteland-courier-dispatcher .
    ```

4.  **Run the Docker container**:
    ```bash
    docker run -p 5000:5000 --name courier-dispatcher-service -d wasteland-courier-dispatcher
    ```
    This will run the service in the background, mapping port 5000 from the container to port 5000 on your host machine.

## Usage

The service exposes a single API endpoint: `/optimize_route`.

### `POST /optimize_route`

**Description**: Calculates the danger and resource consumption for a given courier route.

**Request Body (JSON)**:

```json
{
  "start": "string",
  "end": "string",
  "waypoints": ["string", "string", ...]
}
```

*   `start` (required): The starting location for the courier.
*   `end` (required): The final destination for the courier.
*   `waypoints` (optional): An array of intermediate locations the courier must pass through.

**Example Request**:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"start": "Oasis Haven", "end": "Dusty Flats", "waypoints": ["Sector Alpha", "Whispering Canyons"]}' \
     http://localhost:5000/optimize_route
```

**Example Response (JSON)**:

```json
{
  "dispatch_advice": "Proceed with caution, courier! The wasteland is ever-changing.",
  "detailed_segments": [
    {
      "distance_units": 15.23,
      "from": "Oasis Haven",
      "segment_danger_rating": 3.45,
      "segment_resource_consumption": 1.67,
      "to": "Sector Alpha"
    },
    {
      "distance_units": 28.76,
      "from": "Sector Alpha",
      "segment_danger_rating": 12.12,
      "segment_resource_consumption": 2.61,
      "to": "Whispering Canyons"
    },
    {
      "distance_units": 42.11,
      "from": "Whispering Canyons",
      "segment_danger_rating": 18.95,
      "segment_resource_consumption": 4.16,
      "to": "Dusty Flats"
    }
  ],
  "estimated_total_resource_consumption": 8.44,
  "overall_danger_rating": 34.52,
  "path_taken": [
    "Oasis Haven",
    "Sector Alpha",
    "Whispering Canyons",
    "Dusty Flats"
  ],
  "total_distance_units": 86.1
}
```

## Stopping the Service

To stop and remove the running container:

```bash
docker stop courier-dispatcher-service
docker rm courier-dispatcher-service
```

## Development and Testing

To run tests, you can execute them directly within the container or on your host machine if Python dependencies are installed.

**Running tests inside the container (after building the image)**:

```bash
docker run --rm wasteland-courier-dispatcher python tests/test_app.py
```

**Running tests on host (requires Python and Flask installed)**:

```bash
pip install -r src/requirements.txt
python tests/test_app.py
```
