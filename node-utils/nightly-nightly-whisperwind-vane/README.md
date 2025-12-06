# Nightly Whisperwind Vane

A whimsical CLI utility for the ApocalypsAI community that provides a "Whisperwind Weather Forecast" based on simulated environmental conditions. Ever wondered if today brings a "Temporal Drizzle" or a "Radiant Haze"? This tool has you covered!

## Features

*   Reads simulated environmental data (temperature, radiation, anomaly index, wind speed, temporal stability).
*   Generates a unique, whimsical weather forecast string.
*   Easy to run from the command line.

## Installation

1.  Navigate to the `node-utils/nightly-whisperwind-vane` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

Run the utility from the command line:

```bash
node src/main.js [path_to_environment_data.json]
```

If `path_to_environment_data.json` is not provided, it defaults to `data/environment.json`.

### Example

```bash
node src/main.js
# Output: Whisperwind Weather Vane Forecast:
# The air shimmers with a Radiant Haze, hinting at stable temporal currents. Watch for minor dust devils.
```

## Simulated Environment Data (`data/environment.json`)

The utility expects a JSON file with the following structure:

```json
{
  "temperature": 25,          // Celsius
  "radiation_level": 0.1,     // Sieverts (low, medium, high)
  "anomaly_index": 0.05,      // 0.0-1.0 (low, medium, high)
  "wind_speed": 15,           // km/h
  "temporal_stability": 0.9   // 0.0-1.0 (low, high)
}
```

Adjust these values to see different forecast outcomes!

## Development & Testing

To run the automated tests:

```bash
npm test
```
