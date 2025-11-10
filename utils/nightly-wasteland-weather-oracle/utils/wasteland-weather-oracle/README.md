# Wasteland Weather Oracle

A whimsical yet practical command-line utility for predicting the "weather" in a post-apocalyptic wasteland. Whether you're planning a scavenging run, writing a grimdark story, or just curious about what the irradiated skies hold, the Wasteland Weather Oracle provides a daily forecast tailored to the desolation.

## Features

*   **Date-based Forecasts**: Get a consistent forecast for any given date.
*   **Whimsical Weather Events**: Predicts events like "Acid Rain", "Radiation Storm", "Dust Devil", and more.
*   **Survival Implications**: Each forecast comes with a brief note on its potential impact on a wanderer.

## How to Use

1.  Navigate to the `src` directory:
    ```bash
    cd utils/wasteland-weather-oracle/src
    ```
2.  Run the `oracle.py` script.

    *   **For today's forecast (or a random one if no date is provided):**
        ```bash
        python oracle.py
        ```
    *   **For a specific date (YYYY-MM-DD format):**
        ```bash
        python oracle.py --date 2077-10-23
        ```
        (This date will always yield the same forecast, ensuring determinism for planning.)

## Example Output

```
--- Wasteland Weather Oracle ---
Date: 2077-10-23

Forecast: Scorching Sun
Impact: Dehydration risk is extreme. Seek shade and conserve water.
```
