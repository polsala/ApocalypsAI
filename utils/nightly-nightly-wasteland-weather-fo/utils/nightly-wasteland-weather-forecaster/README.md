# Nightly Wasteland Weather Forecaster

## Overview

The 'Nightly Wasteland Weather Forecaster' is a whimsical yet practical utility designed for the intrepid survivors of the ApocalypsAI community. In a world reshaped by cataclysm, traditional weather forecasts are a relic of the past. This tool provides a simulated, post-apocalyptic weather outlook for various known (and unknown) wasteland locations, helping you anticipate hazards, plan scavenging routes, and decide whether it's safe to venture out or hunker down.

It generates forecasts based on internal, randomized (but testable!) logic, simulating conditions like radiation levels, temperature extremes, and unique wasteland events.

## Usage

To get a forecast, run the `forecaster.py` script with a location and optionally the number of days:

```bash
python src/forecaster.py --location "Old City Ruins"
python src/forecaster.py --location "Radioactive Desert" --days 5
```

### Arguments:

*   `--location <string>`: The name of the wasteland location to forecast for (e.g., "Old City Ruins", "The Glow", "Mutant Mire").
*   `--days <int>`: (Optional) The number of days to forecast. Defaults to 3.

## Example Output

```
Forecasting for Old City Ruins for 3 days:

Day 1 (2077-10-23):
  Conditions: Overcast with a chance of Acid Rain
  Temperature: Chilly (5°C / 41°F)
  Radiation: Moderate (Geiger counter clicking steadily)
  Wind: Gusty (Watch for flying debris!)
  Special Event: Scavenger's Luck - Increased chance of finding useful scrap!

Day 2 (2077-10-24):
  Conditions: Clear Skies
  Temperature: Mild (18°C / 64°F)
  Radiation: Low (Safe for short excursions)
  Wind: Calm
  Special Event: None

Day 3 (2077-10-25):
  Conditions: Dust Storm Warning
  Temperature: Scorching Hot (35°C / 95°F)
  Radiation: High - Seek Shelter! (Geiger counter screaming!)
  Wind: Strong Gale
  Special Event: Mutant Swarm Alert - Stay Indoors!
```

## Development

This utility is written in Python 3.11 and is self-contained. It uses no external APIs for weather data, relying entirely on its internal simulation logic. This ensures deterministic testing and offline usability.

## Tests

To run the tests, navigate to the utility's root directory and execute:

```bash
python -m unittest discover tests
```
