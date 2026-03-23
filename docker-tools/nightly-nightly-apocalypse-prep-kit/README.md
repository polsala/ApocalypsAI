# Nightly Apocalypse Prep-Kit

## Summary
A containerized web service that generates whimsical yet practical survival item lists for various apocalypse scenarios.

## Description
Ever wondered what you'd need for a Disco Apocalypse or a Robot Uprising? The `nightly-apocalypse-prep-kit` is here to help! This Flask-based web service, packaged in a Docker container, provides a simple API to generate a randomized list of essential (and sometimes absurd) items tailored to different end-of-the-world scenarios. It's perfect for a quick laugh, a brainstorming session, or just to feel a little more prepared for the inevitable.

## How it Works
The utility exposes a simple HTTP API. When you hit the `/generate_kit` endpoint, it randomly selects three items from a predefined list specific to a chosen apocalypse scenario. If no scenario is specified, it defaults to 'zombie'.

## Available Scenarios
*   `zombie`: The undead walk among us! Prepare for shambling hordes.
*   `alien_invasion`: Little green (or grey, or purple) men are here for our planet!
*   `robot_uprising`: Our silicon overlords have decided we're obsolete.
*   `disco_apocalypse`: The world is ending in a flurry of glitter and questionable fashion choices.
*   `existential_dread`: The universe is vast and uncaring. Prepare for profound introspection.

## How to Run (Docker)

1.  **Build the Docker image:**
    ```bash
    docker build -t apocalypse-prep-kit .
    ```

2.  **Run the container:**
    ```bash
    docker run -p 5000:5000 --name apocalypse-kit-instance apocalypse-prep-kit
    ```
    The service will be available at `http://localhost:5000`.

## API Usage

### Root Endpoint
Access the root endpoint to see a welcome message and available scenarios:

```bash
curl http://localhost:5000/
```

Example Response:
```json
{
  "available_scenarios": [
    "zombie",
    "alien_invasion",
    "robot_uprising",
    "disco_apocalypse",
    "existential_dread"
  ],
  "message": "Welcome to the Pocket Apocalypse Prep-Kit! Use /generate_kit to get your survival list.",
  "usage": "/generate_kit?scenario=<scenario_name>"
}
```

### Generate Kit Endpoint
Use the `/generate_kit` endpoint to get your survival kit. You can specify a scenario using the `scenario` query parameter.

*   **Default Scenario (Zombie):**
    ```bash
    curl http://localhost:5000/generate_kit
    ```
    Example Response:
    ```json
    {
      "apocalypse_prep_kit": [
        "Crowbar (for cranial re-education)",
        "Canned Beans (indefinite shelf life)",
        "First-Aid Kit (for bites and scrapes)"
      ],
      "description": "The undead walk among us! Prepare for shambling hordes.",
      "message": "Stay whimsical, stay prepared!",
      "scenario": "zombie"
    }
    ```

*   **Specific Scenario (Disco Apocalypse):**
    ```bash
    curl http://localhost:5000/generate_kit?scenario=disco_apocalypse
    ```
    Example Response:
    ```json
    {
      "apocalypse_prep_kit": [
        "Glitter Cannon (for blinding foes with fabulousness)",
        "Platform Boots (for reaching higher ground, or dance moves)",
        "Mirror Ball (reflect their disco rays)"
      ],
      "description": "The world is ending in a flurry of glitter and questionable fashion choices.",
      "message": "Stay whimsical, stay prepared!",
      "scenario": "disco_apocalypse"
    }
    ```

*   **Invalid Scenario:**
    ```bash
    curl http://localhost:5000/generate_kit?scenario=unicorn_stampede
    ```
    Example Response:
    ```json
    {
      "error": "Scenario 'unicorn_stampede' not found. Available scenarios: zombie, alien_invasion, robot_uprising, disco_apocalypse, existential_dread"
    }
    ```

## Development and Testing

To run the automated tests, use the provided `run_tests.sh` script:

```bash
./tests/run_tests.sh
```
This script will build a separate Docker image for testing and execute the unit tests within it, ensuring a clean and isolated test environment.
