# Nightly Luminescence Scheduler

A whimsical-yet-useful CLI tool for the ApocalypsAI community to schedule and manage "luminescent events." Whether you're activating your glowing mushroom patch, timing your solar lanterns, or just need a reminder for a fixed "light-up" event, this utility helps you keep your post-apocalyptic glow on schedule.

## Features

*   **Event Scheduling**: Define events that trigger at fixed times or relative to simulated sunrise/sunset.
*   **Customizable**: Easily configure your events and twilight hours via a JSON file.
*   **CLI Interface**: Get your daily luminescence schedule directly from your terminal.

## Installation

1.  Navigate to the `node-utils/nightly-luminescence-scheduler` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

1.  **Create a configuration file** (e.g., `luminescence-config.json` or modify the default `config.json`):

    ```json
    {
      "defaultSunrise": "06:30",
      "defaultSunset": "18:45",
      "events": [
        { "name": "Activate Glowing Mushroom Patch", "type": "sunset-offset", "offsetMinutes": -45 },
        { "name": "Deploy Solar-Powered Nightlights", "type": "sunset-offset", "offsetMinutes": 15 },
        { "name": "Retrieve Solar Chargers", "type": "sunrise-offset", "offsetMinutes": 30 },
        { "name": "Perform Bioluminescent Algae Check", "type": "fixed", "time": "21:00" }
      ]
    }
    ```
    *   `defaultSunrise` / `defaultSunset`: (Optional) Default times in `HH:MM` format. If not provided, hardcoded defaults (06:00, 18:00) are used.
    *   `events`: An array of event objects.
        *   `name`: A descriptive name for the event.
        *   `type`: `fixed`, `sunrise-offset`, or `sunset-offset`.
        *   `time`: (Required for `fixed` type) Time in `HH:MM` format.
        *   `offsetMinutes`: (Required for `sunrise-offset`/`sunset-offset` types) Offset in minutes. Positive for after, negative for before.

2.  **Run the scheduler**:

    ```bash
    node src/index.js --config ./luminescence-config.json --date 2024-07-20
    ```
    *   `--config <path>`: (Optional) Path to your JSON configuration file. Defaults to `config.json` in the utility's root directory.
    *   `--date <YYYY-MM-DD>`: (Optional) Date for which to generate the schedule. Defaults to today.

    **Example Output:**
    ```
    Luminescence Schedule for 2024-07-20:
    ------------------------------------
    [07:00] Retrieve Solar Chargers
    [18:00] Activate Glowing Mushroom Patch
    [19:00] Deploy Solar-Powered Nightlights
    [21:00] Perform Bioluminescent Algae Check
    ```

## Development

### Running Tests

```bash
npm test
```
