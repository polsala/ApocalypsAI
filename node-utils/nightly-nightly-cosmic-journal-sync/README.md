## Nightly Cosmic Journal Synchronizer

This whimsical utility helps you keep your personal cosmic observations in sync with the grand 'Starlight Logbook' API. It's designed to be run nightly, ensuring your discoveries of nebulae, rogue asteroids, and peculiar stellar phenomena are never lost to the void.

### Features

*   **Local Observation Storage**: Stores your cosmic sightings in a simple JSON file.
*   **API Synchronization**: Pushes new observations to the fictional 'Starlight Logbook' API.
*   **Error Handling**: Gracefully handles API errors and network issues.
*   **Whimsical Output**: Provides fun, space-themed feedback.

### Installation

1.  Clone this repository.
2.  Navigate to the `utils/nightly-cosmic-journal-sync` directory.
3.  Run `npm install` to install dependencies.

### Usage

1.  **Configure API Endpoint**: Update the `STARLIGHT_LOGBOOK_API_URL` in `src/config.js` to your desired (or mock) API endpoint.
2.  **Add Observations**: Manually add your cosmic observations to `data/observations.json` in the following format:
    ```json
    [
      {
        "timestamp": "2023-10-27T10:00:00Z",
        "phenomenon": "Supernova Remnant",
        "description": "A faint, expanding cloud of gas and dust, likely from a star's death.",
        "location": "Orion Nebula vicinity"
      }
    ]
    ```
3.  **Run the Synchronizer**: Execute the script from the utility's directory:
    ```bash
    node src/main.js
    ```

### Development & Testing

The utility includes unit tests that mock the API calls. To run the tests:

```bash
npm test
```

### Data Format (`data/observations.json`)

An array of observation objects, each with:

*   `timestamp` (string, ISO 8601 format)
*   `phenomenon` (string)
*   `description` (string)
*   `location` (string, optional)

### API Interaction (Mocked)

The utility expects a POST request to the configured `STARLIGHT_LOGBOOK_API_URL` with the observation data in the request body.

### License

This utility is provided under the MIT License.
