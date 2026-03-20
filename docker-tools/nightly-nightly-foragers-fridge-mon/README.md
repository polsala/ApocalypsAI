# Nightly Forager's Fridge Monitor

A whimsical, containerized web service designed to help post-apocalyptic foragers keep track of their scavenged goods' freshness. No more guessing if that "mystery meat" is still edible or has achieved sentience! This tool provides a simple web interface to add items, set their estimated shelf life, and receive charmingly grim warnings when they're about to turn.

## Features

*   **Item Tracking**: Add scavenged items with a name and estimated days until spoilage.
*   **Whimsical Warnings**: Get unique, apocalypse-themed messages as items approach or pass their spoilage date.
*   **Simple Web UI**: Easy-to-use interface accessible via your browser.
*   **Containerized**: Runs entirely within a Docker container for easy deployment and isolation.

## Getting Started

### Prerequisites

*   Docker and Docker Compose installed on your system.

### Running the Monitor

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    # Assuming you are in the root of the ApocalypsAI repository
    cd docker-tools/nightly-foragers-fridge-mon
    ```

2.  **Build and run the Docker container using Docker Compose:**
    ```bash
    docker-compose up --build -d
    ```
    This command will:
    *   Build the Docker image for the `fridge-monitor` service.
    *   Start the container in detached mode (`-d`).
    *   Map port `8080` on your host to port `8080` inside the container.
    *   Create a named volume `fridge_data` to persist your item data across container restarts.

3.  **Access the Web Interface:**
    Open your web browser and navigate to `http://localhost:8080`.

### Stopping the Monitor

To stop and remove the container (but keep the data volume):
```bash
docker-compose down
```

To stop and remove the container and its associated data volume:
```bash
docker-compose down -v
```

## Usage

Once the web interface is open:

*   **Add New Item**: Use the form to enter an item name (e.g., "Glowing Mushroom", "Pre-War Canned Beans") and the estimated days until it spoils.
*   **View Items**: See a list of all tracked items, their remaining freshness, and any spoilage warnings.
*   **Mark as Consumed/Spoiled**: Click the respective buttons to remove items from your inventory.

## Development & Testing

### Running Tests

Tests are written in Python and can be run directly against the application logic.

1.  **Install Python dependencies (if testing outside Docker):**
    ```bash
    pip install -r src/requirements.txt
    pip install pytest # For running tests
    ```
2.  **Run the tests:**
    ```bash
    pytest tests/
    ```

### Project Structure

```
.
├── README.md
├── src/
│   ├── app.py              # Flask web application
│   ├── database.py         # SQLite database operations
│   ├── Dockerfile          # Defines the Docker image
│   └── requirements.txt    # Python dependencies
└── tests/
    └── test_app.py         # Unit tests for the Flask application
└── docker-compose.yml      # Docker Compose configuration
```
