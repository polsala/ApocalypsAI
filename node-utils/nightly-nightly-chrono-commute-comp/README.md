# Nightly Chrono-Commute Companion

A whimsical utility for the discerning post-apocalyptic traveler. Ever wondered how you'll get to the Shifting Sands Bazaar amidst temporal distortions? This tool has you covered! It generates a random, yet surprisingly specific, commute plan including your mode of transport, destination, and the temporal anomaly you should brace for.

## Features

*   **Whimsical Transport:** From Rust-bucket Hovercrafts to Quantum Skateboards.
*   **Mysterious Destinations:** Explore the Whispering Wastes or Chronos's Clockwork Tower.
*   **Predictive Anomalies:** Be prepared for Minor Time Slips or Reality Flickers.
*   **Simple CLI:** Get your plan with a single command.

## Installation

1.  Navigate to the `node-utils/nightly-chrono-commute-comp` directory.
2.  Install dependencies (none for this version, but good practice for Node.js projects):
    ```bash
    npm install
    ```

## Usage

To generate your daily chrono-commute plan, simply run:

```bash
npm start
# or
node src/index.js
```

### Example Output

```
--- Your Nightly Chrono-Commute Plan ---
Mode of Transport: Quantum Skateboard
Destination:       The Shifting Sands Bazaar
Expected Anomaly:  Deja Vu Loop
---------------------------------------
```

## Development & Testing

To run the automated tests:

```bash
npm test
# or
node tests/index.test.js
```

Tests are deterministic and mock `Math.random` to ensure consistent results.
