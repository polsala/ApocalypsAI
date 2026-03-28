# Nightly Cosmic Compass

## 🌌 Unveiling the Cosmos' Whispers 🌌

The `nightly-cosmic-compass` is a whimsical-yet-useful command-line utility designed to help you connect with the celestial wonders above. Given your geographical latitude and a specific date, it will consult its ancient cosmic charts to reveal the most 'influential' cosmic anomaly visible from your vantage point.

Whether you're a seasoned stargazer, a curious wanderer, or simply seeking a touch of cosmic guidance, this compass will point you towards the most potent celestial presence of the night.

## ✨ Features

*   **Location-Aware**: Determines visibility based on your latitude (Northern, Southern, or Equatorial hemisphere).
*   **Time-Sensitive**: Filters anomalies based on the specified month, allowing for seasonal celestial events.
*   **Influence Ranking**: Identifies the 'most influential' anomaly from those visible, based on predefined cosmic scores.
*   **Whimsical Descriptions**: Provides enchanting descriptions for each celestial body.

## 🚀 Installation

This utility is a standalone Node.js script. No `npm install` is strictly required if you have Node.js installed, but you can run it directly.

1.  Ensure you have Node.js (v14 or higher) installed on your system.
2.  Navigate to the `node-utils/nightly-cosmic-compass` directory.

## 🔭 Usage

Run the script from your terminal, providing your latitude and an optional date.

```bash
node src/index.js --lat=<latitude> [--lon=<longitude>] [--date=<YYYY-MM-DD>]
```

*   `--lat=<latitude>`: Your geographical latitude (e.g., `40.7128` for New York, `-33.8688` for Sydney). This is **required**.
*   `--lon=<longitude>`: Your geographical longitude (e.g., `-74.0060`). This is optional and currently not used for visibility calculations but can be included.
*   `--date=<YYYY-MM-DD>`: The specific date for which you want to find the anomaly (e.g., `2023-10-26`). If omitted, the current system date will be used.

### Examples:

**1. Find the anomaly for New York City (approx. 40°N) today:**

```bash
node src/index.js --lat=40.7128
```

**2. Find the anomaly for Sydney (approx. 33°S) on a specific date:**

```bash
node src/index.js --lat=-33.8688 --date=2024-06-15
```

**3. Find the anomaly for the Equator (0°) in December:**

```bash
node src/index.js --lat=0 --date=2023-12-01
```

## 🧪 Tests

To run the self-contained tests, execute the `test.js` file using Node.js:

```bash
node tests/test.js
```

The tests use Node.js's built-in `assert` module and mock `fs.readFileSync` and `Date` objects to ensure deterministic and offline execution, verifying the core logic under various conditions.

## 📜 Cosmic Anomalies Data

The `src/cosmic_anomalies.json` file contains the predefined list of celestial objects, their descriptions, visibility windows (by month), and influence scores. Feel free to expand this cosmic catalog with your own discoveries!
